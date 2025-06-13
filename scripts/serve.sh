#!/bin/bash

declare port=${PORT:-9000}
declare launch=${LAUNCH:-1}


if [[ $launch -eq 1 ]]; then
  cat <<EOF
------------------
Opening browser @ http://localhost:${port}
------------------
EOF
  open "http://localhost:${port}"
else
  cat <<EOF
------------------
Open browser @ http://localhost:${port}
------------------
EOF
fi

if ! command -v caddy 1>/dev/null; then
  cat <<EOF
---------------------------------------
FATAL: 'caddy' web server required.

Install with:
  MacOS  : brew install caddy
  Ubuntu : apt  install caddy
---------------------------------------

EOF
  exit 1
fi

caddy run --config scripts/Caddyfile --watch
