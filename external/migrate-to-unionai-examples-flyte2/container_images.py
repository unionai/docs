# container_images.py

# /// script
# dependencies = [
#    "polars",
# ]
# ///

import polars as pl

import flyte

env = flyte.TaskEnvironment(
    name="polars_image",
    image=flyte.Image.from_uv_script(
        __file__,
        name="flyte",
        registry="ghcr.io/unionai-oss",
        arch=("linux/amd64", "linux/arm64"),
    ),
)


@env.task
async def create_dataframe() -> pl.DataFrame:
    return pl.DataFrame(
        {"name": ["Alice", "Bob", "Charlie"], "age": [25, 32, 37], "city": ["New York", "Paris", "Berlin"]}
    )


@env.task
async def print_dataframe(dataframe: pl.DataFrame):
    print(dataframe)


@env.task
async def workflow():
    df = await create_dataframe()
    await print_dataframe(df)


if __name__ == "__main__":
    flyte.init_from_config("./config.yaml")
    run = flyte.run(workflow)
    print(run.name)
    print(run.url)
    run.wait(run)
