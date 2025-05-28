---
title: A tutorial example
weight: 9
variants: -flyte +serverless +byoc +byok
layout: py_example
example_file: /external/unionai-examples/tutorials/nvidia_blueprints/enterprise_rag/app.py
# example_origin: https://github.com/unionai/unionai-examples/blob/main/tutorials/nvidia_blueprints/enterprise_rag/app.py
# example_run_pre:
#     - git clone @@remote@@
#     - cd @@remote:base@@/@@folder@@
example_run_cmd: union run app.py
example_packages:
    - pandas
    - pydantic
    - fastapi
example_setup:
    - cd a/b/c/d
    - pip install -r requirements.txt
example_env:
    USER_NAME: "admin"
    PASSWORD: "<your-password>"
run_on_union_secrets:
    - openai_api_key
    - unionai_api_key
run_on_union_enforce: true
run_on_union_open: true
run_on_union_registry:
    - '# replace with your registry name'
    - export IMAGE_SPEC_REGISTRY="<your-container-registry>"
---