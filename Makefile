
ESBUILD_VERSION=https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.21.4.tgz
ESBUILD_PATH=./bin/esbuild

bin/esbuild:
	mkdir -p ./bin
	mkdir /tmp/esbuild
	wget -qO- ${ESBUILD_VERSION} | tar xvz -C /tmp/esbuild
	cp /tmp/esbuild/package/bin/esbuild ${ESBUILD_PATH}
	rm -rf /tmp/esbuild

.PHONY: watch
watch: bin/esbuild
	./bin/esbuild --minify --entry-names="[dir]/min.[name]" --watch --outdir=./base/static ./base/static/base.js ./base/static/base.css
