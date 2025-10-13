FROM ghcr.io/actions/actions-runner:2.328.0

# Install other dependencies
RUN sudo apt update -y && \
    sudo apt install -y --no-install-recommends \
    build-essential

# Copy tool-cache
RUN mkdir -p /home/runner/_work/_tool
COPY --chown=runner:runner tool-cache /home/runner/_work/_tool
