FROM python:3.10

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN python -m venv .venv
RUN .venv/bin/pip install .

CMD [".venv/bin/python", "-m", "sssimp"]
