---
title: Contributing code
weight: 2
variants: +flyte -serverless -byoc -selfmanaged
---

# Contributing code

Thank you for taking the time to contribute to Flyte!

Here are some guidelines for you to follow, which will make your first and follow-up contributions easier.

TL;DR: Find the repo-specific contribution guidelines in the [Component Reference](#component-reference) section.

## Becoming a contributor

An issue tagged with [`good first issue`](https://github.com/flyteorg/flyte/labels/good%20first%20issue) is the best place to start for first-time contributors.

**Fork and clone the concerned repository. Create a new branch on your fork and make the required changes. Create a pull request once your work is ready for review.**

> [!NOTE]
> To open a pull request, refer to [GitHub's guide](https://guides.github.com/activities/forking/) for detailed instructions.

Example PR for your reference: [GitHub PR](https://github.com/flyteorg/flytepropeller/pull/242).
Several checks are introduced to help maintain the robustness of the project:

1. To get through DCO, sign off on every commit ([Reference](https://github.com/src-d/guide/blob/master/developer-community/fix-DCO.md)).
2. To improve code coverage, write unit tests to test your code.
3. Make sure all the tests pass. If you face any issues, please let us know in the [`#contribute`](https://flyte-org.slack.com/archives/C04NJPLRWUX) channel.
4. Format your Go code with `golangci-lint` followed by `goimports` (use `make lint` and `make goimports`).
5. Format your Python code with `black` and `isort` (use `make fmt`).
6. If make targets are not available, you can manually format the code.

> [!NOTE]
> Refer to [Effective Go](https://golang.org/doc/effective_go), [Black](https://github.com/psf/black), and [Isort](https://github.com/PyCQA/isort) for full coding standards.

As you become more involved with the project, you may be able to be added as a committer to the repos you're working on. Check out the [Flyte Contributor Ladder](https://github.com/flyteorg/community/blob/main/GOVERNANCE.md#community-roles-and-path-to-maintainership) to learn more.

### Before submitting your PR

We strongly encourage you to add one of these labels to your Pull Request:

- **added**: For new features.
- **changed**: For changes in existing functionality.
- **deprecated**: For soon-to-be-removed features.
- **removed**: For features being removed.
- **fixed**: For any bug fixes.
- **security**: In case of vulnerabilities.

This is helpful to build human-readable release notes. [Learn more](https://keepachangelog.com/en/1.1.0/).

> [!NOTE]
> Learn how to apply a label to a PR in the [GitHub docs](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels#applying-a-label).

## 🐞 File an issue

We use [GitHub Issues](https://github.com/flyteorg/flyte/issues) for issue tracking. The following issue types are available for filing an issue:

- [Plugin Request](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=untriaged%2Cplugins&template=backend-plugin-request.md&title=%5BPlugin%5D)
- [Bug Report](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=bug%2C+untriaged&template=bug_report.md&title=%5BBUG%5D+)
- [Documentation Bug/Update Request](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=documentation%2C+untriaged&template=docs_issue.md&title=%5BDocs%5D)
- [Core Feature Request](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=enhancement%2C+untriaged&template=feature_request.md&title=%5BCore+Feature%5D)
- [Flytectl Feature Request](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=enhancement%2C+untriaged%2C+flytectl&template=flytectl_issue.md&title=%5BFlytectl+Feature%5D)
- [Housekeeping](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=housekeeping&template=housekeeping_template.md&title=%5BHousekeeping%5D+)
- [UI Feature Request](https://github.com/flyteorg/flyte/issues/new?assignees=&labels=enhancement%2C+untriaged%2C+ui&template=ui_feature_request.md&title=%5BUI+Feature%5D)

If none of the above fit your requirements, file a [blank](https://github.com/flyteorg/flyte/issues/new) issue.
Also, add relevant labels to your issue. For example, if you are filing a Flytekit plugin request, add the `flytekit` label.

For feedback at any point in the contribution process, feel free to reach out to us on [Slack](https://flyte-org.slack.com/archives/C04NJPLRWUX).

## Component Reference

To understand how the below components interact with each other, refer to [Understand the lifecycle of a workflow](#workflow-lifecycle).

> [!NOTE]
> Except for `flytekit`, the below components are maintained in the [`flyte` monorepo](https://github.com/flyteorg/flyte).

![Dependency graph between various flyteorg repos](../_static/images/community/contributing-code/dependency-graph.png)

### `flyte`

| **Repo** | [flyte](https://github.com/flyteorg/flyte) |
|----------|-------------------------------------------|
| **Purpose** | Deployment, Documentation, and Issues |
| **Languages** | RST |

### `flyteidl`

| **Repo** | [flyteidl](https://github.com/flyteorg/flyteidl) |
|----------|-------------------------------------------------|
| **Purpose** | Flyte workflow specification is in [protocol buffers](https://developers.google.com/protocol-buffers) which forms the core of Flyte |
| **Language** | Protobuf |
| **Guidelines** | Refer to the [README](https://github.com/flyteorg/flyteidl#generate-code-from-protobuf) |

### `flytepropeller`

| **Repo** | [flytepropeller](https://github.com/flyteorg/flytepropeller) \| [Code Reference](https://pkg.go.dev/mod/github.com/flyteorg/flytepropeller) |
|----------|------------------------------------------------------------------------------------------------|
| **Purpose** | Kubernetes-native operator |
| **Language** | Go |
| **Guidelines** |                                                                                          |
|              | - Check for Makefile in the root repo                                                      |
|              | - Run the following commands:                                                              |
|              |   - `make generate`                                                                        |
|              |   - `make test_unit`                                                                       |
|              |   - `make lint`                                                                            |
|              | - To compile, run `make compile`                                                           |

### `flyteadmin`

| **Repo** | [flyteadmin](https://github.com/flyteorg/flyteadmin) \| [Code Reference](https://pkg.go.dev/mod/github.com/flyteorg/flyteadmin) |
|----------|------------------------------------------------------------------------------------------------|
| **Purpose** | Control Plane |
| **Language** | Go |
| **Guidelines** |                                                                                          |
|              | - Check for Makefile in the root repo                                                      |
|              | - If the service code has to be tested, run it locally:                                    |
|              |   - `make compile`                                                                         |
|              |   - `make server`                                                                          |
|              | - To seed data locally:                                                                    |
|              |   - `make compile`                                                                         |
|              |   - `make seed_projects`                                                                   |
|              |   - `make migrate`                                                                         |
|              | - To run integration tests locally:                                                        |
|              |   - `make integration`                                                                     |
|              |   - (or to run in containerized dockernetes): `make k8s_integration`                       |

### `flytekit`

| **Repo** | [flytekit](https://github.com/flyteorg/flytekit) |
|----------|-------------------------------------------------|
| **Purpose** | Python SDK & Tools |
| **Language** | Python |
| **Guidelines** | Refer to the [Flytekit Contribution Guide](https://docs.flyte.org/en/latest/api/flytekit/contributing.html) |

### `flyteconsole`

| **Repo** | [flyteconsole](https://github.com/flyteorg/flyteconsole) |
|----------|---------------------------------------------------------|
| **Purpose** | Admin Console |
| **Language** | Typescript |
| **Guidelines** | Refer to the [README](https://github.com/flyteorg/flyteconsole/blob/master/README.md) |

### `datacatalog`

| **Repo** | [datacatalog](https://github.com/flyteorg/datacatalog) \| [Code Reference](https://pkg.go.dev/mod/github.com/flyteorg/datacatalog) |
|----------|------------------------------------------------------------------------------------------------|
| **Purpose** | Manage Input & Output Artifacts |
| **Language** | Go |

### `flyteplugins`

| **Repo** | [flyteplugins](https://github.com/flyteorg/flyteplugins) \| [Code Reference](https://pkg.go.dev/mod/github.com/flyteorg/flyteplugins) |
|----------|------------------------------------------------------------------------------------------------|
| **Purpose** | Flyte Plugins |
| **Language** | Go |
| **Guidelines** |                                                                                          |
|              | - Check for Makefile in the root repo                                                      |
|              | - Run the following commands:                                                              |
|              |   - `make generate`                                                                        |
|              |   - `make test_unit`                                                                       |
|              |   - `make lint`                                                                            |

### `flytestdlib`

| **Repo** | [flytestdlib](https://github.com/flyteorg/flytestdlib) |
|----------|-------------------------------------------------------|
| **Purpose** | Standard Library for Shared Components |
| **Language** | Go |

### `flytectl`

| **Repo** | [flytectl](https://github.com/flyteorg/flytectl) |
|----------|-------------------------------------------------|
| **Purpose** | A standalone Flyte CLI |
| **Language** | Go |
| **Guidelines** | Refer to the [FlyteCTL Contribution Guide](https://docs.flyte.org/en/latest/flytectl/contribute.html) |

## Development Environment Setup Guide

This guide provides a step-by-step approach to setting up a local
development environment for
[flyteidl](https://github.com/flyteorg/flyteidl),
[flyteadmin](https://github.com/flyteorg/flyteadmin),
[flyteplugins](https://github.com/flyteorg/flyteplugins),
[flytepropeller](https://github.com/flyteorg/flytepropeller),
[flytekit](https://github.com/flyteorg/flytekit) ,
[flyteconsole](https://github.com/flyteorg/flyteconsole),
[datacatalog](https://github.com/flyteorg/datacatalog), and
[flytestdlib](https://github.com/flyteorg/flytestdlib).

The video below is a tutorial on how to set up a local development
environment for Flyte.

{{< youtube V-KlVQmQAjE >}}

### Requirements

This guide has been tested and used on AWS EC2 with an Ubuntu 22.04
image. The following tools are required:

- [Docker](https://docs.docker.com/install/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Go](https://golang.org/doc/install)

### Content

- [Contributing code](#contributing-code)
  - [Becoming a contributor](#becoming-a-contributor)
    - [Before submitting your PR](#before-submitting-your-pr)
  - [🐞 File an issue](#-file-an-issue)
  - [Component Reference](#component-reference)
    - [`flyte`](#flyte)
    - [`flyteidl`](#flyteidl)
    - [`flytepropeller`](#flytepropeller)
    - [`flyteadmin`](#flyteadmin)
    - [`flytekit`](#flytekit)
    - [`flyteconsole`](#flyteconsole)
    - [`datacatalog`](#datacatalog)
    - [`flyteplugins`](#flyteplugins)
    - [`flytestdlib`](#flytestdlib)
    - [`flytectl`](#flytectl)
  - [Development Environment Setup Guide](#development-environment-setup-guide)
    - [Requirements](#requirements)
    - [Content](#content)
    - [How to setup dev environment for flyteidl, flyteadmin, flyteplugins, flytepropeller, datacatalog and flytestdlib?](#how-to-setup-dev-environment-for-flyteidl-flyteadmin-flyteplugins-flytepropeller-datacatalog-and-flytestdlib)
    - [How to setup dev environment for flytekit?](#how-to-setup-dev-environment-for-flytekit)
    - [How to setup dev environment for flyteconsole?](#how-to-setup-dev-environment-for-flyteconsole)
    - [How to access Flyte UI, minio, postgres, k3s, and endpoints?](#how-to-access-flyte-ui-minio-postgres-k3s-and-endpoints)

### How to setup dev environment for flyteidl, flyteadmin, flyteplugins, flytepropeller, datacatalog and flytestdlib?

**1. Install flytectl**

[Flytectl](https://github.com/flyteorg/flytectl) is a portable and lightweight command-line interface to work with Flyte.

``` shell
# Step 1: Install the latest version of flytectl
curl -sL https://ctl.flyte.org/install | bash
# flyteorg/flytectl info checking GitHub for latest tag
# flyteorg/flytectl info found version: 0.6.39 for v0.6.39/Linux/x86_64
# flyteorg/flytectl info installed ./bin/flytectl

# Step 2: Export flytectl path based on the previous log "flyteorg/flytectl info installed ./bin/flytectl"
export PATH=$PATH:/home/ubuntu/bin # replace with your path
```

**2. Build a k3s cluster that runs minio and postgres Pods.**

[Minio](https://min.io/) is an S3-compatible object store that will be used later to store task output, input, etc.

[Postgres](https://www.postgresql.org/) is an open-source object-relational database that will later be used by flyteadmin/dataCatalog to store all Flyte information.

``` shell
# Step 1: Start k3s cluster, create Pods for postgres and minio. Note: We cannot access Flyte UI yet! but we can access the minio console now.
flytectl demo start --dev
# 👨‍💻 Flyte is ready! Flyte UI is available at http://localhost:30080/console 🚀 🚀 🎉
# ❇️ Run the following command to export demo environment variables for accessing flytectl
#         export FLYTECTL_CONFIG=/home/ubuntu/.flyte/config-sandbox.yaml
# 🐋 Flyte sandbox ships with a Docker registry. Tag and push custom workflow images to localhost:30000
# 📂 The Minio API is hosted on localhost:30002. Use http://localhost:30080/minio/login for Minio console

# Step 2: Export FLYTECTL_CONFIG as the previous log indicated.
FLYTECTL_CONFIG=/home/ubuntu/.flyte/config-sandbox.yaml

# Step 3: The kubeconfig will be automatically copied to the user's main kubeconfig (default is `/.kube/config`) with "flyte-sandbox" as the context name.
# Check that we can access the K3s cluster. Verify that postgres and minio are running.
kubectl get pod -n flyte
# NAME                                                  READY   STATUS    RESTARTS   AGE
# flyte-sandbox-docker-registry-85745c899d-dns8q        1/1     Running   0          5m
# flyte-sandbox-kubernetes-dashboard-6757db879c-wl4wd   1/1     Running   0          5m
# flyte-sandbox-proxy-d95874857-2wc5n                   1/1     Running   0          5m
# flyte-sandbox-minio-645c8ddf7c-sp6cc                  1/1     Running   0          5m
# flyte-sandbox-postgresql-0                            1/1     Running   0          5m
```

**3. Run all Flyte components (flyteadmin, flytepropeller, datacatalog, flyteconsole, etc) in a single binary.**

The [Flyte repository](https://github.com/flyteorg/flyte) includes Go code that integrates all Flyte components into a single binary.

``` shell
# Step 1: Clone flyte repo
git clone https://github.com/flyteorg/flyte.git
cd flyte

# Step 2: Build a single binary that bundles all the Flyte components.
# The version of each component/library used to build the single binary are defined in `go.mod`.
sudo apt-get -y install jq # You may need to install jq
make clean # (Optional) Run this only if you want to run the newest version of flyteconsole
make go-tidy
make compile

# Step 3: Prepare a namespace template for the cluster resource controller.
# The configuration file "flyte-single-binary-local.yaml" has an entry named cluster_resources.templatePath.
# This entry needs to direct to a directory containing the templates for the cluster resource controller to use.
# We will now create a simple template that allows the automatic creation of required namespaces for projects.
# For example, with Flyte's default project "flytesnacks", the controller will auto-create the following namespaces:
# flytesnacks-staging, flytesnacks-development, and flytesnacks-production.
mkdir $HOME/.flyte/sandbox/cluster-resource-templates/
echo "apiVersion: v1
kind: Namespace
metadata:
  name: '{{ namespace }}'" > $HOME/.flyte/sandbox/cluster-resource-templates/namespace.yaml

# Step 4: Running the single binary.
# The POD_NAMESPACE environment variable is necessary for the webhook to function correctly.
# You may encounter an error due to `ERROR: duplicate key value violates unique constraint`. Running the command again will solve the problem.
POD_NAMESPACE=flyte flyte start --config flyte-single-binary-local.yaml
# All logs from flyteadmin, flyteplugins, flytepropeller, etc. will appear in the terminal.
```

**4. Build single binary with your own code.**

The following instructions provide guidance on how to build single binary with your customized code under the `flyteadmin` as an example.

- **Note** Although we\'ll use `flyteadmin` as an example, these steps can be applied to other Flyte components or libraries as well.
  `{flyteadmin}` below can be substituted with other Flyte components/libraries: `flyteidl`, `flyteplugins`, `flytepropeller`, `datacatalog`, or `flytestdlib`.
- **Note** If you want to learn how flyte compiles those components and replace the repositories, you can study how `go mod edit` works.

``` shell
# Step 1: Install Go. Flyte uses Go 1.19, so make sure to switch to Go 1.19.
export PATH=$PATH:$(go env GOPATH)/bin
go install golang.org/dl/go1.19@latest
go1.19 download
export GOROOT=$(go1.19 env GOROOT)
export PATH="$GOROOT/bin:$PATH"

# You may need to install goimports to fix lint errors.
# Refer to https://pkg.go.dev/golang.org/x/tools/cmd/goimports
go install golang.org/x/tools/cmd/goimports@latest
export PATH=$(go env GOPATH)/bin:$PATH

# Step 2: Go to the {flyteadmin} repository, modify the source code accordingly.
cd flyte/flyteadmin

# Step 3: Now, you can build the single binary. Go back to Flyte directory.
make go-tidy
make compile
POD_NAMESPACE=flyte flyte start --config flyte-single-binary-local.yaml
```

**5. Test by running a hello world workflow.**

``` shell
# Step 1: Install flytekit
pip install flytekit && export PATH=$PATH:/home/ubuntu/.local/bin

# Step 2: Run a hello world example
pyflyte run --remote https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/basics/basics/hello_world.py  hello_world_wf
# Go to http://localhost:30080/console/projects/flytesnacks/domains/development/executions/fd63f88a55fed4bba846 to see execution in the console.
# You can go to the [flytesnacks repository](https://github.com/flyteorg/flytesnacks) to see more useful examples.
```

**6. Tear down the k3s cluster after finishing developing.**

``` shell
flytectl demo teardown
# context removed for "flyte-sandbox".
# 🧹 🧹 Sandbox cluster is removed successfully.
# ❇️ Run the following command to unset sandbox environment variables for accessing flytectl
#        unset FLYTECTL_CONFIG
```

### How to setup dev environment for flytekit?

**1. Set up local Flyte Cluster.**

If you are also modifying the code for flyteidl, flyteadmin, flyteplugins, flytepropeller datacatalog, or flytestdlib, refer to the instructions in the
[previous section](#how-to-setup-dev-environment-for-flyteidl-flyteadmin-flyteplugins-flytepropeller-datacatalog-and-flytestdlib)
to set up a local Flyte cluster.

If not, we can start backends with a single command.

``` shell
# Step 1: Install the latest version of flytectl, a portable and lightweight command-line interface to work with Flyte.
curl -sL https://ctl.flyte.org/install | bash
# flyteorg/flytectl info checking GitHub for latest tag
# flyteorg/flytectl info found version: 0.6.39 for v0.6.39/Linux/x86_64
# flyteorg/flytectl info installed ./bin/flytectl

# Step 2: Export flytectl path based on the previous log "flyteorg/flytectl info installed ./bin/flytectl"
export PATH=$PATH:/home/ubuntu/bin # replace with your path

# Step 3: Starts the Flyte demo cluster. This will setup a k3s cluster running minio, postgres Pods, and all Flyte components: flyteadmin, flyteplugins, flytepropeller, etc.
# See https://docs.flyte.org/en/latest/flytectl/gen/flytectl_demo_start.html for more details.
flytectl demo start
# 👨‍💻 Flyte is ready! Flyte UI is available at http://localhost:30080/console 🚀 🚀 🎉
# ❇️ Run the following command to export demo environment variables for accessing flytectl
#         export FLYTECTL_CONFIG=/home/ubuntu/.flyte/config-sandbox.yaml
# 🐋 Flyte sandbox ships with a Docker registry. Tag and push custom workflow images to localhost:30000
# 📂 The Minio API is hosted on localhost:30002. Use http://localhost:30080/minio/login for Minio console
```

**2. Run workflow locally.**

``` shell
# Step 1: Build a virtual environment for developing Flytekit. This will allow your local changes to take effect when the same Python interpreter runs `import flytekit`.
git clone https://github.com/flyteorg/flytekit.git # replace with your own repo
cd flytekit
virtualenv ~/.virtualenvs/flytekit
source ~/.virtualenvs/flytekit/bin/activate
make setup
pip install -e .

# If you are also developing the plugins, consider the following:

# Installing Specific Plugins:
# If you wish to only use few plugins, you can install them individually.
# Take [Flytekit BigQuery Plugin](https://github.com/flyteorg/flytekit/tree/master/plugins/flytekit-bigquery#flytekit-bigquery-plugin) for example:
# You have to go to the bigquery plugin folder and install it.
cd plugins/flytekit-bigquery/
pip install -e .
# Now you can use the bigquery plugin, and the performance is fast.

# (Optional) Installing All Plugins:
# If you wish to install all available plugins, you can execute the command below.
# However, it's not typically recommended because the current version of plugins does not support
# lazy loading. This can lead to a slowdown in the performance of your Python engine.
cd plugins
pip install -e .
# Now you can use all plugins, but the performance is slow.

# Step 2: Modify the source code for flytekit, then run unit tests and lint.
make lint
make test

# Step 3: Run a hello world sample to test locally
pyflyte run https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/basics/basics/hello_world.py hello_world_wf
# Running hello_world_wf() hello world
```

**3. Run workflow in sandbox.**

Before running your workflow in the sandbox, make sure you're able to successfully run it locally.
To deploy the workflow in the sandbox, you'll need to build a Flytekit image.
Create a Dockerfile in your Flytekit directory with the minimum required configuration to run a task, as shown below.
If your task requires additional components, such as plugins, you may find it useful to refer to the construction of the
[official flytekit image](https://github.com/flyteorg/flytekit/blob/master/Dockerfile)

``` Dockerfile
FROM python:3.9-slim-buster
USER root
WORKDIR /root
ENV PYTHONPATH /root
RUN apt-get update && apt-get install build-essential -y
RUN apt-get install git -y
# The following line is an example of how to install your modified plugins. In this case, it demonstrates how to install the 'deck' plugin.
# RUN pip install -U git+https://github.com/Yicheng-Lu-llll/flytekit.git@"demo#egg=flytekitplugins-deck-standard&subdirectory=plugins/flytekit-deck-standard" # replace with your own repo and branch
RUN pip install -U git+https://github.com/Yicheng-Lu-llll/flytekit.git@demo # replace with your own repo and branch
ENV FLYTE_INTERNAL_IMAGE "localhost:30000/flytekit:demo" # replace with your own image name and tag
```

The instructions below explain how to build the image, push the image to
the Flyte cluster, and finally submit the workflow.

``` shell
# Step 1: Ensure you have pushed your changes to the remote repo
# In the flytekit folder
git add . && git commit -s -m "develop" && git push

# Step 2: Build the image
# In the flytekit folder
export FLYTE_INTERNAL_IMAGE="localhost:30000/flytekit:demo" # replace with your own image name and tag
docker build --no-cache -t  "${FLYTE_INTERNAL_IMAGE}" -f ./Dockerfile .

# Step 3: Push the image to the Flyte cluster
docker push ${FLYTE_INTERNAL_IMAGE}

# Step 4: Submit a hello world workflow to the Flyte cluster
cd flytesnacks
pyflyte run --image ${FLYTE_INTERNAL_IMAGE} --remote https://raw.githubusercontent.com/flyteorg/flytesnacks/master/examples/basics/basics/hello_world.py hello_world_wf
# Go to http://localhost:30080/console/projects/flytesnacks/domains/development/executions/f5c17e1b5640c4336bf8 to see execution in the console.
```

### How to setup dev environment for flyteconsole?

**1. Set up local Flyte cluster.**

Depending on your needs, refer to one of the following guides to set up the Flyte cluster:

- If you do not need to change the backend code, refer to the section on [How to Set Up a Dev Environment for Flytekit?](#how-to-setup-dev-environment-for-flytekit)
- If you need to change the backend code, refer to the section on
  [How to setup dev environment for flyteidl, flyteadmin, flyteplugins, flytepropeller, datacatalog and flytestdlib?](#how-to-setup-dev-environment-for-flyteidl-flyteadmin-flyteplugins-flytepropeller-datacatalog-and-flytestdlib)

**2. Start flyteconsole.**

``` shell
# Step 1: Clone the repo and navigate to the Flyteconsole folder
git clone https://github.com/flyteorg/flyteconsole.git
cd flyteconsole

# Step 2: Install Node.js 18. Refer to https://github.com/nodesource/distributions/blob/master/README.md#using-ubuntu-2.
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - &&\
sudo apt-get install -y nodejs

# Step 3: Install yarn. Refer to https://classic.yarnpkg.com/lang/en/docs/install/#debian-stable.
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update && sudo apt install yarn

# Step 4: Add environment variables
export BASE_URL=/console
export ADMIN_API_URL=http://localhost:30080
export DISABLE_AUTH=1
export ADMIN_API_USE_SSL="http"

# Step 5: Generate SSL certificate
# Note, since we will use HTTP, SSL is not required. However, missing an SSL certificate will cause an error when starting Flyteconsole.
make generate_ssl

# Step 6: Install node packages
yarn install
yarn build:types # It is fine if seeing error `Property 'at' does not exist on type 'string[]'`
yarn run build:prod

# Step 7: Start flyteconsole
yarn start
```

**3. Install the Chrome plugin:** [Moesif Origin & CORS
Changer](https://chrome.google.com/webstore/detail/moesif-origin-cors-change/digfbfaphojjndkpccljibejjbppifbc).

We need to disable
[CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) to load
resources.

    1. Activate plugin (toggle to "on")
    2. Open 'Advanced Settings':
    3. set Access-Control-Allow-Credentials: true

**4. Go to** <http://localhost:3000/console/>.

### How to access Flyte UI, minio, postgres, k3s, and endpoints?

This section presumes a local Flyte cluster is already setup. If it
isn't, refer to either:

- [How to setup dev environment for flytekit?](#how-to-setup-dev-environment-for-flytekit)
- [How to setup dev environment for flyteidl, flyteadmin, flyteplugins, flytepropeller, datacatalog and flytestdlib?](#how-to-setup-dev-environment-for-flyteidl-flyteadmin-flyteplugins-flytepropeller-datacatalog-and-flytestdlib)

**1. Access the Flyte UI.**

[Flyte UI](https://docs.flyte.org/en/latest/concepts/flyte_console.html) is a web-based user interface for Flyte
that lets you interact with Flyte objects and build directed acyclic graphs (DAGs) for your workflows.

You can access it via <http://localhost:30080/console>.

**2. Access the minio console.**

Core Flyte components, such as admin, propeller, and datacatalog, as well as user runtime containers rely on an object store (in this case, minio) to hold files.
During development, you might need to examine files such as
[input.pb/output.pb](https://docs.flyte.org/en/latest/concepts/data_management.html#serialization-time), or
[deck.html](https://docs.flyte.org/en/latest/user_guide/development_lifecycle/decks.html#id1) stored in minio.

Access the minio console at: <http://localhost:30080/minio/login>.
The default credentials are:

- Username: `minio`
- Password: `miniostorage`

**3. Access the postgres.**

FlyteAdmin and datacatalog use postgres to store persistent records, and you can interact with postgres on port `30001`.
Here is an example of using `psql` to connect:

``` shell
# Step 1: Install the PostgreSQL client.
sudo apt-get update
sudo apt-get install postgresql-client

# Step 2: Connect to the PostgreSQL server. The password is "postgres".
psql -h localhost -p 30001 -U postgres -d flyte
```

**4. Access the k3s dashboard.**

Access the k3s dashboard at [http://localhost:30080/kubernetes-dashboard](http://localhost:30080/kubernetes-dashboard).

**5. Access the endpoints.**

Service endpoints are defined in the `flyteidl` repository under the `service` directory.
You can browse them at [here](https://github.com/flyteorg/flyteidl/tree/master/protos/flyteidl/service).

For example, the endpoint for the
[ListTaskExecutions](https://github.com/flyteorg/flyteidl/blob/b219c2ab37886801039fda67d913760ac6fc4c8b/protos/flyteidl/service/admin.proto#L442)
API is:

``` shell
/api/v1/task_executions/{node_execution_id.execution_id.project}/{node_execution_id.execution_id.domain}/{node_execution_id.execution_id.name}/{node_execution_id.node_id}
```

You can access this endpoint at:

``` shell
# replace with your specific task execution parameters
http://localhost:30080/api/v1/task_executions/flytesnacks/development/fe92c0a8cbf684ad19a8/n0?limit=10000
```
