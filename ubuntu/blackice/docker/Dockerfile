###############################################################################
#                         GLOBAL ARGUMENTS                                    #
###############################################################################
# Base Docker image
ARG BASE_IMAGE=databricksruntime/python:experimental
ARG package_index_url="https://pypi.org/simple"
ARG PYTHON_VERSION="3.12"
ARG LEGACY_PYTHON_VERSION="3.10"
ARG TORCH_INDEX_URL="https://download.pytorch.org/whl/torch/"

# All Python tools included in the Docker image
# - Installed globally if listed in SYSTEM_TOOLS; otherwise installed into isolated Python virtual environments
# - Installed from Git repositories if listed in GIT_TOOLS; otherwise installed from PyPI (tools installed via PyPI must be version pinned)
ARG PYTHON_TOOLS="fickling==0.1.4 rigging==3.3.2 judges==0.1.1 garak==0.13.1 giskard[llm]==2.18.0 adversarial-robustness-toolbox==1.20.1 pyrit cyberseceval lm-eval-harness promptmap fuzzyai easyedit cleverhans"

# Subset of PYTHON_TOOLS installed directly from Git repositories
# Format: TOOL_NAME=GIT_URL=GIT_REF[=DEPENDENCIES_SUBDIR]
 # - TOOL_NAME: Matches the Python virtual environment name.
 # - GIT_URL: Git repository to clone.
 # - GIT_REF: Can be a commit hash, tag, or branch name to checkout.
 # - REQUIREMENTS_FILE (optional): Path (relative to repo root) to a requirements file (e.g., requirements.txt, requirements/requirements_2.txt).
 #      - If pyproject.toml or setup.py is present in the repo root, REQUIREMENTS_FILE should not be specified.
ARG GIT_TOOLS="pyrit[gcg]=https://github.com/Azure/PyRIT.git=v0.10.0rc0 cyberseceval=https://github.com/meta-llama/PurpleLlama.git=3494754=CybersecurityBenchmarks/requirements.txt lm-eval-harness[api]=https://github.com/EleutherAI/lm-evaluation-harness.git=v0.4.9.1 promptmap=https://github.com/utkusen/promptmap.git=9e1b4fe=requirements.txt fuzzyai=https://github.com/cyberark/FuzzyAI.git=2d1d4e6 easyedit=https://github.com/zjunlp/EasyEdit.git=da6f731=requirements_2.txt cleverhans=https://github.com/cleverhans-lab/cleverhans.git=574efc1=requirements/requirements.txt"

# Subset of PYTHON_TOOLS installed globally into the system Python environment
ARG SYSTEM_TOOLS="pyrit fickling rigging judges"

# Special-case Python tool lists for custom install logic
ARG TOOLS_WITH_TORCH_DEP="pyrit garak giskard lm-eval-harness fuzzyai easyedit"
ARG TOOLS_WITH_LEGACY_DEPS="easyedit adversarial-robustness-toolbox cleverhans"

# Node.js tools (JavaScript/TypeScript) installed via npm into separate project directories
ARG NODEJS_TOOLS="promptfoo==0.118.11"

# Self-contained CLI scripts integrated as standalone tools
ARG CUSTOM_TOOLS="biasforge"

# Stub CLI tools providing only a "--help" message redirecting to actively maintained equivalents
ARG STUB_TOOLS="llm-security-scripts gpt-fuzzer"

###############################################################################
#                         STAGE 1: BUILDER                                    #
###############################################################################
FROM ${BASE_IMAGE} AS builder

# Re-expose global ARGs
ARG package_index_url PYTHON_VERSION LEGACY_PYTHON_VERSION TORCH_INDEX_URL PYTHON_TOOLS SYSTEM_TOOLS GIT_TOOLS TOOLS_WITH_TORCH_DEP TOOLS_WITH_LEGACY_DEPS NODEJS_TOOLS STUB_TOOLS

# Set essential environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV VENV_BASE=/venvs

# ---------------------------------------------------------------------------- #
# Install System-Level Build Dependencies                                      #
# ---------------------------------------------------------------------------- #
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update && apt-get install -y --no-install-recommends \
       git \
       build-essential \
       nano \
       python3-venv \
       dos2unix \
       cmake \
       nodejs \
       patch \
    && rm -rf /var/lib/apt/lists/* \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && /usr/local/bin/pip install --index-url $package_index_url --no-cache-dir --upgrade --break-system-packages pip uv

ENV PATH="/root/.cargo/bin:${PATH}"

# ---------------------------------------------------------------------------- #
# Set Up Tools (Create Venvs, Download from PyPI, and Clone Git Repos)         #
# ---------------------------------------------------------------------------- #
RUN for tool in $PYTHON_TOOLS; do \
        TOOL_NAME=$(echo $tool | sed 's/\[.*\]//; s/==.*//'); \
        if echo "$SYSTEM_TOOLS" | grep -q "$TOOL_NAME"; then \
            echo "$TOOL_NAME should be installed globally, skipping venv creation"; \
            continue; \
        fi; \
        VENV_PATH="$VENV_BASE/$TOOL_NAME"; \
        if echo "$TOOLS_WITH_LEGACY_DEPS" | grep -q "$TOOL_NAME"; then \
            uv venv $VENV_PATH --python=python${LEGACY_PYTHON_VERSION}; \
        else \
            uv venv $VENV_PATH --python=python${PYTHON_VERSION}; \
        fi; \
    done \
    \
    # Download tools from PyPI
    && for tool in $PYTHON_TOOLS; do \
        TOOL_NAME=$(echo $tool | sed 's/\[.*\]//; s/==.*//'); \
        if echo "$GIT_TOOLS" | grep -q "$TOOL_NAME"; then \
            echo "$TOOL_NAME is a Git-based tool, skipping PyPI download"; \
            continue; \
        elif echo "$SYSTEM_TOOLS" | grep -q "$TOOL_NAME"; then \
            SRC_DIR="/opt/$TOOL_NAME"; \
        else \
            SRC_DIR="$VENV_BASE/$TOOL_NAME/source"; \
        fi; \
        mkdir -p $SRC_DIR && \
        pip download --index-url $package_index_url --no-cache-dir --no-deps --no-binary=$TOOL_NAME --dest $SRC_DIR $tool && \
        tar -xvf $SRC_DIR/*.tar.gz -C $SRC_DIR --strip-components=1 && \
        rm $SRC_DIR/*.tar.gz || true; \
    done \
    \
    # Clone Git-based tools
    && for tool in $GIT_TOOLS; do \
        TOOL_NAME=$(echo $tool | cut -d'=' -f1 | sed 's/\[.*\]//; s/==.*//'); \
        REPO_URL=$(echo $tool | cut -d'=' -f2); \
        GIT_REF=$(echo $tool | cut -d'=' -f3); \
        if echo "$SYSTEM_TOOLS" | grep -q "$TOOL_NAME"; then \
            CLONE_PATH="/opt/$TOOL_NAME"; \
        else \
            CLONE_PATH="$VENV_BASE/$TOOL_NAME/source"; \
        fi; \
        REPO_NAME=$(basename $REPO_URL .git); \
        git clone $REPO_URL $CLONE_PATH/$REPO_NAME || exit 1; \
        cd $CLONE_PATH/$REPO_NAME \
            && (git checkout "tags/$GIT_REF" 2>/dev/null || git checkout $GIT_REF) || exit 1; \
        rm -rf $CLONE_PATH/$REPO_NAME/.git; \
    done

# ---------------------------------------------------------------------------- #
# Apply Patches and Install Tools                                              #
# ---------------------------------------------------------------------------- #
COPY patches /patches
COPY global_requirements.txt /opt/global_requirements.txt
COPY torch_constraints /opt/torch_constraints

# Apply patches
RUN for tool in $PYTHON_TOOLS; do \
      TOOL_NAME=$(echo $tool | sed 's/\[.*\]//; s/==.*//'); \
      PATCH_DIR="/patches/$TOOL_NAME"; \
      echo "Processing tool: $TOOL_NAME"; \
      if echo "$SYSTEM_TOOLS" | grep -q "$TOOL_NAME"; then \
          SRC_DIR="/opt/$TOOL_NAME"; \
      else \
          SRC_DIR="$VENV_BASE/$TOOL_NAME/source"; \
      fi; \
      if [ -d "$SRC_DIR" ]; then \
          find "$SRC_DIR" -type f -name '*.py' -exec dos2unix {} \;; \
      fi; \
      if [ -d "$PATCH_DIR" ]; then \
          for diff_file in $(find "$PATCH_DIR" -type f -name '*.diff'); do \
              echo "Applying patch: $diff_file"; \
              patch -u -p0 -d "$SRC_DIR" -i "$diff_file" || (echo "ERROR: Failed applying patch $diff_file"; exit 1); \
          done; \
          for pyfile in $(find "$PATCH_DIR" -type f -name '*.py'); do \
              TARGET_PATH=$(grep '^# NEW_FILE_PATH:' "$pyfile" | head -1 | awk '{print $3}'); \
              if [ -n "$TARGET_PATH" ]; then \
                  mkdir -p "$(dirname \"$SRC_DIR/$TARGET_PATH\")"; \
                  echo "Adding file: $pyfile"; \
                  cp "$pyfile" "$SRC_DIR/$TARGET_PATH"; \
              else \
                  echo "ERROR: NEW_FILE_PATH not specified in $pyfile"; exit 1; \
              fi; \
          done; \
      fi; \
    done \
    && rm -rf /patches \
    \
    # Install Python tools
    && for tool in $PYTHON_TOOLS; do \
        TOOL_NAME=$(echo $tool | sed 's/\[.*\]//; s/==.*//'); \
        if echo "$SYSTEM_TOOLS" | grep -q "$TOOL_NAME"; then \
            IS_SYSTEM_TOOL=true; \
            TOOL_PATH="/opt/$TOOL_NAME"; \
        else \
            TOOL_PATH="$VENV_BASE/$TOOL_NAME"; \
            IS_SYSTEM_TOOL=false; \
        fi; \
        echo "Installing $TOOL_NAME to $TOOL_PATH"; \
        IS_GIT_TOOL=false; \
        for GIT_TOOL in $GIT_TOOLS; do \
            if echo "$GIT_TOOL" | grep -q "^$TOOL_NAME"; then \
                IS_GIT_TOOL=true; \
                GIT_TOOL_NAME=$(echo "$GIT_TOOL" | cut -d'=' -f1); \
                REPO_URL=$(echo "$GIT_TOOL" | cut -d'=' -f2); \
                REPO_COMMIT=$(echo "$GIT_TOOL" | cut -d'=' -f3); \
                REQUIREMENTS_FILE=$(echo "$GIT_TOOL" | cut -d'=' -f4); \        
                if [ "$IS_SYSTEM_TOOL" = true ]; then \
                    REPO_PATH="$TOOL_PATH/$(basename $REPO_URL .git)"; \
                else \
                    REPO_PATH="$TOOL_PATH/source/$(basename $REPO_URL .git)"; \
                fi; \
                if [ -n "$REQUIREMENTS_FILE" ]; then \
                    REQUIREMENTS_FILE="$REPO_PATH/$REQUIREMENTS_FILE"; \
                    if [ "$IS_SYSTEM_TOOL" = true ]; then \
                        if echo "$TOOLS_WITH_TORCH_DEP" | grep -q "$TOOL_NAME"; then \
                            uv pip install --no-cache-dir -r $REQUIREMENTS_FILE --system --break-system-packages --find-links=$TORCH_INDEX_URL -c /opt/torch_constraints/$TOOL_NAME.txt; \
                        else \
                            uv pip install --no-cache-dir -r $REQUIREMENTS_FILE --system --break-system-packages; \
                        fi; \
                    else \
                        if echo "$TOOLS_WITH_TORCH_DEP" | grep -q "$TOOL_NAME"; then \
                            uv pip install --no-cache-dir -r $REQUIREMENTS_FILE --python $TOOL_PATH/bin/python --find-links=$TORCH_INDEX_URL -c /opt/torch_constraints/$TOOL_NAME.txt; \
                        else \
                            uv pip install --no-cache-dir -r $REQUIREMENTS_FILE --python $TOOL_PATH/bin/python; \
                        fi; \
                    fi; \
                elif [ -f "$REPO_PATH/pyproject.toml" ] || [ -f "$REPO_PATH/setup.py" ]; then \
                    EXTRAS=$(echo "$GIT_TOOL_NAME" | grep -oP '\[.*?\]' | tr -d '[]'); \
                    if [ -n "$EXTRAS" ]; then \
                        INSTALL_TARGET=".[$EXTRAS]"; \
                    else \
                        INSTALL_TARGET="."; \
                    fi; \ 
                    if [ "$IS_SYSTEM_TOOL" = true ]; then \
                        if echo "$TOOLS_WITH_TORCH_DEP" | grep -q "$TOOL_NAME"; then \
                            cd $REPO_PATH && uv pip install --no-cache-dir $INSTALL_TARGET --system --break-system-packages --find-links=$TORCH_INDEX_URL -c /opt/torch_constraints/$TOOL_NAME.txt; \
                        else \
                            cd $REPO_PATH && uv pip install --no-cache-dir $INSTALL_TARGET --system --break-system-packages; \
                        fi; \
                    else \
                        if echo "$TOOLS_WITH_TORCH_DEP" | grep -q "$TOOL_NAME"; then \
                            cd $REPO_PATH && uv pip install --no-cache-dir $INSTALL_TARGET --python $TOOL_PATH/bin/python --find-links=$TORCH_INDEX_URL -c /opt/torch_constraints/$TOOL_NAME.txt; \
                        else \
                            cd $REPO_PATH && uv pip install --no-cache-dir $INSTALL_TARGET --python $TOOL_PATH/bin/python; \
                        fi; \
                    fi; \
                else \
                    echo "REQUIREMENTS_FILE not specified and pyproject.toml not found in $REPO_PATH!"; exit 1; \
                fi; \
                break; \
            fi; \
        done; \
        if [ "$IS_GIT_TOOL" = false ]; then \
            # Handle optional dependencies (e.g., giskard[llm])
            EXTRAS=$(echo "$tool" | grep -oP '\[.*?\]' | tr -d '[]'); \
            if [ "$IS_SYSTEM_TOOL" = true ]; then \
                if [ -n "$EXTRAS" ]; then \
                    INSTALL_TARGET="$TOOL_PATH[$EXTRAS]"; \
                else \
                    INSTALL_TARGET="$TOOL_PATH"; \
                fi; \
                if echo "$TOOLS_WITH_TORCH_DEP" | grep -q "$TOOL_NAME"; then \
                    uv pip install --no-cache-dir "$INSTALL_TARGET" --system --break-system-packages --find-links=$TORCH_INDEX_URL -c /opt/torch_constraints/$TOOL_NAME.txt; \
                else \
                    uv pip install --no-cache-dir "$INSTALL_TARGET" --system --break-system-packages; \
                fi; \
                rm -rf /opt/$TOOL_NAME; \
            else \
                if [ -n "$EXTRAS" ]; then \
                    INSTALL_TARGET="$TOOL_PATH/source[$EXTRAS]"; \
                else \
                    INSTALL_TARGET="$TOOL_PATH/source"; \
                fi; \
                if echo "$TOOLS_WITH_TORCH_DEP" | grep -q "$TOOL_NAME"; then \
                    uv pip install --no-cache-dir "$INSTALL_TARGET" --python "$TOOL_PATH/bin/python" --find-links=$TORCH_INDEX_URL -c /opt/torch_constraints/$TOOL_NAME.txt; \
                else \
                    uv pip install --no-cache-dir "$INSTALL_TARGET" --python "$TOOL_PATH/bin/python"; \
                fi; \
                rm -rf "$TOOL_PATH/source"; \
            fi; \
        fi; \
    done \
    \
    # Install typer in Python virtual envs
    && TYPER_VERSION=$(grep '^typer==' /opt/global_requirements.txt | cut -d'=' -f3 || true) && \
        CLICK_VERSION=$(grep '^click==' /opt/global_requirements.txt | cut -d'=' -f3 || true) && \
    if [ -n "$TYPER_VERSION" ]; then \
      for tool in $PYTHON_TOOLS; do \
          TOOL_NAME=$(echo $tool | sed 's/\[.*\]//; s/==.*//'); \
          if echo "$SYSTEM_TOOLS" | grep -q "$TOOL_NAME"; then \
            echo "$TOOL_NAME is installed globally, skipping typer installation"; \
            continue; \
          fi; \
          VENV_PATH="$VENV_BASE/$TOOL_NAME"; \
          if ! $VENV_PATH/bin/python -c "import typer" &>/dev/null; then \
            uv pip install --no-cache-dir typer==$TYPER_VERSION click==$CLICK_VERSION --python $VENV_PATH/bin/python; \
          fi; \
      done \
    fi \
    \
    # Install global requirements to system-level Python environment
    && if [ -s /opt/global_requirements.txt ]; then \
        uv pip install --no-cache-dir --system -r /opt/global_requirements.txt --break-system-packages --find-links=$TORCH_INDEX_URL; \
    else \
        echo "global_requirements.txt is empty, skipping installation"; \
    fi \
    && rm /opt/global_requirements.txt \
    \
    # Install Node.js tools in /venvs
    && for tool in $NODEJS_TOOLS; do \
        TOOL_NAME=$(echo $tool | sed 's/==.*//'); \
        TOOL_VERSION=$(echo $tool | sed 's/.*==//'); \
        TOOL_VENV="$VENV_BASE/$TOOL_NAME"; \
        mkdir -p $TOOL_VENV && cd $TOOL_VENV && npm init -y && \
        npm install "$TOOL_NAME@$TOOL_VERSION" && \
        npm cache clean --force || true; \
    done \
    \
    # Final cleanup of caches
    && rm -rf /root/.cargo/registry \
              /root/.cargo/git \
              /root/.rustup/tmp \
              /root/.rustup/downloads \
              /root/.cache/pip \
              /root/.cache/uv \
              /root/.cache/npm \
              /root/.npm \
              /tmp/*


###############################################################################
#                         STAGE 2: FINAL                                      #
###############################################################################
FROM ${BASE_IMAGE} AS final

# Re-expose global ARGs
ARG package_index_url PYTHON_VERSION PYTHON_TOOLS SYSTEM_TOOLS GIT_TOOLS NODEJS_TOOLS CUSTOM_TOOLS STUB_TOOLS

# Set essential environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV VENV_BASE=/venvs

# Copy from builder
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/dist-packages/ /usr/local/lib/python${PYTHON_VERSION}/dist-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /root/.local/share/ /root/.local/share/
COPY --from=builder $VENV_BASE $VENV_BASE
COPY --from=builder /opt /opt

# Copy from repo
COPY global_requirements.txt /opt/global_requirements.txt
COPY torch_constraints /opt/torch_constraints
COPY cli_scripts /opt/cli_scripts

# ---------------------------------------------------------------------------- #
# Install final-stage OS dependencies, remove conflicting Python packages from #
# /databricks venv, create CLI script symlinks, and modify PYTHONPATH          #
# ---------------------------------------------------------------------------- #
RUN apt-get update && apt-get install -y --no-install-recommends curl nano vim \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends figlet nodejs libgl1 libglib2.0-0\
    && rm -rf /var/lib/apt/lists/* \
    && pip install --index-url $package_index_url --no-cache-dir --upgrade --break-system-packages pip uv \
    \
    # Remove conflcting packages from /databricks virtual env
    && for pkg in $(awk -F'[=<>]' '{print $1}' /opt/global_requirements.txt | grep -vE '^#|^$'); do \
        uv pip uninstall $pkg --python /databricks/python3/bin/python || true; \
    done \
    # Create symlinks for CLI scripts
    && for tool in ${PYTHON_TOOLS} ${NODEJS_TOOLS} ${CUSTOM_TOOLS} ${STUB_TOOLS} ; do \
        TOOL_NAME=$(echo $tool | sed 's/\[.*\]//; s/==.*//'); \
        SCRIPT_PATH="/opt/cli_scripts/$TOOL_NAME"; \     
        if [ ! -f "$SCRIPT_PATH" ]; then \
            if echo "${SYSTEM_TOOLS} ${STUB_TOOLS}" | sed "s/==[^ ]*//g" | grep -q "${TOOL_NAME}"; then \
                echo "Warning: CLI script $SCRIPT_PATH not found for $TOOL_NAME; skipping symlink creation."; continue; \
            elif echo "${PYTHON_TOOLS}" | sed "s/==[^ ]*//g" | grep -q "${TOOL_NAME}"; then \
                echo "ERROR: Missing CLI script for '$TOOL_NAME' at $SCRIPT_PATH."; \
                echo "All non-system PYTHON_TOOLS need a CLI script using the right Python interpreter (see /docker/cli_scripts/garak for a minimal example)."; \
                exit 1; \
            elif echo "${NODEJS_TOOLS}" | sed "s/==[^ ]*//g" | grep -q "${TOOL_NAME}"; then \
                ln -s $VENV_BASE/"$TOOL_NAME"/node_modules/.bin/"$TOOL_NAME" /usr/local/bin/"$TOOL_NAME"; \
            else \
                echo "ERROR: tool $TOOL_NAME not assigned to category"; exit 1; \
            fi; \
        else \
            ln -s "$SCRIPT_PATH" /usr/local/bin/"$TOOL_NAME" && chmod +x "$SCRIPT_PATH"; \
        fi; \
    done \
    \
    # For GIT_TOOLS installed via requirements file (i.e., not pip-installable packages),
    # add the repo root to PYTHONPATH or a .pth file so Python can import any top-level packages.
    && for GIT_TOOL in $GIT_TOOLS; do \
        TOOL_NAME=$(echo "$GIT_TOOL" | cut -d'=' -f1 | sed 's/\[.*\]//; s/==.*//'); \
        REPO_URL=$(echo "$GIT_TOOL" | cut -d'=' -f2); \
        REPO_NAME=$(basename "$REPO_URL" .git); \
        REQUIREMENTS_FILE=$(echo "$GIT_TOOL" | cut -d'=' -f4); \
        if [ -n "$REQUIREMENTS_FILE" ]; then \
            if echo "$SYSTEM_TOOLS" | grep -q "$TOOL_NAME"; then \
                # Make packages importable for system Python
                echo "/opt/$TOOL_NAME/$REPO_NAME" > "/usr/local/lib/python${PYTHON_VERSION}/dist-packages/$TOOL_NAME.pth"; \
            else \
                # Make packages importable when venv is activated
                VENV_PATH="$VENV_BASE/$TOOL_NAME"; \
                echo "PYTHONPATH=\"$VENV_PATH/source/$REPO_NAME:\$PYTHONPATH\"" >> "$VENV_PATH/bin/activate"; \
                echo "export PYTHONPATH" >> "$VENV_PATH/bin/activate"; \
            fi; \
        fi; \
    done

# ---------------------------------------------------------------------------- #
# Final Setup                                                                  #
# ---------------------------------------------------------------------------- #
WORKDIR /workspace

RUN figlet "BLACKICE" > /etc/motd \
    && echo "Welcome to the BLACKICE Docker Image!\n" >> /etc/motd \
    && echo "To get started, try out one of the following tools with --help:\n" >> /etc/motd \
    && echo "  lm-eval-harness                  [Academic benchmarks for LLMs]" >> /etc/motd \
    && echo "  promptfoo                        [General purpose LLM security tool]" >> /etc/motd \
    && echo "  garak                            [LLM Vulnerability Scanner with static corpus]" >> /etc/motd \
    && echo "  giskard                          [LLM Vulnerability Scanner with dynamic corpus]" >> /etc/motd \
    && echo "  cyberseceval                     [Benchmark to evaluate cybersecurity vulnerabilities in LLMs]" >> /etc/motd \
    && echo "  promptmap                        [Prompt Injection attack scanner]" >> /etc/motd \
    && echo "  fuzzyai                          [Automated fuzzing framework for LLMs]\n" >> /etc/motd \
    && echo "OR import one of the following libraries in Python:\n" >> /etc/motd \
    && echo "  pyrit                            [Open source framework for AI red teaming]" >> /etc/motd \
    && echo "  fickling                         [Pickle object scanner (includes CLI support)]" >> /etc/motd \
    && echo "  rigging                          [Flexible LLM library by dreadnode]" >> /etc/motd \
    && echo "  judges                           [Let LLMs judge the outcome of other LLMs (LLM-as-a-judge)]" >> /etc/motd \
    && echo "  easyedit                         [Knowledge editing framework for LLMs]" >> /etc/motd \
    && echo "  adversarial-robustness-toolbox   [Evaluate adversarial threats for classical machine learning]" >> /etc/motd \
    && echo "  cleverhans                       [Adversarial examples for classic machine learning]" >> /etc/motd

CMD ["/bin/bash", "-c", "cat /etc/motd && /bin/bash"]
