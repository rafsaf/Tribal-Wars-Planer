
ESBUILD_VERSION=https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.21.4.tgz
ESBUILD_PATH=./bin/esbuild

.PHONY: up
up:
	docker compose up -d postgres_dev
	poetry run python manage.py migrate
	DJANGO_SUPERUSER_PASSWORD=admin poetry run python manage.py createsuperuser --noinput --username admin --email admin@admin.admin || true
	poetry run python manage.py runserver

.PHONY: run
run: up

.PHONY: trans
trans:
	docker compose -f docker-compose.translation.yml run --build --rm trans

bin/esbuild:
	mkdir -p ./bin
	mkdir /tmp/esbuild
	wget -qO- ${ESBUILD_VERSION} | tar xvz -C /tmp/esbuild
	cp /tmp/esbuild/package/bin/esbuild ${ESBUILD_PATH}
	rm -rf /tmp/esbuild

.PHONY: watch
watch: bin/esbuild
	./bin/esbuild --minify --entry-names="[dir]/min.[name]" --watch --outdir=./base/static ./base/static/base.js ./base/static/base.css

.PHONY: to_avif
to_avif:
	# sudo apt install imagemagick
	find base -type f -regex ".*\.\(jpg\|jpeg\|png\)" -exec convert -format avif {}  \; -print
	find base -type f -regex ".*\.\(jpg\|jpeg\|png\)" -exec rm {}  \; -print
	
.PHONY: docs_serve_pl
docs_serve_pl:
	poetry run mkdocs serve -f docs/config/pl/mkdocs.yml
	
.PHONY: docs_build_pl
docs_build_pl:
	poetry run mkdocs build -f docs/config/pl/mkdocs.yml

.PHONY: docs_serve_en
docs_serve_en:
	poetry run mkdocs serve -f docs/config/en/mkdocs.yml

.PHONY: docs_build_en
docs_build_en:
	poetry run mkdocs build -f docs/config/en/mkdocs.yml

.PHONY: build_cython
build_cython:
	poetry run python setup.py build_ext --inplace

.PHONY: test
test:
	poetry run pytest -v --cov --cov-report xml --cov-report term-missing -n auto 

.PHONY: benchmark
benchmark:
	poetry run pytest --codspeed

.PHONY: debug_available_troops
debug_available_troops:
	poetry run python -m cProfile -o debug_available_troops.prof manage.py debug_available_troops 3
	poetry run snakeviz debug_available_troops.prof

