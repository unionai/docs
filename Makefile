include makefile.inc

PREFIX := $(if $(VERSION),docs/$(VERSION),docs)
PORT := 9000
BUILD := $(shell date +%s)

.PHONY: all dist variant dev update-examples sync-examples

all: usage

usage:
	@./scripts/make_usage.sh

base:
	@if ! ./scripts/pre-build-checks.sh; then exit 1; fi
	@if ! ./scripts/pre-flight.sh; then exit 1; fi
	rm -rf dist
	mkdir -p dist
	mkdir -p dist/docs
	cat index.html.tmpl | sed 's#@@BASE@@#/${PREFIX}#g' > dist/index.html
	cat index.html.tmpl | sed 's#@@BASE@@#/${PREFIX}#g' > dist/docs/index.html
	#cp -R static/* dist/${PREFIX}/

dist: base
	make variant VARIANT=flyte
	make variant VARIANT=serverless
	make variant VARIANT=byoc
	make variant VARIANT=selfmanaged

variant:
	@if [ -z ${VARIANT} ]; then echo "VARIANT is not set"; exit 1; fi
	@VERSION=${VERSION} ./scripts/run_hugo.sh --config hugo.toml,hugo.site.toml,hugo.ver.toml,config.${VARIANT}.toml --destination dist/${VARIANT}
	@VERSION=${VERSION} VARIANT=${VARIANT} PREFIX=${PREFIX} BUILD=${BUILD} ./scripts/gen_404.sh

dev:
	@if ! ./scripts/pre-flight.sh; then exit 1; fi
	@if ! ./scripts/dev-pre-flight.sh; then exit 1; fi
	rm -rf public
	hugo server --config hugo.toml,hugo.site.toml,hugo.ver.toml,hugo.dev.toml,hugo.local.toml

serve:
	@if [ ! -d dist ]; then "echo Run `make dist` first"; exit 1; fi
	@PORT=${PORT} LAUNCH=${LAUNCH} ./scripts/serve.sh

update-examples:
	git submodule update --remote

init-examples:
	git submodule update --init

check-jupyter:
	./tools/jupyter_generator/check_jupyter.sh

check-images:
	./scripts/check_images.sh
