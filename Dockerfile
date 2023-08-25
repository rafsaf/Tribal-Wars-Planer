FROM python:3.11.4-bookworm as base

ENV PYTHONUNBUFFERED 1
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

RUN apt-get update && apt-get install -y python3-pip nginx postgresql-client

FROM base as poetry
RUN pip install poetry==1.5.1
COPY poetry.lock pyproject.toml ./
RUN poetry export -o /requirements.txt --without-hashes

FROM base AS build
COPY --from=poetry /requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get remove -y python3-pip && apt-get autoremove --purge -y        \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list
COPY ./config/twp_nginx.conf /etc/nginx/nginx.conf
COPY . .
RUN chown -R ${SERVICE_NAME}:${SERVICE_NAME} /build
CMD bash /build/scripts/init_webserver.sh

FROM build as translations
RUN apt-get update -y && apt-get install gettext -y
CMD python manage.py makemessages --all --ignore .venv &&  \
    python manage.py compilemessages --ignore .venv