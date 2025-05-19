---
title: User guide
weight: 1
variants: +flyte +serverless +byoc +byok
top_menu: true
site_root: true
sidebar_expanded: true
---

# User guide

> [!WARNING] This is the staging version of the site.
> Please visit [www.union.ai/docs](https://www.union.ai/docs) for the official
> version.

{{< variant flyte >}}
{{< markdown >}}

> [!NOTE] Flyte
> Welome to the offical documentation for the [**Flyte**](./about-flyte) open-source project.
> This documentation is maintained by Union.ai.
>
> You can switch to the documentation for the closed-source versions with the selector above.

{{< /markdown >}}
{{< /variant >}}
{{< variant serverless >}}
{{< markdown >}}

> [!NOTE] {{< key product_name >}} Serverless
> Welcome to the offical documentation for [**{{< key product_name >}} Serverless**](./about-union#union-serverless).
>
> You can switch to another product version with the selector above.

{{< /markdown >}}
{{< /variant >}}
{{< variant byoc >}}
{{< markdown >}}

> [!NOTE] {{< key product_name >}} BYOC
> Welcome to the offical documentation for [**{{< key product_name >}} BYOC**](./about-union#union-byoc).
>
> You can switch to another product version with the selector above.

{{< /markdown >}}
{{< /variant >}}
{{< variant byok >}}
{{< markdown >}}

> [!NOTE] {{< key product_name >}} BYOK
> Welcome to the offical documentation for [**{{< key product_name >}} BYOK**](./about-union#union-byok).
>
> You can switch to another product version with the selector above.

{{< /markdown >}}
{{< /variant >}}

{{< variant flyte >}}
{{< markdown>}}

Flyte is an open-source, Kubernetes-native workflow orchestrator implemented in Go.

Flyte empowers AI development teams to rapidly ship high-quality code to production by offering optimized performance, unparalleled resource efficiency, and a delightful workflow authoring experience.


{{< /markdown >}}
{{< /variant >}}
{{< variant serverless byoc byok >}}
{{< markdown>}}

The {{< key product_name >}} platform empowers AI development teams to rapidly ship high-quality code to production by offering optimized performance, unparalleled resource efficiency, and a delightful workflow authoring experience.

* Run complex AI workloads with performance, scale, and efficiency.
* Achieve millisecond-level execution times with reusable containers.
* Scale out to multiple regions, clusters, and clouds as needed for resource availability, scale or compliance.

{{< /markdown >}}
{{< /variant >}}

{{< grid >}}

{{< variant flyte >}}

{{< link-card target="about-flyte" icon="lightbulb" title="About Flyte" >}}
Flyte is the leading open-source Kubernetes-native workflow orchestrator.
{{< /link-card >}}

{{< /variant >}}
{{< variant serverless byoc byok >}}

{{< link-card target="about-union" icon="lightbulb" title="About Union.ai" >}}
{{< key product_name >}} builds on the leading open-source workflow orchestrator, Flyte, to provide a powerful, scalable, and flexible platform for AI applications.
{{< /link-card >}}

{{< /variant >}}

{{< link-card target="getting-started" icon="123" title="Getting started" >}}
Build your first {{< key product_name >}} workflow, exploring the major features of the platform along the way.
{{< /link-card >}}

{{< link-card target="core-concepts" icon="mortarboard" title="Core concepts" >}}
Understand the core concepts of the {{< key product_name >}} platform.
{{< /link-card >}}

{{< link-card target="development-cycle" icon="arrow-repeat" title="Development cycle" >}}
Explore the {{< key product_name >}} development cycle from experimentation to production.
{{< /link-card >}}

{{< link-card target="data-input-output" icon="arrow-left-right" title="Data input/output" >}}
Manage the input and output of data in your {{< key product_name >}} workflow.
{{< /link-card >}}

{{< link-card target="programming" icon="code-slash" title="Programming" >}}
Learn about {{< key product_name >}}-specific programming constructs.
{{< /link-card >}}

{{< variant byoc byok >}}

{{< link-card target="administration" icon="person-add" title="Administration" >}}
{{< key product_full_name >}} administrators can manage users, projects, and resources.
{{< /link-card >}}

{{< link-card target="integrations" icon="tools" title="Integrations" >}}
{{< key product_full_name >}} integrates with your cloud resources and external services.
{{< /link-card >}}

{{< link-card target="faq" icon="question-circle" title="FAQ" >}}
Frequently asked questions.
{{< /link-card >}}

{{< /variant >}}

{{< /grid >}}
