FROM quay.io/centos/centos:stream8

# Import keys to suppress warnings about GPG-keys
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial \
    && rpm --import https://packages.microsoft.com/keys/microsoft.asc

# Minimal:
# WARNING! Lower security by enabling TLSv1 and TLSv1.1
# Docs: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/considerations_in_adopting_rhel_8/security_considerations-in-adopting-rhel-8#tls-v10-v11_security
RUN dnf install -y \
    java-1.8.0-openjdk \
    sudo \
    procps \
    && update-ca-trust \
    && update-crypto-policies --set LEGACY

# Clean-up:
RUN dnf clean all \
      && rm -rf /tmp/* /var/tmp/*
