FROM python:3.12-slim
RUN pip install uv
WORKDIR /app
COPY . .
RUN uv sync
RUN uv run init.py --reset
EXPOSE 8000
CMD ["uv", "run", "main.py"]