# temp stage
FROM --platform=linux/amd64 python:3.12.3-slim as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# RUN apt-get update && apt-get install -y git

# Install dependencies
# RUN pip3 install --upgrade pip

RUN pip install uv
RUN uv venv /opt/venv

# Add our code
ADD . /app
WORKDIR /app

RUN . /opt/venv/bin/activate && uv pip install .

# final stage
FROM --platform=linux/amd64 python:3.12.3-slim

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/key.key /app/key.key

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"
RUN . /opt/venv/bin/activate

# Run the image as a non-root user
RUN useradd -m myuser
RUN chown myuser:myuser -R /app
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD python3 -m blueshed.crypto.main
