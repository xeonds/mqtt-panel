FROM ubuntu:latest

WORKDIR /app

COPY mqtt-panel-linux-amd64-0.1.0 /app/
COPY ./dist /app/dist

EXPOSE 8765

CMD ["./mqtt-panel-linux-amd64-0.1.0"]

