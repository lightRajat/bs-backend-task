FROM python:3.12-slim
RUN pip install uv
WORKDIR /app
COPY . .
RUN uv sync
EXPOSE 8000
CMD sh -c "uv run init.py --reset && uv run main.py"