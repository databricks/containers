# CAMLIS Demo Notebook

## Overview

This demo notebook was presented at CAMLIS 2025 (Conference on Applied Machine Learning for Information Security). It demonstrates how BlackICE can be used to orchestrate multiple security evaluation tools to assess AI model vulnerabilities.
Specifically, we demonstrate testing for Prompt Injections and Jailbreaks using the tools Garak, Promptmap, CyberSecEval, and FuzzyAI.
While this demo uses a Databricks environment, the approach is generally applicable. The collection of tools and attack categories shown here is not exhaustive, but aims to illustrate the flexibility that BlackICE provides for security tool orchestration.

## Workflow
1. Selects a target LLM from Databricks foundation model endpoints
2. Loads attack configurations from a JSON setup file
3. Executes each attack using the appropriate security testing tool
4. Collects success rates for each attack type
