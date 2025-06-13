---
title: Shortcode Examples
variants: -flyte -serverless -byoc -selfmanaged
---

# Shortcode Examples {.docs-builder .shortcodes}

## Icon

> &#123;&#123;&lt; icon "book" &gt;&#125;&#125;

### Renders as {.renders-as}

{{< icon "book" >}}

List of icons [here](https://shoelace.style/components/icon)

## Notes

> &gt; [!NOTE] This is the title
> &gt; This is the body of the note.
> &gt; It can have multiple paragraphs.

### Renders as

> [!NOTE] This is the title
> This is the body of the note.
> It can have multiple paragraphs.

## Warning

> &gt; [!WARNING] This is the title
> &gt; This is the body of the warning.
> &gt; It can also have multiple paragraphs.

### Renders as

> [!WARNING] This is the title
> This is the body of the warning.
> It can also have multiple paragraphs.

## Link Card

> &#123;&#123;&lt; link-card target="navigation" title="Navigation Tests" icon="bullseye" &gt;&#125;&#125;
> Various links to test navigation.
> &#123;&#123;&lt; /link-card &gt;&#125;&#125;

### Renders as

{{< link-card target="navigation" title="Navigation Tests" icon="bullseye" >}}
Various links to test navigation.
{{< /link-card >}}

## Grid

> &#123;&#123;&lt; grid &gt;&#125;&#125;
>
> &#123;&#123;&lt; link-card target="navigation" title="Navigation Tests" icon="bullseye" &gt;&#125;&#125;
> Various links to test navigation.
> &#123;&#123;&lt; /link-card &gt;&#125;&#125;
>
> &#123;&#123;&lt; link-card target="navigation" title="Navigation Tests" icon="bullseye" &gt;&#125;&#125;
> Various links to test navigation.
> &#123;&#123;&lt; /link-card &gt;&#125;&#125;
>
> &#123;&#123;&lt; markdown &gt;&#125;&#125;
> A container with markdown
> &#123;&#123;&lt; /markdown &gt;&#125;&#125;
>
> &#123;&#123;&lt; markdown &gt;&#125;&#125;
> Another container with markdown
> &#123;&#123;&lt; /markdown &gt;&#125;&#125;
>
> &#123;&#123;&lt; link-card target="navigation" title="Navigation Tests" icon="bullseye" &gt;&#125;&#125;
> Various links to test navigation.
> &#123;&#123;&lt; /link-card &gt;&#125;&#125;
>
> &#123;&#123;&lt; link-card target="navigation" title="Navigation Tests" icon="bullseye" &gt;&#125;&#125;
> Various links to test navigation.
> &#123;&#123;&lt; /link-card &gt;&#125;&#125;
>
> &#123;&#123;&lt; /grid &gt;&#125;&#125;

### Renders as

{{< grid >}}
{{< link-card target="navigation" title="Navigation Tests" icon="bullseye" >}}
Various links to test navigation.
{{< /link-card >}}
{{< link-card target="navigation" title="Navigation Tests" icon="bullseye" >}}
Various links to test navigation.
{{< /link-card >}}
{{< markdown >}}
A container with markdown
{{< /markdown >}}
{{< markdown >}}
Another container with markdown
{{< /markdown >}}
{{< link-card target="navigation" title="Navigation Tests" icon="bullseye" >}}
Various links to test navigation.
{{< /link-card >}}
{{< link-card target="navigation" title="Navigation Tests" icon="bullseye" >}}
Various links to test navigation.
{{< /link-card >}}
{{< /grid >}}

## Code

Code examples are integrated into the main documentation:

[Community > Contributing Docs > Shortcodes > Code](../../community/contributing-docs/shortcodes#-code-)