<!-- omit from toc -->
# Special Blocks and Code Generators

This site has special blocks that can be used to generate code for Union.

> You can see examples by running the dev server and visiting
> [`http://localhost:1313/__docs_builder__/shortcodes/`][demo-shortcodes]. This
> page neither shows in the menus nor in the production build.
>
> If you need instructions on how to create the local environment and get the
> `localhost:1313` server running, please refer to the [local development guide](DEVELOPER.md).

- [How to specify a "shortcode"](#how-to-specify-a-shortcode)
- [Variants](#variants)
- [Component Library](#component-library)
  - [`{{< audio >}}`](#-audio-)
  - [`{{< code >}}` (deprecated as we will inline all code)](#-code--deprecated-as-we-will-inline-all-code)
  - [`{{< grid >}}`](#-grid-)
  - [`{{< variant >}}`](#-variant-)
  - [`{{< link-card >}}`](#-link-card-)
  - [`{{< markdown >}}`](#-markdown-)
  - [`{{< multiline >}}`](#-multiline-)
  - [`{{< tabs >}}` and `{{< tab >}}`](#-tabs--and--tab-)
  - [`{{< key >}}`](#-key-)
    - [List of available keys](#list-of-available-keys)
  - [`{{< download >}}`](#-download-)
  - [`{{< docs_home >}}`](#-docs_home-)
  - [`{{< py_class_docsum >}}`, `{{< py_class_ref >}}`, and `{{< py_func_ref >}}`](#-py_class_docsum---py_class_ref--and--py_func_ref-)
  - [`{{< icon name >}}`](#-icon-name-)

## How to specify a "shortcode"

The shortcode is a string that is used to generate the HTML that is displayed.

You can specify parameters, when applicable, or have content inside it, if applicable.

> If you specify content, you have to have a close tag.

Examples:

* A shortcode that just outputs something

      {{< key product_name >}}

* A shortcode that has content inside

      {{< markdown >}}
      * You markdown
      * goes here
      {{< /markdown >}}

* A shortcode with parameters

      {{< link-card target="union-sdk" icon="workflow" title="Union SDK" >}}
      The Union SDK provides the Python API for building Union workflows and apps.
      {{< /link-card >}}

> If you're wondering why we have a `{{< markdown >}}` when we can generate markdown natively...
> it is because inside a container we need to specify what content we're rendering.

## Variants

The big difference of this site, compared to other documentation sites, is that
we generate multiple "flavors" of the documentation that are slightly different
from each other. We are calling these "variants."

When you are writing your content, and you want a specific part of the content
to be conditional to a flavor, say "BYOC", you surround that with `variant`.

> `variant` is a container, so inside you will specify what you are wrapping.
> You can wrap any of the shortcodes listed in this document.

Example:

    {{< variant serverless byoc >}}
        {{< markdown >}}
        **The quick brown fox signed up for Union!**
        {{< /markdown >}}

        {{< link-button text="Contact Us" target="https://union.ai/contact" >}}
    {{< /variant >}}

## Component Library

### `{{< audio >}}`

Generates an audio media player.

> TODO(peeter): document parameters

### `{{< code >}}` (deprecated as we will inline all code)

Includes source code from an external file.

> TODO(peeter): document parameters

### `{{< grid >}}`

Creates a fixed column grid for lining up content.

> TODO(peeter): document parameters

### `{{< variant >}}`

Filters content based on which flavor you're seeing.

> TODO(peeter): document parameters

### `{{< link-card >}}`

A floatable, clickable, navigatable card.

> TODO(peeter): document parameters

### `{{< markdown >}}`

Generates a markdown block, to be used inside containers such as `{{< dropdown >}}` or `{{< variant >}}`.

> TODO(peeter): document parameters

### `{{< multiline >}}`

Generates a multiple line, single paragraph. Useful for making a multiline table cell.

> TODO(peeter): document parameters

### `{{< tabs >}}` and `{{< tab >}}`

Generates a tab panel with content switching per tab.

> TODO(peeter): document parameters

### `{{< key >}}`

Outputs one of the pre-defined keywords.
Enables inline text that differs per-variant without using the heavy-weight `{{< variant>}}...{{< /variant >}}` construct.

Take, for example, the following:

```
The {{< key product_name >}} platform is awesome.
```

In the Flyte variant of the site this will render as:

> The Flyte platform is awesome.

While, in the BYOC, BYOK and Serverless variants of the site it will render as:

> The Union platform is awesome.

You can add keywords and specify their value, per variant, in `hugo.toml`:

```
[params.key.product_full_name]
flyte = "Flyte"
serverless = "Union Serverless"
byoc = "Union BYOC"
byok = "Union BYOK"
```

#### List of available keys

| Key               | Description                           | Example Usage (Flyte → Union)                                          |
| ----------------- | ------------------------------------- | ---------------------------------------------------------------------- |
| default_project   | Default project name used in examples | `{{< key default_project >}}` → "flytesnacks" or "default"             |
| product_full_name | Full product name                     | `{{< key product_full_name >}}` → "Flyte OSS" or "Union.ai Serverless" |
| product_name      | Short product name                    | `{{< key product_name >}}` → "Flyte" or "Union.ai"                     |
| product           | Lowercase product identifier          | `{{< key product >}}` → "flyte" or "union"                             |
| kit_name          | SDK name                              | `{{< key kit_name >}}` → "Flytekit" or "Union"                         |
| kit               | Lowercase SDK identifier              | `{{< key kit >}}` → "flytekit" or "union"                              |
| kit_as            | SDK import alias                      | `{{< key kit_as >}}` → "fl" or "union"                                 |
| kit_import        | SDK import statement                  | `{{< key kit_import >}}` → "flytekit as fl" or "union"                 |
| kit_remote        | Remote client class name              | `{{< key kit_remote >}}` → "FlyteRemote" or "UnionRemote"              |
| cli_name          | CLI tool name                         | `{{< key cli_name >}}` → "Pyflyte" or "Union"                          |
| cli               | Lowercase CLI tool identifier         | `{{< key cli >}}` → "pyflyte" or "union"                               |
| ctl_name          | Control tool name                     | `{{< key ctl_name >}}` → "Flytectl" or "Uctl"                          |
| ctl               | Lowercase control tool identifier     | `{{< key ctl >}}` → "flytectl" or "uctl"                               |
| config_env        | Configuration environment variable    | `{{< key config_env >}}` → "FLYTECTL_CONFIG" or "UNION_CONFIG"         |
| env_prefix        | Environment variable prefix           | `{{< key env_prefix >}}` → "FLYTE" or "UNION"                          |
| docs_home         | Documentation home URL                | `{{< key docs_home >}}` → "/docs/flyte" or "/docs/serverless"          |
| map_func          | Map function name                     | `{{< key map_func >}}` → "map_task" or "map"                           |
| logo              | Logo image filename                   | `{{< key logo >}}` → "flyte-logo.svg" or "union-logo.svg"              |
| favicon           | Favicon image filename                | `{{< key favicon >}}` → "flyte-favicon.ico" or "union-favicon.ico"     |

### `{{< download >}}`

Generates a download link.

Parameters:
  - `url`: The URL to download from
  - `filename`: The filename to save the file as
  - `text`: The text to display for the download link

Example:

    {{< download "/_static/public/public-key.txt" "public-key.txt" >}}

### `{{< docs_home >}}`

Produces a link to the home page of the documentation for a specific variant.

Example:

    [See this in Flyte]({{< docs_home flyte>}}/wherever/you/want/to/go/in/flyte/docs)

### `{{< py_class_docsum >}}`, `{{< py_class_ref >}}`, and `{{< py_func_ref >}}`

Helper functions to track Python classes in Flyte documentation, so we can link them to
the appropriate documentation.

Parameters:
  - name of the class
  - text to add to the link

Example:

    Please see {{< py_class_ref flyte.core.Image >}} for more details.

### `{{< icon name >}}`

Uses a named icon in the content.

Example

    [Download {{< icon download >}}](/download)

[demo-shortcodes]: http://localhost:1313/__docs_builder__/shortcodes/
