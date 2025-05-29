---
title: Cloud image builder
weight: 2
variants: -flyte +serverless +byoc +selfmanaged
---

## Cloud image builder

When `builder="union"` is specified in an `ImageSpec`, {{< key product_name >}} will build the image using its `ImageBuilder` service in the cloud and registered, either in the in {{< key product_name >}}'s own internal container registry (the default) or if a
If no `registry` parameter is supplied, the resulting image will be registered

If a `registry` parameter is supplied, then

From there it will be pulled and installed in the task container when it spins up.
All this is done transparently and does not require any set up by the user.

