---
title:
weight: 1
variants: +flyte -serverless -byoc -byok
---

(memray_plugin)=

# Memray Profiling



Memray tracks and reports memory allocations, both in python code and in compiled extension modules.
This Memray Profiling plugin enables memory tracking on the Flyte task level and renders a memgraph profiling graph on Flyte Deck.

First, install the Memray plugin:

```bash
pip install flytekitplugins-memray
```


