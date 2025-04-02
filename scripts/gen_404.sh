#!/bin/bash

# This script generates a 404.html file for the website.

ensure_var() {
    local var_name="$1"
    local var_value="${!var_name}"

    if [[ -z "$var_value" ]]; then
        echo "Error: Environment variable $var_name is not set."
        exit 1
    fi
}

# Ensure required environment variables are set
ensure_var "PREFIX"
ensure_var "VARIANT"
ensure_var "BUILD"

declare source

if [[ -e "404.html.tmpl~${VARIANT}" ]]; then
    source="404.html.tmpl~${VARIANT}"
else
    source="404.html.tmpl"
fi

readonly source

sed \
    -e "s#@@BASE@@#/${PREFIX}#g" \
    -e "s#@@VARIANT@@#${VARIANT}#g" \
    -e "s#@@BUILD@@#${BUILD}#g" \
    > "dist/docs/${VARIANT}/404.html" \
    < "${source}"

if [[ $? -ne 0 ]]; then
    echo "Error generating 404.html"
    exit 1
fi
