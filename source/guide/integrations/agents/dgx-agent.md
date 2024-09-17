# NVIDIA DGX agent

You can run workflows on the [NVIDIA DGX platform](https://www.nvidia.com/en-us/data-center/dgx-platform/) with the DGX agent.


## Installation

To install the DGX agent and have it enabled in your deployment, contact the Union team.

## Example usage

```{code-block} python
from typing import List

from flytekit import task, workflow, ImageSpec
from flytekitplugins.dgx import DGXConfig


dgx_image_spec = ImageSpec(
    base_image="my-image/dgx:v24",
    packages=["torch", "transformers", "accelerate", "bitsandbytes"],
    registry="my-registry",
)


DEFAULT_CHAT_TEMPLATE = """
{% for message in messages %}
{% if message['role'] == 'user' %}
{{ '<<|user|>> ' + message['content'].strip() + ' <</s>>' }}
{% elif message['role'] == 'system' %}
{{ '<<|system|>>\\n' + message['content'].strip() + '\\n<</s>>\\n\\n' }}
{% endif %}
{% endfor %}
{% if add_generation_prompt %}{{ '<|im_start|>assistant\n' }}{% endif %}
""".strip()


@task(container_image=dgx_image_spec, cache_version="1.0", cache=True)
def form_prompt(prompt: str, system_message: str) -> List[dict]:
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]


@task(
    task_config=DGXConfig(instance="dgxa100.80g.8.norm"),
    container_image=dgx_image_spec,
)
def inference(messages: List[dict], n_variations: int) -> List[str]:
    import torch
    import transformers
    from transformers import AutoTokenizer

    print(f"gpu is available: {torch.cuda.is_available()}")

    model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    tokenizer = AutoTokenizer.from_pretrained(model)
    pipeline = transformers.pipeline(
        "text-generation",
        tokenizer=tokenizer,
        model=model,
        model_kwargs={"torch_dtype": torch.float16, "load_in_4bit": True},
    )
    print(f"{messages=}")
    prompt = pipeline.tokenizer.apply_chat_template(
        messages,
        chat_template=DEFAULT_CHAT_TEMPLATE,
        tokenize=False,
        add_generation_prompt=True,
    )
    outputs = pipeline(
        prompt,
        num_return_sequences=n_variations,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        return_full_text=False,
    )
    print(f'generated text={outputs[0]["generated_text"]}')
    return [output["generated_text"] for output in outputs]


@workflow
def wf(
    prompt: str = "Explain what a Mixture of Experts is in less than 100 words.",
    n_variations: int = 8,
    system_message: str = "You are a helpful and polite bot.",
) -> List[str]:
    messages = form_prompt(prompt=prompt, system_message=system_message)
    return inference(messages=messages, n_variations=n_variations)
```
