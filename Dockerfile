FROM python:3.12-slim

RUN pip install uv --no-cache-dir

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev

COPY src/ ./src/

ENV EXCEL_FILES_PATH=/data \
    FASTMCP_PORT=8017 \
    FASTMCP_HOST=0.0.0.0

EXPOSE 8017
VOLUME ["/data"]

CMD ["uv", "run", "excel-mcp-server", "streamable-http"]
