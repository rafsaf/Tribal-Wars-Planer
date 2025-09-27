FROM python:3.13.7-bookworm AS base

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

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y python3-pip nginx postgresql-client

FROM base AS poetry
RUN --mount=type=cache,target=/root/.cache/pip pip install poetry==2.0.1
RUN --mount=type=cache,target=/root/.cache/pip poetry self add poetry-plugin-export
COPY poetry.lock pyproject.toml ./
RUN poetry export -o  /requirements.txt --without-hashes --without="dev" --without="docs"
RUN poetry export -o /requirements-docs.txt --without-hashes --only="docs"

FROM base AS docs
COPY docs docs
COPY --from=poetry /requirements-docs.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements-docs.txt
RUN mkdocs build -f docs/config/pl/mkdocs.yml
RUN mkdocs build -f docs/config/en/mkdocs.yml
RUN mkdocs build -f docs/config/hu/mkdocs.yml
RUN mkdocs build -f docs/config/pt-br/mkdocs.yml
RUN mkdocs build -f docs/config/cs/mkdocs.yml

FROM base AS build
COPY --from=docs /build/generated_docs generated_docs
COPY --from=poetry /requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY base base
COPY config/twp_nginx.conf /etc/nginx/nginx.conf
COPY locale locale
COPY manage.py .
COPY metrics metrics
COPY pyproject.toml .
COPY rest_api rest_api
COPY scripts scripts
COPY LICENSE .
COPY templates templates
COPY tribal_wars_planer tribal_wars_planer
COPY utils utils
COPY setup.py setup.py
COPY shipments shipments

RUN python setup.py build_ext --inplace
RUN rm utils/write_ram_target.py
RUN rm utils/write_noble_target.py

RUN chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build
CMD /build/scripts/init_webserver.sh
EXPOSE 80
EXPOSE 8050

FROM base AS translations
COPY --from=poetry /requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN apt-get update -y && apt-get install gettext -y
CMD python manage.py makemessages --all --ignore .venv &&  \
    python manage.py compilemessages --ignore .venv