---
title: Files and directories
weight: 5
variants: +flyte +serverless +byoc +selfmanaged
---

# Files and directories

Flyte allows you to read, write, and manipulate files and directories
and pass them across task boundaries without worrying about how the file
contents are transferred from one container to the next.

Here is an example:

```python
import asyncio
import tempfile
from pathlib import Path

import flyte
from flyte.io._dir import Dir
from flyte.io._file import File

env = flyte.TaskEnvironment(name="examples-offloaded")


@env.task
async def write_file(name: str) -> File:

    # Create a file and write some content to it
    with open("test.txt", "w") as f:
        f.write(f"hello world {name}")

    # Upload the file using flyte
    uploaded_file_obj = await File.from_local("test.txt")
    return uploaded_file_obj


@env.task
async def write_and_check_files() -> Dir:
    coros = []
    for name in ["Alice", "Bob", "Eve"]:
        coros.append(write_file(name=name))

    vals = await asyncio.gather(*coros)
    temp_dir = tempfile.mkdtemp()
    for file in vals:
        async with file.open() as fh:
            contents = fh.read()
            print(f"File {file.path} contents: {contents}")
            new_file = Path(temp_dir) / file.name
            with open(new_file, "wb") as out:  # noqa: ASYNC230
                out.write(contents)
    print(f"Files written to {temp_dir}")

    # walk the directory and ls
    for path in Path(temp_dir).iterdir():
        print(f"File: {path.name}")

    my_dir = await Dir.from_local(temp_dir)
    return my_dir


@env.task
async def check_dir(my_dir: Dir):
    print(f"Dir {my_dir.path} contents:")
    async for file in my_dir.walk():
        print(f"File: {file.name}")
        async with file.open() as fh:
            contents = fh.read()
            print(f"Contents: {contents.decode('utf-8')}")


@env.task
async def create_and_check_dir():
    my_dir = await write_and_check_files()
    await check_dir(my_dir=my_dir)


if __name__ == "__main__":
    flyte.init_auto_from_config("./config.yaml")
    run = flyte.run(create_and_check_dir)
    print(run.name)
    print(run.url)
    run.wait(run)

```
