FROM gitpod/workspace-full

USER gitpod

# Best practices for apt-get to prevent caching issues and reduce image layers
RUN sudo apt-get update \
    && sudo apt-get install -y ruby-full \
    && sudo rm -rf /var/lib/apt/lists/*

# Install vsce globally
RUN npm install --global vsce

# Install specific Python version using pyenv and set it as global default
RUN pyenv install 3.12.1 \
    && pyenv global 3.12.1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Install github-changelog-generator
RUN sudo  gem install github_changelog_generator

# Ensure the Poetry and pyenv bin directories are in the PATH
ENV PATH="/home/gitpod/.pyenv/shims:/home/gitpod/.pyenv/bin:$PATH:/home/gitpod/.local/bin"
