---
title: OpenAI Batch Agent
weight: 1
variants: +flyte -serverless -byoc -byok
sidebar_expanded: false
---

# OpenAI Batch Agent

The Batch API agent allows you to submit requests for asynchronous batch processing on OpenAI.
You can provide either a JSONL file or a JSON iterator, and the agent handles the upload to OpenAI,
creation of the batch, and downloading of the output and error files.

## Installation

To use the OpenAI Batch agent, run the following command:

```shell
$ pip install flytekitplugins-openai
```

## Example usage

For a usage example, see [OpenAI Batch agent example usage](./openai_batch_agent_example_usage).

## Local testing

To test an agent locally, create a class for the agent task that inherits from
[SyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L222-L256)
or [AsyncAgentExecutorMixin](https://github.com/flyteorg/flytekit/blob/master/flytekit/extend/backend/base_agent.py#L259-L354).
These mixins can handle synchronous and synchronous tasks, respectively,
and allow flytekit to mimic FlytePropeller's behavior in calling the agent.
For more information, see "[Testing agents locally](https://docs.flyte.org/en/latest/flyte_agents/testing_agents_locally.html)".

## Flyte deployment configuration

> [!NOTE]
> If you are using a managed deployment of Flyte, you will need to contact your deployment administrator to configure agents in your deployment.

To enable the OpenAI Batch agent in your Flyte deployment, refer to the
[OpenAI Batch agent setup guide](../../../deployment/flyte-connectors/openai-batch)
