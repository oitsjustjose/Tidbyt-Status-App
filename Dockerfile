FROM python:3.10-slim-bookworm

RUN apt-get update && apt-get upgrade -y
# RUN apt-get install libc6

COPY . .
RUN pip install -r requirements.txt

CMD ["fastapi", "run", "src/server/main.py"]