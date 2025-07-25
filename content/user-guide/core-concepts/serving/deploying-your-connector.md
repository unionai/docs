---
title: Deploy Custom Flyte Connectors
weight: 6
variants: -flyte +serverless +byoc +selfmanaged
---

# Deploying Custom Flyte Connectors

[Flyte connectors](../../../integrations/connectors/_index.md) allow you to extend Union's capabilities by integrating with external services.
This guide explains how to deploy custom connectors that can be used in your Flyte workflows.

## Overview

Connectors enable your workflows to interact with third-party services or systems.
Union.ai supports deploying connectors as services using the `FlyteConnectorApp` class. You can deploy connectors in two ways:

1. **Module-based deployment**: Include your connector code directly in the deployment
2. **ImageSpec-based deployment**: Use pre-built images with connectors already installed

## Prerequisites

Before deploying a connector, ensure you have:

- A Union.ai account
- Any required API keys or credentials for your connector
- Docker registry access (if using custom images)

## Connector Deployment Options

### Module-based Deployment

Module-based deployment is ideal when you want to iterate quickly on connector development. With this approach, you include your connector code directly using the `include` parameter.

```python
# app.py

from union import ImageSpec, Resources, Secret
from union.app import FlyteConnectorApp

image = ImageSpec(
    name="flyteconnector",
    packages=[
        "flytekit[connector]",
        "union",
        "union-runtime",
        "openai",  # ChatGPT connector needs openai SDK
    ],
    env={"FLYTE_SDK_LOGGING_LEVEL": "10"},
    builder="union",
)

openai_connector_app = FlyteConnectorApp(
    name="openai-connector-app",
    container_image=image,
    secrets=[Secret(key="flyte_openai_api_key")],
    limits=Resources(cpu="1", mem="1Gi"),
    include=["./chatgpt"],  # Include the connector module directory
)
```

With this approach, you organize your connector code in a module structure:

```bash
chatgpt/
├── __init__.py
├── connector.py
└── constants.py
```

The `include` parameter takes a list of files or directories to include in the deployment.

### ImageSpec-based Deployment

ImageSpec-based deployment is preferred for production environments where you have stable connector implementations. In this approach, your connector code is pre-installed in a container image.

```python
# app.py

from union import ImageSpec, Resources, Secret
from union.app import FlyteConnectorApp

image = ImageSpec(
    name="flyteconnector",
    packages=[
        "flytekit[connector]",
        "flytekitplugins-slurm",
        "union",
        "union-runtime",
    ],
    apt_packages=["build-essential", "libmagic1", "vim", "openssh-client", "ca-certificates"],
    env={"FLYTE_SDK_LOGGING_LEVEL": "10"},
    builder="union",
)

slurm_connector_app = FlyteConnectorApp(
    name="slurm-connector-app",
    container_image=image,
    secrets=[Secret(key="flyte_slurm_private_key")],
    limits=Resources(cpu="1", mem="1Gi"),
)
```

## Managing Secrets

Most connectors require credentials to authenticate with external services. Union.ai allows you to manage these securely:

```bash
# Create a secret for OpenAI API key
union create secret flyte_openai_api_key -f /etc/secrets/flyte_openai_api_key --project flytesnacks --domain development

# Create a secret for SLURM access
union create secret flyte_slurm_private_key -f /etc/secrets/flyte_slurm_private_key --project flytesnacks --domain development
```

Reference these secrets in your connector app:

```python
from union import Secret

# In your app definition
secrets=[Secret(key="flyte_openai_api_key")]
```

Inside your connector code, access these secrets using:

```python
from flytekit.extend.backend.utils import get_connector_secret

api_key = get_connector_secret(secret_key="FLYTE_OPENAI_API_KEY")
```

## Example: Creating a ChatGPT Connector

Here's how to implement a ChatGPT connector:

1. Create a connector class:

```python
# chatgpt/connector.py

import asyncio
import logging
from typing import Optional

import openai
from flyteidl.core.execution_pb2 import TaskExecution
from flytekit import FlyteContextManager
from flytekit.core.type_engine import TypeEngine
from flytekit.extend.backend.base_connector import ConnectorRegistry, Resource, SyncConnectorBase
from flytekit.extend.backend.utils import get_connector_secret
from flytekit.models.literals import LiteralMap
from flytekit.models.task import TaskTemplate

from .constants import OPENAI_API_KEY, TIMEOUT_SECONDS


class ChatGPTConnector(SyncConnectorBase):
    name = "ChatGPT Connector"

    def __init__(self):
        super().__init__(task_type_name="chatgpt")

    async def do(
        self,
        task_template: TaskTemplate,
        inputs: Optional[LiteralMap] = None,
        **kwargs,
    ) -> Resource:
        ctx = FlyteContextManager.current_context()
        input_python_value = TypeEngine.literal_map_to_kwargs(ctx, inputs, {"message": str})
        message = input_python_value["message"]

        custom = task_template.custom
        custom["chatgpt_config"]["messages"] = [{"role": "user", "content": message}]
        client = openai.AsyncOpenAI(
            organization=custom["openai_organization"],
            api_key=get_connector_secret(secret_key=OPENAI_API_KEY),
        )

        logger = logging.getLogger("httpx")
        logger.setLevel(logging.WARNING)

        completion = await asyncio.wait_for(client.chat.completions.create(**custom["chatgpt_config"]), TIMEOUT_SECONDS)
        message = completion.choices[0].message.content
        outputs = {"o0": message}

        return Resource(phase=TaskExecution.SUCCEEDED, outputs=outputs)


ConnectorRegistry.register(ChatGPTConnector())
```

2. Define constants:

```python
# chatgpt/constants.py

# Constants for ChatGPT connector
TIMEOUT_SECONDS = 10
OPENAI_API_KEY = "FLYTE_OPENAI_API_KEY"
```

3. Create an `__init__.py` file:

```python
# chatgpt/__init__.py

from .connector import ChatGPTConnector

__all__ = ["ChatGPTConnector"]
```

## Using the Connector in a Workflow

After deploying your connector, you can use it in your workflows:

```python
# workflow.py

from flytekit import workflow
from flytekitplugins.openai import ChatGPTTask

chatgpt_small_job = ChatGPTTask(
    name="3.5-turbo",
    chatgpt_config={
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
    },
)

chatgpt_big_job = ChatGPTTask(
    name="gpt-4",
    chatgpt_config={
        "model": "gpt-4",
        "temperature": 0.7,
    },
)


@workflow
def wf(message: str) -> str:
    message = chatgpt_small_job(message=message)
    message = chatgpt_big_job(message=message)
    return message
```

Run the workflow:

```bash
union run --remote workflow.py wf --message "Tell me about Union.ai"
```

## Creating Your Own Connector

To create a custom connector:

1. Inherit from `SyncConnectorBase` or `AsyncConnectorBase`
2. Implement the required methods (`do` for synchronous connectors, `create`, `get`, and `delete` for asynchronous connectors)
3. Register your connector with `ConnectorRegistry.register(YourConnector())`
4. Deploy your connector using one of the methods above

## Deployment Commands

Deploy your connector app:

```bash
# Module-based deployment
union deploy apps app_module_deployment/app.py openai-connector-app

# ImageSpec-based deployment
union deploy apps app_image_spec_deployment/app.py slurm-connector-app
```

## Best Practices

1. **Security**: Never hardcode credentials; always use Union.ai secrets
2. **Error Handling**: Include robust error handling in your connector implementation
3. **Timeouts**: Set appropriate timeouts for external API calls
4. **Logging**: Implement detailed logging for debugging
5. **Testing**: Test your connector thoroughly before deploying to production

By following this guide, you can create and deploy custom connectors that extend Union.ai's capabilities to integrate with any external service or system your workflows need to interact with.
