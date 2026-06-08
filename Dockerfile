# Containerize the registry agent's HTTP surface. Minimal, no secrets baked in.
FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir cryptography

COPY autonomyx/ ./autonomyx/
COPY agentweb/ ./agentweb/

ENV PORT=8080
EXPOSE 8080

# Non-root user (least privilege)
RUN useradd -m -u 10001 agent
USER agent

CMD ["python", "-m", "agentweb.http_server"]
