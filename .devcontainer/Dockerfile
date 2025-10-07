# Use the official Microsoft DevContainer base image with Python and Node.js
FROM mcr.microsoft.com/devcontainers/python:1-3.11

# Install Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install additional development tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        git \
        curl \
        wget \
        vim \
        nano \
        htop \
        tree \
        jq \
        sqlite3 \
        build-essential \
        pkg-config \
        libffi-dev \
        libssl-dev \
        python3-dev \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install global npm packages for development
RUN npm install -g nodemon concurrently

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user if it doesn't exist
RUN if ! id -u $USERNAME > /dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
        && apt-get update \
        && apt-get install -y sudo \
        && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
        && chmod 0440 /etc/sudoers.d/$USERNAME; \
    fi

# Set up Python environment for the user
USER $USERNAME
RUN python3 -m pip install --user --upgrade pip setuptools wheel

# Install common Python development tools
RUN python3 -m pip install --user \
    black \
    flake8 \
    isort \
    pylint \
    pytest \
    pytest-cov

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Set working directory
WORKDIR /workspace

# Switch back to root for any final setup
USER root

# Set the default user back to vscode
USER $USERNAME