{{- $base := site.BaseURL -}}

Once you have a Union account, install `union`:
```shell
pip install union
{{ if .packages }}
# You will also need to install the following packages...
pip install {{ delimit .packages " " }}
{{ end }}
```
{{ if .setup }}
Please run the following setup commands:
```shell
{{ delimit .setup "\n" }}
```
{{ end }}

{{ if .secrets }}
Please set the following secrets below.

```shell
{{ range .secrets -}}
union create secret --name {{ . }} --value "your-secret-value"
{{ end }}
```

> For more information on secrets, please refer to the
> [Managing Secrets]({{ urls.JoinPath $base "user-guide/development-cycle/managing-secrets/" }})
> documentation.

{{ end }}

{{ if .registry }}
Export the following environment variable to build and push
images to your own container registry:

```shell
# replace with your registry name
export IMAGE_SPEC_REGISTRY="<your-container-registry>"
```
{{ end }}

Then run the following commands to run the workflow:

```shell
{{ delimit .run_pre "\n" }}
{{ .run_cmd }}
```
