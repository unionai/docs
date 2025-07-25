---
title: API Key Authentication with FastAPI
weight: 3
variants: -flyte +serverless +byoc +selfmanaged
---

# API Key Authentication with FastAPI

In this guide, we'll deploy a FastAPI app that uses API key authentication. This
allows you to invoke the endpoint from the public internet in a secure manner.

## Define the Fast API app

First we define the `ImageSpec` for the runtime image:

```python
import os
from union import ImageSpec, Resources, Secret
from union.app import App

image_spec = ImageSpec(
    name="fastapi-with-auth-image",
    builder="union",
    packages=["union-runtime>=0.1.11", "fastapi[standard]==0.115.11", "union>=0.1.150"],
)
```

Then we define a simple FastAPI app that uses `HTTPAuthorizationCredentials` to
authenticate requests.

```python
import os

from fastapi import FastAPI, HTTPException, Security, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated

from union import UnionRemote

app = FastAPI()
fast_api_app = union.app.App(
    name="fastapi-with-auth",
    secrets=[
        union.Secret(key="AUTH_API_KEY", env_var="AUTH_API_KEY"),
        union.Secret(key="MY_UNION_API_KEY", env_var="UNION_API_KEY"),
    ],
    container_image=image_spec,
    framework_app=app,
    limits=union.Resources(cpu="1", mem="1Gi"),
    port=8082,
    requires_auth=False,
)


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> HTTPAuthorizationCredentials:
    auth_api_key = os.getenv("AUTH_API_KEY")
    if credentials.credentials != AUTH_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return credentials


@app.get("/")
def root(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(verify_token)],
):
    return {"message": "Hello, World!"}
```

As you can see, we define a `FastAPI` app and provide it as an input in the
`union.app.App` definition. Then, we define a `verify_token` function that
verifies the API key. Finally, we define a root endpoint that uses the
`verify_token` function to authenticate requests.

Note that we are also requesting for two secrets:
- The `AUTH_API_KEY` is used by the FastAPI app to authenticate the webhook.
- The `MY_UNION_API_KEY` is used to authenticate UnionRemote with Union.

With `requires_auth=False`, you can reach the endpoint without going through Union’s authentication, which is okay since we are rolling our own `AUTH_API_KEY`. Before
we can deploy the app, we create the secrets required by the application:

```bash
union create secret --name AUTH_API_KEY
```

Next, to create the MY_UNION_API_KEY secret, we need to first create a admin api-key:

```bash
union create admin-api-key --name MY_UNION_API_KEY
```
## Deploy the Fast API app

Finally, you can now deploy the FastAPI app:

```bash
union deploy apps app.py fastapi-with-auth
```

Deploying the application will stream the status to the console:

```
Image ghcr.io/.../webhook-serving:KXwIrIyoU_Decb0wgPy23A found. Skip building.
✨ Deploying Application: fastapi-webhook
🔎 Console URL: https://<union-tenant>/console/projects/thomasjpfan/domains/development/apps/fastapi-webhook
[Status] Pending: App is pending deployment
[Status] Pending: RevisionMissing: Configuration "fastapi-webhook" is waiting for a Revision to become ready.
[Status] Pending: IngressNotConfigured: Ingress has not yet been reconciled.
[Status] Pending: Uninitialized: Waiting for load balancer to be ready
[Status] Started: Service is ready
🚀 Deployed Endpoint: https://rough-meadow-97cf5.apps.<union-tenant>
```

Then to invoke the endpoint, you can use the following curl command:

```bash
curl -X GET "https://rough-meadow-97cf5.apps.<union-tenant>/" \
-H "Authorization: Bearer <MY_UNION_API_KEY>"
```
