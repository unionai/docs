---
title: Google OpenID Connect
weight: 2
variants: -flyte -serverless +byoc -selfmanaged
---

# Google OpenID Connect

To set up your {{< key product_name >}} instance to use Google OpenID Connect as the identity provider, follow the directions below.

> [!NOTE] Google Documentation
> In this article, we cover the same steps as in the
> [OpenID Connect](https://developers.google.com/identity/openid-connect/openid-connect) Google documentation,
> but with additional directions specific to {{< key product_name >}}.

## Setting up OAuth 2.0

First, select an existing project or set up a new project in the
[Google Cloud Console](https://console.cloud.google.com).

1. Navigate to the **Clients** section for [Google Auth Platform](https://console.cloud.google.com/auth/).

2. Click **CREATE CLIENT**. If this is your first client, you might need to provide additional app details. There is no special configuration needed from the {{< key product_name >}} side.

3. Under **Create OAuth client ID**, select **Web application** as the application type and assign a name.

4. Under **Authorized redirect URIs**, add an entry with the following callback URI:
   `https://signin.hosted.unionai.cloud/oauth2/v1/authorize/callback`.

5. Click **Create**.

## Obtain OAuth 2.0 credentials

Next, retrieve your credentials: Click on your configured client and copy the values for **Client ID** and **Client secret** to a text file on your computer.

![OAuth 2.0 credentials](../../_static/images/user-guide/data-plane-setup/single-sign-on-setup/google-oidc/oauth-credentials.png)

## Share the client ID and client secret securely with {{< key product_name >}}

Finally, you will need to share the client ID and client secret securely with {{< key product_name >}}:

1. Copy the public key provided by {{< key product_name >}} here:
   {{< download "/_static/public/public-key.txt" "public-key.txt" >}}

2. Encrypt the given text file on your computer with a PGP tool of your choice.

3. Share the encrypted message with the {{< key product_name >}} team over Slack.
