FROM python:3.11-slim-bullseye AS base
WORKDIR /app

FROM base AS build
COPY ["requirements.txt", "./"]
RUN \
  apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    git && \
  rm -rf /var/lib/apt/lists/* ./venv && \
  # Install dependencies.
  python -m venv ./venv && \
  ./venv/bin/pip install --upgrade \
    pip \
    setuptools \
    wheel && \
  ./venv/bin/pip install --no-cache-dir -r ./requirements.txt

FROM base AS final
COPY --from=build ["/app/venv", "./venv"]
# Copy the source code in last to optimize rebuilding the image.
COPY [".", "./"]
ENTRYPOINT \
  # Start the server.
  ./venv/bin/python -m streamlit run src/homepage.py
