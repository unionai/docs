---
title: Domains
weight: 2
variants: +flyte -serverless -byoc -selfmanaged
---

# Domains
Domains are fixed and unique at the global level, and provide an abstraction to isolate resources and feature configuration for different deployment environments.

For example: We develop and deploy Flyte workflows in development, staging, and production. We configure Flyte domains with those names, and specify lower resource limits on the development and staging domains than production domains.

We also use domains to disable launch plans and schedules from development and staging domains, since those features are typically meant for production deployments.