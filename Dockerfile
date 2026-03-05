FROM python:3.12-slim
RUN pip install uv
WORKDIR /app
COPY . .
RUN uv sync
EXPOSE 7860
CMD sh -c "uv run init.py --reset && uvicorn main:app --port 7860"