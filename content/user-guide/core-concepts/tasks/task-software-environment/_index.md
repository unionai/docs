---
title: Task software environment
weight: 6
variants: +flyte -serverless +byoc +selfmanaged
sidebar_expanded: false
---

# Task software environment

The @{{< key kit_as >}}.task decorator provides the following parameters to specify the software environment in which a task runs:

* `container_image`: Can be either a string referencing a specific image on a container repository, or an ImageSpec defining a build. See [ImageSpec](./image-spec) for details.
* `environment`: See [Environment](./environment-variables) for details.
