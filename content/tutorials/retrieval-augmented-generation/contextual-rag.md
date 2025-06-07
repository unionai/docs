---
title: Building a Contextual RAG Workflow with Together AI
weight: 10
variants: -flyte +serverless +byoc +selfmanaged
---

# Building a Contextual RAG Workflow with Together AI

This notebook walks you through building a Contextual RAG (Retrieval-Augmented Generation) workflow using Together's embedding, reranker, and chat models. It ties together web scraping, embedding generation, and serving into one cohesive application.

We take the [existing Contextual RAG Together app](https://docs.together.ai/docs/how-to-implement-contextual-rag-from-anthropic) and make it "production-grade" with {{< key product_name >}} — ready for enterprise deployment.

![Contextual RAG App](../../_static/images/tutorials/retrieval-augmented-generation/contextual-rag/contextual_rag.png)

## Workflow overview

The workflow follows these steps:

1. Fetches all links to Paul Graham's essays.
2. Scrapes web content to retrieve the full text of the essays.
3. Splits the text into smaller chunks for processing.
4. Appends context from the relevant essay to each chunk.
5. Generates embeddings and stores them in a hosted vector database.
6. Creates a keyword index for efficient retrieval.
7. Serves a FastAPI app to expose the RAG functionality.
8. Provides a Gradio app, using the FastAPI endpoint, for an easy-to-use RAG interface.

## Execution approach

This workflow is designed for local execution first, allowing you to test and validate it before deploying and scaling it on a {{< key product_name >}} cluster. This staged approach ensures smooth transitions from development to production.

Before running the workflow, make sure to install `union`:

```
pip install union
```

### Local execution

First, we import the required dependencies to ensure the workflow runs smoothly. Next, we define an actor environment, as the workflow relies on actor tasks throughout the process.

[{{< key product_name >}} Actors](../../user-guide/core-concepts/actors) let us reuse a container and its environment across tasks, avoiding the overhead of starting a new container for each task. In this workflow, we define a single actor and reuse it consistently since the underlying components don’t require independent scaling or separate environments.

Within the actor environment, we specify the `ImageSpec`, which defines the container image that tasks in the workflow will use. With {{< key product_name >}}, every task runs in its own dedicated container, requiring a container image. Instead of manually creating a Dockerfile, we define the image specification in Python. When run on {{< key product_name >}} Serverless, the container image is built remotely, simplifying the setup.

We also configure the actor’s replica count to 10, meaning 10 workers are provisioned to handle tasks, allowing up to 10 tasks to run in parallel, provided sufficient resources. The TTL (time to live) is set to 120 seconds, ensuring the actor remains active for this period when no tasks are being processed.

Finally, we create a Pydantic `BaseModel` named `Document` to capture metadata for each document used by the RAG app. This model ensures consistent data structuring and smooth integration throughout the workflow.

NOTE: Add your Together AI API key (`TOGETHER_API_KEY`) to the `.env` file before running the notebook.

```python
import os
from pathlib import Path
from typing import Annotated, Optional
from urllib.parse import urljoin

import numpy as np
import requests
import union
from flytekit.core.artifact import Artifact
from flytekit.exceptions.base import FlyteRecoverableException
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from pydantic import BaseModel
from union.actor import ActorEnvironment

import {{< key kit_import >}}

actor = ActorEnvironment(
    name="contextual-rag",
    replica_count=10,
    ttl_seconds=120,
    container_image=union.ImageSpec(
        name="contextual-rag",
        packages=[
            "together==1.3.10",
            "beautifulsoup4==4.12.3",
            "bm25s==0.2.5",
            "pydantic>2",
            "pymilvus>=2.5.4",
            "union>=0.1.139",
            "flytekit>=1.15.0b5",
        ],
    ),
    secret_requests=[
        {{< key kit_as >}}.Secret(
            key="together-api-key",
            env_var="TOGETHER_API_KEY",
            mount_requirement=union.Secret.MountType.ENV_VAR,
        ),
        {{< key kit_as >}}.Secret(
            key="milvus-uri",
            env_var="MILVUS_URI",
            mount_requirement=union.Secret.MountType.ENV_VAR,
        ),
        {{< key kit_as >}}.Secret(
            key="milvus-token",
            env_var="MILVUS_TOKEN",
            mount_requirement=union.Secret.MountType.ENV_VAR,
        )
    ],
)

class Document(BaseModel):
    idx: int
    title: str
    url: str
    content: Optional[str] = None
    chunks: Optional[list[str]] = None
    prompts: Optional[list[str]] = None
    contextual_chunks: Optional[list[str]] = None
    tokens: Optional[list[list[int]]] = None
```

We begin by defining an actor task to parse the main page of Paul Graham's essays. This task extracts a list of document titles and their respective URLs. Since actor tasks run within the shared actor environment we set up earlier, they efficiently reuse the same container and environment.

```python
@actor.task
def parse_main_page(
    base_url: str, articles_url: str, local: bool = False
) -> list[Document]:
    from bs4 import BeautifulSoup

    assert base_url.endswith("/"), f"Base URL must end with a slash: {base_url}"
    response = requests.get(urljoin(base_url, articles_url))
    soup = BeautifulSoup(response.text, "html.parser")

    td_cells = soup.select("table > tr > td > table > tr > td")
    documents = []

    idx = 0
    for td in td_cells:
        img = td.find("img")
        if img and int(img.get("width", 0)) <= 15 and int(img.get("height", 0)) <= 15:
            a_tag = td.find("font").find("a") if td.find("font") else None
            if a_tag:
                documents.append(
                    Document(
                        idx=idx, title=a_tag.text, url=urljoin(base_url, a_tag["href"])
                    )
                )
                idx += 1

    if local:
        return documents[:3]

    return documents
```

Next, we define an actor task to scrape the content of each document. Using the list of URLs gathered in the previous step, this task extracts the full text of the essays, ensuring that all relevant content is retrieved for further processing.

We also set `retries` to `3`, meaning the task will be retried three times before the error is propagated.

```python
@actor.task(retries=3)
def scrape_pg_essays(document: Document) -> Document:
    from bs4 import BeautifulSoup

    try:
        response = requests.get(document.url)
    except Exception as e:
        raise FlyteRecoverableException(f"Failed to scrape {document.url}: {str(e)}")

    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("font")

    text = None
    if content:
        text = " ".join(content.get_text().split())
    document.content = text
    return document
```

Then, define an actor task to create chunks for each document. Chunks are necessary because we need to append context to each chunk, ensuring the RAG app can process the information effectively.

```python
@actor.task(cache=True, cache_version="0.2")
def create_chunks(document: Document, chunk_size: int, overlap: int) -> Document:
    if document.content:
        content_chunks = [
            document.content[i : i + chunk_size]
            for i in range(0, len(document.content), chunk_size - overlap)
        ]
        document.chunks = content_chunks
    return document
```

Next, we use Together AI to generate context for each chunk of text, using the secret we initialized earlier. The system retrieves relevant context based on the entire document, ensuring accurate and meaningful outputs.

Notice that we set [`cache`](../../user-guide/core-concepts/caching) to `True` for this task to avoid re-running the execution for the same inputs. This ensures that if the document and model remain unchanged, the outputs are retrieved directly from the cache, improving efficiency.

Once the context is generated, we map the chunks back to their respective documents.

```python
@actor.task(cache=True, cache_version="0.4")
def generate_context(document: Document, model: str) -> Document:
    from together import Together

    CONTEXTUAL_RAG_PROMPT = """
Given the document below, we want to explain what the chunk captures in the document.

{WHOLE_DOCUMENT}

Here is the chunk we want to explain:

{CHUNK_CONTENT}

Answer ONLY with a succinct explanation of the meaning of the chunk in the context of the whole document above.
"""

    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

    contextual_chunks = [
        f"{response.choices[0].message.content} {chunk}"
        for chunk in (document.chunks or [])
        for response in [
            client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": CONTEXTUAL_RAG_PROMPT.format(
                            WHOLE_DOCUMENT=document.content,
                            CHUNK_CONTENT=chunk,
                        ),
                    }
                ],
                temperature=1,
            )
        ]
    ]

    # Assign the contextual chunks back to the document
    document.contextual_chunks = contextual_chunks if contextual_chunks else None
    return document
```

We define an embedding function to generate embeddings for each chunk. This function converts the chunks into vector representations, which we can store in a vector database for efficient retrieval and processing.

Next, we create a vector index and store the embeddings in the [Milvus](https://milvus.io/) vector database. For each embedding, we store the ID, document, and document title. These details ensure the embeddings are ready for efficient retrieval during the RAG process.

By setting `cache` to `True`, we avoid redundant upserts or inserts for the same document. Instead, we can add new records or update existing ones only if the content has changed. This approach keeps the vector database up-to-date efficiently, minimizing resource usage while maintaining accuracy.

Note: We're using the Milvus hosted vector database to store the embeddings. However, you can replace it with any vector database of your choice based on your requirements.

```python
from together import Together

def get_embedding(chunk: str, embedding_model: str):
    client = Together(
        api_key=os.getenv("TOGETHER_API_KEY")
    )
    outputs = client.embeddings.create(
        input=chunk,
        model=embedding_model,
    )
    return outputs.data[0].embedding


@actor.task(cache=True, cache_version="0.19", retries=5)
def create_vector_index(
    document: Document, embedding_model: str, local: bool = False
) -> Document:
    from pymilvus import DataType, MilvusClient

    if local:
        client = MilvusClient("test_milvus.db")
    else:
        try:
            client = MilvusClient(uri=os.getenv("MILVUS_URI"), token=os.getenv("MILVUS_TOKEN"))
        except Exception as e:
            raise FlyteRecoverableException(
                f"Failed to connect to Milvus: {e}"
            )

    collection_name = "paul_graham_collection"

    if not client.has_collection(collection_name):
        schema = client.create_schema()
        schema.add_field(
            "id", DataType.INT64, is_primary=True, auto_id=True
        )
        schema.add_field("document_index", DataType.VARCHAR, max_length=255)
        schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=1024)
        schema.add_field("title", DataType.VARCHAR, max_length=255)
        index_params = client.prepare_index_params()
        index_params.add_index("embedding", metric_type="COSINE")

        client.create_collection(collection_name, dimension=512, schema=schema, index_params=index_params)

    if not document.contextual_chunks:
        return document  # Exit early if there are no contextual chunks

    # Generate embeddings for chunks
    embeddings = [get_embedding(chunk[:512], embedding_model) for chunk in document.contextual_chunks] # NOTE: Trimming the chunk for the embedding model's context window
    embeddings_np = np.array(embeddings, dtype=np.float32)

    ids = [
        f"id{document.idx}_{chunk_idx}"
        for chunk_idx, _ in enumerate(document.contextual_chunks)
    ]
    titles = [document.title] * len(document.contextual_chunks)

    client.upsert(
        collection_name,
        [
            {"id": index, "document_index": document_index, "embedding": embedding, "title": title}
            for index, (document_index, embedding, title) in enumerate(zip(ids, embeddings_np.tolist(), titles))
        ]
    )

    return document
```

Lastly, we create a BM25S keyword index to organize the document chunks. This index is great for keyword-based searches and works well alongside vector indexing. We also store a mapping between document IDs and their corresponding contextual chunk data, making it easier to retrieve content during the RAG process.

```python
@actor.task(cache=True, cache_version="0.5")
def create_bm25s_index(documents: list[Document]) -> tuple[FlyteDirectory, FlyteFile]:
    import json
    import bm25s

    # Prepare data for JSON
    data = {
        f"id{doc_idx}_{chunk_idx}": contextual_chunk
        for doc_idx, document in enumerate(documents)
        if document.contextual_chunks
        for chunk_idx, contextual_chunk in enumerate(document.contextual_chunks)
    }

    retriever = bm25s.BM25(corpus=list(data.values()))
    retriever.index(bm25s.tokenize(list(data.values())))

    ctx = union.current_context()
    working_dir = Path(ctx.working_directory)
    bm25s_index_dir = working_dir / "bm25s_index"
    contextual_chunks_json = working_dir / "contextual_chunks.json"

    retriever.save(str(bm25s_index_dir))

    # Write the data to a JSON file
    with open(contextual_chunks_json, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    return FlyteDirectory(path=bm25s_index_dir), FlyteFile(contextual_chunks_json)
```

We define a [standard workflow](../../user-guide/core-concepts/workflows/standard-workflows) to execute these tasks in sequence. By using [map tasks](../../user-guide/core-concepts/tasks/task-types#map-tasks), we run operations in parallel while respecting the resource constraints of each task. This approach **significantly improves execution speed**. We set the concurrency to 2, meaning two tasks will run in parallel. Note that the replica count for actors is set to 10, but this can be overridden at the map task level. We're doing this because having too many parallel clients could cause server availability issues.

The final output of this workflow includes the BM25S keyword index and the contextual chunks mapping file, both returned as [{{< key product_name >}} Artifacts](../../user-guide/core-concepts/artifacts). The Artifact Service automatically indexes and assigns semantic meaning to all outputs from {{< key product_name >}} tasks and workflow executions, such as models, files, or other data. This makes it easy to track, access, and orchestrate pipelines directly through their outputs. In this case, the keyword index and file artifacts are directly used during app serving.

We also set up a retrieval task to fetch embeddings for local execution. Once everything’s in place, we run the workflow and the retrieval task locally, producing a set of relevant chunks.

One advantage of running locally is that all tasks and workflows are Python functions, making it easy to test everything before moving to production. This approach allows you to experiment locally and then deploy the same workflow in a production environment, ensuring it’s production-ready. You get the flexibility to test and refine your workflow without compromising on the capabilities needed for deployment.

```python
import functools
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()  # Ensure the secret (together API key) is present in the .env file

BM25Index = Artifact(name="bm25s-index")
ContextualChunksJSON = Artifact(name="contextual-chunks-json")


@union.workflow
def build_indices_wf(
    base_url: str = "https://paulgraham.com/",
    articles_url: str = "articles.html",
    embedding_model: str = "BAAI/bge-large-en-v1.5",
    chunk_size: int = 250,
    overlap: int = 30,
    model: str = "deepseek-ai/DeepSeek-R1",
    local: bool = True,
) -> tuple[
    Annotated[FlyteDirectory, BM25Index], Annotated[FlyteFile, ContextualChunksJSON]
]:
    tocs = parse_main_page(base_url=base_url, articles_url=articles_url, local=local)
    scraped_content = {{< key kit_as >}}.{{<key map_func>}}(scrape_pg_essays, concurrency=2)(document=tocs)
    chunks = {{< key kit_as >}}.{{<key map_func>}}(
        functools.partial(create_chunks, chunk_size=chunk_size, overlap=overlap)
    )(document=scraped_content)
    contextual_chunks = {{< key kit_as >}}.{{<key map_func>}}(functools.partial(generate_context, model=model))(
        document=chunks
    )
    {{< key kit_as >}}.{{<key map_func>}}(
        functools.partial(
            create_vector_index, embedding_model=embedding_model, local=local
        ),
        concurrency=2
    )(document=contextual_chunks)
    bm25s_index, contextual_chunks_json_file = create_bm25s_index(
        documents=contextual_chunks
    )
    return bm25s_index, contextual_chunks_json_file


@dataclass
class RetrievalResults:
    vector_results: list[list[str]]
    bm25s_results: list[list[str]]


@union.task
def retrieve(
    bm25s_index: FlyteDirectory,
    contextual_chunks_data: FlyteFile,
    embedding_model: str = "BAAI/bge-large-en-v1.5",
    queries: list[str] = [
        "What to do in the face of uncertainty?",
        "Why won't people write?",
    ],
) -> RetrievalResults:
    import json

    import bm25s
    import numpy as np
    from pymilvus import MilvusClient

    client = MilvusClient("test_milvus.db")

    # Generate embeddings for the queries using Together
    query_embeddings = [
        get_embedding(query, embedding_model) for query in queries
    ]
    query_embeddings_np = np.array(query_embeddings, dtype=np.float32)

    collection_name = "paul_graham_collection"
    results = client.search(
        collection_name,
        query_embeddings_np,
        limit=5,
        search_params={"metric_type": "COSINE"},
        anns_field="embedding",
        output_fields=["document_index", "title"]
    )

    # Load BM25S index
    retriever = bm25s.BM25()
    bm25_index = retriever.load(save_dir=bm25s_index.download())

    # Load contextual chunk data
    with open(contextual_chunks_data, "r", encoding="utf-8") as json_file:
        contextual_chunks_data_dict = json.load(json_file)

    # Perform BM25S-based retrieval
    bm25s_idx_result = bm25_index.retrieve(
        query_tokens=bm25s.tokenize(queries),
        k=5,
        corpus=np.array(list(contextual_chunks_data_dict.values())),
    )

    # Return results as a dataclass
    return RetrievalResults(
        vector_results=results,
        bm25s_results=bm25s_idx_result.documents.tolist(),
    )

if __name__ == "__main__":
    bm25s_index, contextual_chunks_data = build_indices_wf()
    results = retrieve(
        bm25s_index=bm25s_index, contextual_chunks_data=contextual_chunks_data
    )
    print(results)
```

### Remote execution

To provide the Together AI API key to the actor during remote execution, we send it as a [secret](../../user-guide/development-cycle/managing-secrets#creating-secrets). We can create this secret using the {{< key product_name >}} CLI before running the workflow. Simply run the following commands:
```
union create secret together-api-key
```

To run the workflow remotely on a {{< key product_name >}} cluster, we start by logging into the cluster.

```python
!union create login --serverless
```

Then, we initialize a {{< key product_name >}} remote object to execute the workflow on the cluster. The [UnionRemote](../../user-guide/development-cycle/union-remote) Python API supports functionality similar to that of the Union CLI, enabling you to manage {{< key product_name >}} workflows, tasks, launch plans and artifacts from within your Python code.

```python
from union.remote import UnionRemote

remote = UnionRemote(default_project="default", default_domain="development")
```

```python
indices_execution = remote.execute(build_indices_wf, inputs={"local": False})
print(indices_execution.execution_url)
```

We define a launch plan to run the workflow daily. A [launch plan](../../user-guide/core-concepts/launch-plans/) serves as a template for invoking the workflow.

The scheduled launch plan ensures that the vector database and keyword index are regularly updated, keeping the data fresh and synchronized.

Be sure to note the `version` field when registering the launch plan. Each Union entity (task, workflow, launch plan) is automatically versioned, as every entity is associated with a version by default.

```python
lp = {{< key kit_as >}}.LaunchPlan.get_or_create(
    workflow=build_indices_wf,
    name="vector_db_ingestion_activate",
    schedule={{< key kit_as >}}.CronSchedule(
        schedule="0 1 * * *"
    ),  # Run every day to update the databases
    auto_activate=True,
)

registered_lp = remote.register_launch_plan(entity=lp)
```

## Deploy apps

We deploy the FastAPI and Gradio applications to serve the RAG app with {{< key product_name >}}. FastAPI is used to define the endpoint for serving the app, while Gradio is used to create the user interface.

When defining the app, we can specify inputs, images (using `ImageSpec`), resources to assign to the app, secrets, replicas, and more. We can organize the app specs into separate files. The FastAPI app spec is available in the `fastapi_app.py` file, and the Gradio app spec is in the `gradio_app.py` file.

We retrieve the artifacts and send them as inputs to the FastAPI app. We can then retrieve the app's endpoint to use in the other app. Finally, we either create the app if it doesn't already exist or update it if it does.

While we’re using FastAPI and Gradio here, you can use any Python-based front-end and API frameworks to define your apps.

```python
import os

from union.app import App, Input


fastapi_app = App(
    name="contextual-rag-fastapi",
    inputs=[
        Input(
            name="bm25s_index",
            value=BM25Index.query(),
            download=True,
            env_var="BM25S_INDEX",
        ),
        Input(
            name="contextual_chunks_json",
            value=ContextualChunksJSON.query(),
            download=True,
            env_var="CONTEXTUAL_CHUNKS_JSON",
        ),
    ],
    container_image=union.ImageSpec(
        name="contextual-rag-fastapi",
        packages=[
            "together",
            "bm25s",
            "pymilvus",
            "uvicorn[standard]",
            "fastapi[standard]",
            "union-runtime>=0.1.10",
            "flytekit>=1.15.0b5",
        ],
    ),
    limits=union.Resources(cpu="1", mem="3Gi"),
    port=8080,
    include=["fastapi_app.py"],
    args=["uvicorn", "fastapi_app:app", "--port", "8080"],
    min_replicas=1,
    max_replicas=1,
    secrets=[
        {{< key kit_as >}}.Secret(
            key="together-api-key",
            env_var="TOGETHER_API_KEY",
            mount_requirement=union.Secret.MountType.ENV_VAR
        ),
        {{< key kit_as >}}.Secret(
            key="milvus-uri",
            env_var="MILVUS_URI",
            mount_requirement=union.Secret.MountType.ENV_VAR,
        ),
        {{< key kit_as >}}.Secret(
            key="milvus-token",
            env_var="MILVUS_TOKEN",
            mount_requirement=union.Secret.MountType.ENV_VAR,
        ),
    ],
)


gradio_app = App(
    name="contextual-rag-gradio",
    inputs=[
        Input(
            name="fastapi_endpoint",
            value=fastapi_app.query_endpoint(public=False),
            env_var="FASTAPI_ENDPOINT",
        )
    ],
    container_image=union.ImageSpec(
        name="contextual-rag-gradio",
        packages=["gradio", "union-runtime>=0.1.5"],
    ),
    limits=union.Resources(cpu="1", mem="1Gi"),
    port=8080,
    include=["gradio_app.py"],
    args=[
        "python",
        "gradio_app.py",
    ],
    min_replicas=1,
    max_replicas=1,
)
```

```python
from union.remote._app_remote import AppRemote

app_remote = AppRemote(project="default", domain="development")

app_remote.create_or_update(fastapi_app)
app_remote.create_or_update(gradio_app)
```

The apps will be deployed at the URLs provided in the output, which you can access. Below are some example queries to test the Gradio application:

- What did Paul Graham do growing up?
- What did the author do during their time in art school?
- Can you give me a summary of the author's life?
- What did the author do during their time at Yale?
- What did the author do during their time at YC?

```python
# If you want to stop the apps, here’s how you can do it:
# app_remote.stop(name="contextual-rag-fastapi-app")
# app_remote.stop(name="contextual-rag-gradio-app")
```
