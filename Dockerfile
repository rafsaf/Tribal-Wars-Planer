FROM python:3.14.0-trixie AS base

ENV PYTHONUNBUFFERED=1
ENV PROMETHEUS_MULTIPROC_DIR=prometheus_multi_proc_dir
ENV UWSGI_PROCESSES=1
ENV UWSGI_THREADS=1
ENV SERVICE_NAME=uwsgi

RUN mkdir build
WORKDIR /build

RUN addgroup --gid 2222 --system ${SERVICE_NAME} && \
    adduser --gid 2222 --shell /bin/false --disabled-password --uid 2222 ${SERVICE_NAME}

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

FROM base AS uv
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /uvx /bin/
COPY uv.lock pyproject.toml ./
RUN uv export --no-dev --no-group docs --no-hashes -o /requirements.txt --no-install-workspace --frozen
RUN uv export --only-group docs --no-hashes -o /requirements-docs.txt --no-install-workspace --frozen

FROM base AS docs
COPY docs docs
COPY --from=uv /requirements-docs.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements-docs.txt
RUN mkdocs build -f docs/config/pl/mkdocs.yml
RUN mkdocs build -f docs/config/en/mkdocs.yml
RUN mkdocs build -f docs/config/hu/mkdocs.yml
RUN mkdocs build -f docs/config/pt-br/mkdocs.yml
RUN mkdocs build -f docs/config/cs/mkdocs.yml
RUN mkdocs build -f docs/config/de/mkdocs.yml

FROM base AS build
COPY --from=docs /build/generated_docs generated_docs
COPY --from=uv /requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} base base
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} locale locale
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} manage.py .
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} metrics metrics
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} pyproject.toml .
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} rest_api rest_api
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} scripts scripts
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} LICENSE .
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} templates templates
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} tribal_wars_planer tribal_wars_planer
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} utils utils
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} setup.py setup.py
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} shipments shipments
COPY --chown=${SERVICE_NAME}:${SERVICE_NAME} generated_docs generated_docs

RUN python setup.py build_ext --inplace
RUN rm utils/write_ram_target.py
RUN rm utils/write_noble_target.py

RUN python -m compileall -b /build/base /build/rest_api /build/utils /build/shipments /build/metrics /build/tribal_wars_planer
# Run collectstatic with minimal required env vars for Django to start
RUN SECRET_KEY=build-time-secret \
    POSTGRES_NAME=postgres \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres \
    POSTGRES_HOST=localhost \
    POSTGRES_PORT=5432 \
    python manage.py collectstatic --no-input

RUN apt-get update -y && apt-get install -y nginx postgresql-client
COPY config/twp_nginx.conf /etc/nginx/nginx.conf

CMD /build/scripts/init_webserver.sh
EXPOSE 80
EXPOSE 8050

FROM base AS translations
COPY --from=uv /requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN apt-get update -y && apt-get install gettext -y
CMD python manage.py makemessages --all --ignore .venv &&  \
    python manage.py compilemessages --ignore .venv