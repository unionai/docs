---
title: Kubeflow MPI
layout: plugin
variants: +flyte -byoc -byok -serverless
metadata:
  title: Kubeflow MPI
  title_expanded: Flytekit Kubeflow MPI Plugin
  name: flytekitplugins-kfmpi
  version: 0.0.0+develop
  author: flyteorg
  author_email: admin@flyte.org
  description: K8s based MPI plugin for flytekit
  namespace_packages:
  - flytekitplugins
  packages:
  - flytekitplugins.kfmpi
  install_requires:
  - flytekit>=1.6.1,<2.0.0
  license: apache2
  python_requires: '>=3.9'
  classifiers:
  - 'Intended Audience :: Science/Research'
  - 'Intended Audience :: Developers'
  - 'License :: OSI Approved :: Apache Software License'
  - 'Programming Language :: Python :: 3.9'
  - 'Programming Language :: Python :: 3.10'
  - 'Topic :: Scientific/Engineering'
  - 'Topic :: Scientific/Engineering :: Artificial Intelligence'
  - 'Topic :: Software Development'
  - 'Topic :: Software Development :: Libraries'
  - 'Topic :: Software Development :: Libraries :: Python Modules'
  folder: flytekit-kf-mpi
---


This plugin uses the Kubeflow MPI Operator and provides an extremely simplified interface for executing distributed training.

To install the plugin, run the following command:

```bash
pip install flytekitplugins-kfmpi
```

## Code Example
MPI usage:
```python
    @task(
        task_config=MPIJob(
            launcher=Launcher(
                replicas=1,
            ),
            worker=Worker(
                replicas=5,
                requests=Resources(cpu="2", mem="2Gi"),
                limits=Resources(cpu="4", mem="2Gi"),
            ),
            slots=2,
        ),
        cache=True,
        requests=Resources(cpu="1"),
        cache_version="1",
    )
    def my_mpi_task(x: int, y: str) -> int:
        return x
```


Horovod Usage:
You can override the command of a replica group by:
```python
    @task(
        task_config=HorovodJob(
            launcher=Launcher(
                replicas=1,
                requests=Resources(cpu="1"),
                limits=Resources(cpu="2"),
            ),
            worker=Worker(
                replicas=1,
                command=["/usr/sbin/sshd", "-De", "-f", "/home/jobuser/.sshd_config"],
                restart_policy=RestartPolicy.NEVER,
            ),
            slots=2,
            verbose=False,
            log_level="INFO",
        ),
    )
    def my_horovod_task():
        ...
```




## Upgrade MPI Plugin from V0 to V1
MPI plugin is now updated from v0 to v1 to enable more configuration options.
To migrate from v0 to v1, change the following:
1. Update flytepropeller to v1.6.0
2. Update flytekit version to v1.6.2
3. Update your code from:
```
    task_config=MPIJob(num_workers=10),
```
to
```
    task_config=MPIJob(worker=Worker(replicas=10)),
```
