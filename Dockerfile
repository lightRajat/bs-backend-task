FROM python:3.12-slim
RUN pip install uv
WORKDIR /app
COPY . .
RUN uv sync
EXPOSE 7860
CMD sh -c "uv run init.py && uv run uvicorn main:app --host 0.0.0.0 --port 7860"