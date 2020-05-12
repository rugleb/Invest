FROM python:3.7-buster as builder

COPY . .

RUN pip install -U --no-cache-dir pip wheel setuptools poetry && \
    poetry build -f wheel && \
    poetry export -f requirements.txt -o requirements.txt --without-hashes && \
    pip wheel -w dist -r requirements.txt


FROM python:3.7-slim-buster as runtime

WORKDIR /usr/src/app

ENV PYTHONOPTIMIZE 1

COPY --from=builder dist dist
COPY --from=builder gunicorn.config.py ./

RUN pip install --no-cache-dir --no-index dist/*.whl && \
    rm -rf dist

RUN useradd -r -UM app
USER app

CMD ["gunicorn", "invest_api:create_app", "-c", "gunicorn.config.py"]
