# Use the specified image for standalone Chromium
FROM seleniarm/standalone-chromium:latest

# Set shared memory size
# This can be done by setting runtime options when you run the container,
# because Dockerfile doesn't support shm_size configuration directly.

# Set environment variables
ENV SE_VNC_NO_PASSWORD=1 \
    SE_NODE_OVERRIDE_MAX_SESSIONS=true \
    SE_NODE_MAX_SESSIONS=10 \
    SE_SESSION_REQUEST_TIMEOUT=1000

# Entry point is already defined in the base image to start Selenium