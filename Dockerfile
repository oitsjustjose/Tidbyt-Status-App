FROM python:3.10-slim-bookworm

RUN apt-get update && apt-get upgrade -y

COPY . .
RUN pip install -r src/server/requirements.txt

CMD ["fastapi", "run", "src/server/main.py"]