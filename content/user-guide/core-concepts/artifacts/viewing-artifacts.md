---
title: Viewing artifacts
weight: 5
variants: -flyte +serverless +byoc +selfmanaged
---

# Viewing artifacts

## Artifacts list

Artifacts can be viewed in the UI by navigating to the artifacts app in the left sidebar:

![Artifacts overview](../../../_static/images/user-guide/core-concepts/artifacts/viewing-artifacts/artifacts-list.png)

## Artifact view

Selecting a specific artifact from the artifact list will take you to that artifact's **Overview** page:

![Single artifact overview](../../../_static/images/user-guide/core-concepts/artifacts/viewing-artifacts/artifact-view.png)

Here you can see relevant metadata about the artifact, including:
* Its version
* Its partitions
* The task or workflow that produced it
* Its creation time
* Its object store URI
* Code for accessing the artifact via [{{< key kit_remote >}}](../../development-cycle/union-remote)

You can also view the artifact's object structure, model card, and lineage graph.

### Artifact lineage graph

Once an artifact is materialized, you can view its lineage in the UI, including the specific upstream task or workflow execution that created it, and any downstream workflows that consumed it. You can traverse the lineage graph by clicking between artifacts and inspecting any relevant workflow executions in order to understand and reproduce any step in the AI development process.

![Artifact lineage overview](../../../_static/images/user-guide/core-concepts/artifacts/viewing-artifacts/artifact-lineage.png)

You can navigate through the lineage graph by clicking from artifact to artifact.