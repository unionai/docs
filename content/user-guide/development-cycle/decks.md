---
title: Decks
weight: 22
variants: +flyte +serverless +byoc +selfmanaged
---

# Decks

Decks lets you display customized data visualizations from within your task code.
Decks are rendered as HTML and appear right in the {{< key product_name >}} UI when you run your workflow.


> [!NOTE]
> Decks is an opt-in feature; to enable it, set `enable_deck` to `True` in the task parameters.

To begin, import the dependencies:

```python
import {{< key kit_import >}}
from flytekit.deck.renderer import MarkdownRenderer
from sklearn.decomposition import PCA
import plotly.express as px
import plotly
```

> [!NOTE]
> The renderers are packaged separately from `flytekit` itself.
> To enable the `MarkdownRenderer` imported above
> you first have to install the package `flytekitplugins-deck-standard`
> in your local Python environment and include it in your `ImageSpec` (as shown below).

We create a new deck named `pca` and render Markdown content along with a
[PCA](https://en.wikipedia.org/wiki/Principal_component_analysis) plot.

Now, declare the required dependnecies in an `ImageSpec`:

{{< variant flyte >}}
{{< markdown >}}

```python
custom_image = {{< key kit_as >}}.ImageSpec(
    packages=[
        "flytekitplugins-deck-standard",
        "markdown",
        "pandas",
        "pillow",
        "plotly",
        "pyarrow",
        "scikit-learn",
        "ydata_profiling",
    ],
)
```

{{< /markdown >}}
{{< /variant >}}
{{< variant byoc selfmanaged serverless >}}
{{< markdown >}}

```python
custom_image = {{< key kit_as >}}.ImageSpec(
    packages=[
        "flytekitplugins-deck-standard",
        "markdown",
        "pandas",
        "pillow",
        "plotly",
        "pyarrow",
        "scikit-learn",
        "ydata_profiling",
    ],
    builder="union",
)
```

{{< /markdown >}}
{{< /variant >}}

Next, we define the task that will construct the figure and create the Deck:

```python
@{{< key kit_as >}}.task(enable_deck=True, container_image=custom_image)
def pca_plot():
    iris_df = px.data.iris()
    X = iris_df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    pca = PCA(n_components=3)
    components = pca.fit_transform(X)
    total_var = pca.explained_variance_ratio_.sum() * 100
    fig = px.scatter_3d(
        components,
        x=0,
        y=1,
        z=2,
        color=iris_df["species"],
        title=f"Total Explained Variance: {total_var:.2f}%",
        labels={"0": "PC 1", "1": "PC 2", "2": "PC 3"},
    )
    main_deck = {{< key kit_as >}}.Deck("pca", MarkdownRenderer().to_html("### Principal Component Analysis"))
    main_deck.append(plotly.io.to_html(fig))
```

Note the usage of `append` to append the Plotly figure to the Markdown deck.

The following is the expected output containing the path to the `deck.html` file:

```
{"asctime": "2023-07-11 13:16:04,558", "name": "flytekit", "levelname": "INFO", "message": "pca_plot task creates flyte deck html to file:///var/folders/6f/xcgm46ds59j7g__gfxmkgdf80000gn/T/flyte-0_8qfjdd/sandbox/local_flytekit/c085853af5a175edb17b11cd338cbd61/deck.html"}
```

![Union deck plot](https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/flyte_deck_plot_local.webp)

Once you execute this task on the {{< key product_name >}} instance, you can access the deck by going to the task view and clicking the _Deck_ button:

![Union deck button](https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/flyte_deck_button.png)

## Deck tabs

Each Deck has a minimum of three tabs: input, output and default.
The input and output tabs are used to render the input and output data of the task,
while the default deck can be used to creta cusom renderings such as line plots, scatter plots, Markdown text, etc.
Additionally, you can create other tabs as well.

## Deck renderers

> [!NOTE]
> The renderers are packaged separately from `flytekit` itself.
> To enable them you first have to install the package `flytekitplugins-deck-standard`
> in your local Python environment and include it in your `ImageSpec`.

### Frame profiling renderer

The frame profiling render creates a profile report from a Pandas DataFrame.

```python
import {{< key kit_import >}}
import pandas as pd
from flytekitplugins.deck.renderer import FrameProfilingRenderer


@{{< key kit_as >}}.task(enable_deck=True, container_image=custom_image)
def frame_renderer() -> None:
    df = pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})
    {{< key kit_as >}}.Deck("Frame Renderer", FrameProfilingRenderer().to_html(df=df))
```

![Frame renderer](https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/flyte_decks_frame_renderer.png)

### Top-frame renderer

The top-fram renderer renders a DataFrame as an HTML table.

```python
import {{< key kit_import >}}
from typing import Annotated
from flytekit.deck import TopFrameRenderer


@{{< key kit_as >}}.task(enable_deck=True, container_image=custom_image)
def top_frame_renderer() -> Annotated[pd.DataFrame, TopFrameRenderer(1)]:
    return pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})
```

![Top frame renderer](https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/flyte_decks_top_frame_renderer.png)

### Markdown renderer

The Markdown renderer converts a Markdown string into HTML.

```python
import {{< key kit_import >}}
from flytekit.deck import MarkdownRenderer


@{{< key kit_as >}}.task(enable_deck=True, container_image=custom_image)
def markdown_renderer() -> None:
    {{< key kit_as >}}.current_context().default_deck.append(
        MarkdownRenderer().to_html("You can install flytekit using this command: ```import flytekit```")
    )
```

![Markdown renderer](https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/flyte_decks_markdown_renderer.png)

### Box renderer

The box renderer groups rows of a DataFrame together into a
box-and-whisker mark to visualize their distribution.

Each box extends from the first quartile (Q1) to the third quartile (Q3).
The median (Q2) is indicated by a line within the box.
Typically, the whiskers extend to the edges of the box,
plus or minus 1.5 times the interquartile range (IQR: Q3-Q1).

```python
import {{< key kit_import >}}
from flytekitplugins.deck.renderer import BoxRenderer


@{{< key kit_as >}}.task(enable_deck=True, container_image=custom_image)
def box_renderer() -> None:
    iris_df = px.data.iris()
    {{< key kit_as >}}.Deck("Box Plot", BoxRenderer("sepal_length").to_html(iris_df))
```

![Box renderer](https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/flyte_decks_box_renderer.png)

### Image renderer

The image renderer converts a `FlyteFile` or `PIL.Image.Image` object into an HTML displayable image,
where the image data is encoded as a base64 string.

```python
import {{< key kit_import >}}
from flytekitplugins.deck.renderer import ImageRenderer


@{{< key kit_as >}}.task(enable_deck=True, container_image=custom_image)
def image_renderer(image: {{< key kit_as >}}.FlyteFile) -> None:
    {{< key kit_as >}}.Deck("Image Renderer", ImageRenderer().to_html(image_src=image))


@{{< key kit_as >}}.workflow
def image_renderer_wf(image: {{< key kit_as >}}.FlyteFile = "https://bit.ly/3KZ95q4",) -> None:
    image_renderer(image=image)
```

![Image renderer](https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/flyte_decks_image_renderer.png)

#### Table renderer

The table renderer converts a Pandas DataFrame into an HTML table.

```python
import {{< key kit_import >}}
from flytekitplugins.deck.renderer import TableRenderer


@{{< key kit_as >}}.task(enable_deck=True, container_image=custom_image)
def table_renderer() -> None:
    {{< key kit_as >}}.Deck(
        "Table Renderer",
        TableRenderer().to_html(df=pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]}), table_width=50),
    )
```

![Table renderer](https://raw.githubusercontent.com/flyteorg/static-resources/main/flytesnacks/user_guide/flyte_decks_table_renderer.png)


{{< variant flyte >}}
{{< markdown >}}

### Contribute to renderers

Don't hesitate to integrate a new renderer into
[renderer.py](https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-deck-standard/flytekitplugins/deck/renderer.py)
if your deck renderers can enhance data visibility.
Feel encouraged to open a pull request and play a part in enhancing the Flyte deck renderer ecosystem!

{{< /markdown >}}
{{< /variant >}}

### Custom renderers

YOU can also create your own cusome renderer.
A renderer is essentially a class with a to_html method.
Here we create custom renderer that summarizes the data from a Pandas DataFRame instead of showing raw values.

```python
class DataFrameSummaryRenderer:

    def to_html(self, df: pd.DataFrame) -> str:
        assert isinstance(df, pd.DataFrame)
        return df.describe().to_html()
```

Then we can use the Annotated type to override the default renderer of the pandas.DataFrame type:

```python
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


@task(enable_deck=True)
def iris_data(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
) -> Annotated[pd.DataFrame, DataFrameSummaryRenderer()]:
    data = px.data.iris()
    if sample_frac is not None:
        data = data.sample(frac=sample_frac, random_state=random_state)

    md_text = (
        "# Iris Dataset\n"
        "This task loads the iris dataset using the  `plotly` package."
    )
    flytekit.current_context().default_deck.append(MarkdownRenderer().to_html(md_text))
    flytekit.Deck("box plot", BoxRenderer("sepal_length").to_html(data))
    return data
```

## Streaming Decks

You can stream a Deck directly using `Deck.publish()`:

```python
import {{< key kit_import >}}

@task(enable_deck=True)
def t_deck():
    {{< key kit_as >}}.Deck.publish()
```

This will create a live deck that where you can click the refresh button and see the Deck update until the task succeeds.

### Union Deck Succeed Video
{{< youtube LJaBP0mdFeE >}}

### Union Deck Fail Video
{{< youtube xaBF6Jlzjq0 >}}
