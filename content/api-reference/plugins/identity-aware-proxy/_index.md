---
title: Google IAP
layout: plugin
variants: +flyte -byoc -selfmanaged -serverless
metadata:
  title: Google IAP
  title_expanded: Flytekit Identity Aware Proxy
  name: flytekitplugins-identity_aware_proxy
  version: 0.0.0+develop
  author: flyteorg
  author_email: admin@flyte.org
  description: External command plugin to generate ID tokens for GCP Identity Aware
    Proxy
  url: https://github.com/flyteorg/flytekit/tree/master/plugins/flytekit-identity-aware-proxy
  long_description: "External command plugin to generate ID tokens for GCP Identity Aware"
  long_description_content_type: text/markdown
  namespace_packages:
  - flytekitplugins
  packages:
  - flytekitplugins.identity_aware_proxy
  entry_points:
    console_scripts:
    - flyte-iap=flytekitplugins.identity_aware_proxy.cli:cli
  install_requires:
  - click
  - google-cloud-secret-manager
  - google-auth
  - flytekit>=1.10
  - grpcio>=1.62.0
  license: apache2
  python_requires: '>=3.8'
  classifiers:
  - 'Intended Audience :: Science/Research'
  - 'Intended Audience :: Developers'
  - 'License :: OSI Approved :: Apache Software License'
  - 'Programming Language :: Python :: 3.8'
  - 'Programming Language :: Python :: 3.9'
  - 'Programming Language :: Python :: 3.10'
  - 'Topic :: Scientific/Engineering'
  - 'Topic :: Scientific/Engineering :: Artificial Intelligence'
  - 'Topic :: Software Development'
  - 'Topic :: Software Development :: Libraries'
  - 'Topic :: Software Development :: Libraries :: Python Modules'
  folder: flytekit-identity-aware-proxy
---


[GCP Identity Aware Proxy (IAP)](https://cloud.google.com/iap) is a managed Google Cloud Platform (GCP) service that makes it easy to protect applications deployed on GCP by verifying user identity and using context to determine whether a user should be granted access. Because requests to applications protected with IAP first have to pass IAP before they can reach the protected backends, IAP provides a convenient way to implement a zero-trust access model.

This flytekit plugin allows users to generate ID tokens via an external command for use with Flyte deployments protected with IAP. A step by step guide to protect a Flyte deployment with IAP is provided as well.

**Disclaimer: Do not choose this deployment path with the goal of *a* Flyte deployment configured with authentication on GCP. The deployment is more involved than the standard Flyte GCP deployment. Follow this guide if your organization has a security policy that requires the use of GCP Identity Aware Proxy.**

## Configuring the token generation CLI provided by this plugin

1. Install this plugin via `pip install flytekitplugins-identity-aware-proxy`.

    Verify the installation with `flyte-iap --help`.

2. Create OAuth 2.0 credentials for both the token generation CLI and for IAP.
    1. [Desktop OAauth credentials](https://cloud.google.com/iap/docs/authentication-howto#authenticating_from_a_desktop_app) for this CLI:

        In the GCP cloud console navigate to *"Apis & Services" / "Credentials"* click *"Create Credentials"*, select "*OAuth Client ID*", and finally choose *“Desktop App”*.

        Note the client id and client secret.

    2. Follow the instructions to [activate IAP](https://cloud.google.com/iap/docs/enabling-kubernetes-howto#enabling_iap) in your project and cluster. In the process you will create web application type OAuth credentials for IAP (similar as done above for the desktop application type credentials). Again, note the client id and client secret. Don't proceed with the instructions to create the Kubernetes secret for these credentials and the backend config yet, this is done in the deployment guide below. Stop when you have the client id and secret.

        Note: In case you have an existing [Flyte deployment with auth configured](https://docs.flyte.org/en/latest/deployment/configuration/auth_setup.html#apply-oidc-configuration), you likely already have web application type OAuth credentials. You can reuse those credentials for Flyte's IAP.

3. The token generation CLI provided by this plugin requires 1) the desktop application type client id and client secret to issue an ID token for IAP as well as 2) the client id (not the secret) of the web app type credentials that will be used by IAP (as the audience of the token).

    The desktop client secret needs to be kept secret. Therefore, create a GCP secret manager secret with the desktop client secret.

    Note the name of the secret and the id of the GCP project containing the secret.

    (You will have to grant users that will use the token generation CLI access to the secret.)

4. Test the token generation CLI:

    ```console
    flyte-iap generate-user-id-token \
        --desktop_client_id < fill in desktop client id> \
        --desktop_client_secret_gcp_secret_name <fill in the secret name > \
        --webapp_client_id < fill in the web app client id> \
        --project < fill in the gcp project id where the secret was saved >
    ```

    A browser window should open, asking you to login with your GCP account. Then, a successful log in should be confirmed with *"Successfully logged into accounts.google.com"*.

    Finally, the token beginning with `eyJhbG..."` should be printed to the console.

    You can decode the token with:

    ```console
    jq -R 'split(".") | select(length > 0) | .[0],.[1] | @base64d | fromjson' <<< "eyJhbG..."
    ```

    The token should be issued by `"https://accounts.google.com"`, should contain your email, and should have the desktop client id set as `"azp"` and the web app client id set as `"aud"` (audience).

5. Configure proxy authorization with this CLI in `~/.flyte/config.yaml`:

    ```yaml
    admin:
      endpoint: dns:///<fill in your flyte domain >.com
      insecure: false
      insecureSkipVerify: true
      authType: Pkce
      proxyCommand: ["flyte-iap", "generate-user-id-token", "--desktop_client_id", ...]  # Add this line
    ```

    This configures the Flyte clients to send `"proxy-authorization"` headers with the token generated by the CLI with every request in order to pass the GCP Identity Aware Proxy.

  6. For registering workflows from CICD, you might have to generate ID tokens for GCP service accounts instead of user accounts. For this purpose, you have the following options:
      * `flyte-iap` provides a second sub command called `generate-service-account-id-token`. This subcommand uses either a service account key json file to obtain an ID token or alternatively obtains one from the metadata server when being run on GCP Compute Engine, App Engine, or Cloud Run. It caches tokens and only obtains a new one when the cached token is about to expire.
      * If you want to avoid a flytekit/python dependency in your CICD systems, you can use the `gcloud` sdk:

        ```
        gcloud auth print-identity-token --token-format=full  --audiences="<webapp client id used by IAP>.apps.googleusercontent.com"
        ```
      * Adapt [this bash script](https://cloud.google.com/iap/docs/authentication-howto#obtaining_an_oidc_token_from_a_local_service_account_key_file) from the GCP Identity Aware Proxy documentation which retrieves a token in exchange for service account credentials. (You would need to replace the `curl` command in the last line with `echo $ID_TOKEN`.)

## Configuring your Flyte deployment to use IAP

### Introduction

To protect your Flyte deployment with IAP, we have to deploy it with a GCE ingress (instead of the Nginx ingress used by the default Flyte deployment).

Flyteadmin has a gRPC endpoint. The gRPC protocol requires the use of http2. When using http2 between a GCP load balancer (created by the GCE ingress) and a backend in GKE, the use of TLS is required ([see documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/ingress-http2)):

> To ensure the load balancer can make a correct HTTP2 request to your backend, your backend must be configured with SSL.

The following deployment guide follows [this](https://cloud.google.com/architecture/exposing-service-mesh-apps-through-gke-ingress) reference architecture for the Istio service mesh on Google Kubernetes Engine.

We will configure an Istio ingress gateway (pod) deployed behind a GCP load balancer to use http2 and TLS (see [here](https://cloud.google.com/architecture/exposing-service-mesh-apps-through-gke-ingress#security)):

> you can enable HTTP/2 with TLS encryption between the cluster ingress [...] and the mesh ingress (the envoy proxy instance). When you enable HTTP/2 with TLS encryption for this path, you can use a self-signed or public certificate to encrypt traffic [...]

Flyte is then deployed behind the Istio ingress gateway and does not need to be configured to use TLS itself.

*Note that we do not do this for security reasons but to enable http2 traffic (required by gRPC) into the cluster through a GCE Ingress (which is required by IAP).*

### Deployment

1. If not already done, deploy the flyte-core helm chart, [activating auth](https://docs.flyte.org/en/latest/deployment/configuration/auth_setup.html#apply-oidc-configuration). Reuse the web app client id created for IAP (see section above). Disable the default ingress in the helm values by setting `common.ingress.enabled` to `false` in the helm values file.


2. Deployment of Istio and the Istio ingress gateway ([docs](https://istio.io/latest/docs/setup/install/helm/))

    * `helm repo add istio https://istio-release.storage.googleapis.com/charts`
    * `helm repo update`
    * `kubectl create namespace istio-system`
    * `helm install istio-base istio/base -n istio-system`
    * `helm install istiod istio/istiod -n istio-system --wait`
    * `helm install istio-ingress istio/gateway -n istio-system -f istio-values.yaml --wait`

    Here, `istio-values.yaml` contains the following:

    ```yaml
    service:
      annotations:
        beta.cloud.google.com/backend-config: '{"default": "ingress-backend-config"}'
        cloud.google.com/app-protocols: '{"https": "HTTP2"}'
      type:
        NodePort
    ```

    It is crucial that the service type is set to `NodePort` and not the default `LoadBalancer`. Otherwise, the Istio ingress gateway won't be deployed behind the GCP load balancer we create below but would be **publicly available on the internet!**

    With the annotations we configured the service to use http2 which is required by gRPC. We also configured the service to use a so-called backend config `ingress-backend-config` which activates IAP and which we will create in the next step.


3. Activate IAP for the Istio ingress gateway via a backend config:

    Create a Kubernetes secret containing the web app client id and secret we created above. The creation of the secret is described [here](https://cloud.google.com/iap/docs/enabling-kubernetes-howto#kubernetes-configure). From now on the assumption is that the secret is called `iap-oauth-client-id`.

    Create a backend config for the Istio ingress gateway:

    ```yaml
    apiVersion: cloud.google.com/v1
    kind: BackendConfig
    metadata:
      name: ingress-backend-config
      namespace: istio-system
    spec:
      healthCheck:
        port: 15021
        requestPath: /healthz/ready
        type: HTTP
      iap:
        enabled: true
        oauthclientCredentials:
          secretName: iap-oauth-client-id
    ```

    Note that apart from activating IAP, we also configured a custom health check as the istio ingress gateway doesn't use the default health check path and port assumed by the GCP load balancer.


4. [Install Cert Manager](https://cert-manager.io/docs/installation/helm/) to [create and rotate](https://cert-manager.io/docs/configuration/selfsigned/) a self-signed certificate for the istio ingress (pod):

    * `helm repo add jetstack https://charts.jetstack.io`
    * `helm repo update`
    * `helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true`

    Create the following objects:

    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Issuer
    metadata:
      name: selfsigned-issuer
      namespace: istio-system
    spec:
      selfSigned: {}
    ```

    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Certificate
    metadata:
      name: istio-ingress-cert
      namespace: istio-system
    spec:
      commonName: istio-ingress
      dnsNames:
      - istio-ingress
      - istio-ingress.istio-system.svc
      - istio-ingress.istio-system.svc.cluster.local
      issuerRef:
        kind: Issuer
        name: selfsigned-issuer
      secretName: istio-ingress-cert
    ```

    This self-signed TLS certificate is only used between the GCP load balancer and the istio ingress gateway. It is not used by the istio ingress gateway to terminate TLS connections from the outside world (as we created it using a `NodePort` type service). Therefore, it is not unsafe to use a self-signed certificate here. Many applications deployed on GKE don't use any additional encryption between the load balancer and the backend. GCP, however, [encrypts these connections by default](https://cloud.google.com/load-balancing/docs/backend-service#encryption_between_the_load_balancer_and_backends):

      > The next hop, which is between the Google Front End (GFE) and the mesh ingress proxy, is encrypted by default. Network-level encryption between the GFEs and their backends is applied automatically. However, if your security requirements dictate that the platform owner retain ownership of the encryption keys, then you can enable HTTP/2 with TLS encryption between the cluster ingress (the GFE) and the mesh ingress (the envoy proxy instance).

    This additional self-managed encryption is also required to use http2 and in extension gRPC. To repeat, we mainly add this self-signed certificate in order to be able to expose a gRPC service (flyteadmin) via a GCP load balancer, less for the additional encryption.


5. Configure the istio ingress gateway to use the self-signed certificate:


    ```yaml
    apiVersion: networking.istio.io/v1beta1
    kind: Gateway
    metadata:
      name: default-gateway
      namespace: istio-system
    spec:
      selector:
        app: istio-ingress
        istio: ingress
      servers:
      - hosts:
        - '*'
        port:
          name: https
          number: 443
          protocol: HTTPS
        tls:
          credentialName: istio-ingress-cert
          mode: SIMPLE
    ```

    (Note that the `credentialName` matches the `secretName` in the `Certificate` we created.)

    This `Gateway` object configures the Istio ingress gateway (pod) to use the self-signed certificate we created above for every incoming TLS connection.


6. Deploy the GCE ingress that will route traffic to the istio ingress gateway:


    * Create a global (not regional) static IP address in GCP as is described [here](https://cloud.google.com/kubernetes-engine/docs/how-to/managed-certs#prerequisites).
    * Create a DNS record for your Flyte domain to route traffic to this static IP address.
    * Create a GCP managed certificate (please fill in your domain):

        ```yaml
        apiVersion: networking.gke.io/v1
        kind: ManagedCertificate
        metadata:
          name: flyte-managed-certificate
          namespace: istio-system
        spec:
          domains:
            - < fill in your domain >
        ```
    * Create the ingress (please fill in the name of the static IP):

        ```yaml
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          annotations:
            kubernetes.io/ingress.allow-http: "true"
            kubernetes.io/ingress.global-static-ip-name: "< fill in >"
            networking.gke.io/managed-certificates: flyte-managed-certificate
            networking.gke.io/v1beta1.FrontendConfig: ingress-frontend-config
          name: flyte-ingress
          namespace: istio-system
        spec:
          rules:
          - http:
              paths:
              - backend:
                  service:
                    name: istio-ingress
                    port:
                      number: 443
                path: /
                pathType: Prefix
        ---
        apiVersion: networking.gke.io/v1beta1
        kind: FrontendConfig
        metadata:
          name: ingress-frontend-config
          namespace: istio-system
        spec:
          redirectToHttps:
            enabled: true
            responseCodeName: MOVED_PERMANENTLY_DEFAULT
        ```

        This ingress routes all traffic to the istio ingress gateway via http2 and TLS.

        For clarity: The GCP load balancer TLS terminates connections coming from the outside world using a GCP managed certificate.
        The self-signed certificate created above is only used between the GCP load balancer and the istio ingress gateway running in the cluster.
        To repeat, because of this it is important for security that the istio ingress gateway uses a `NodePort` type service and not a `LoadBalancer`.

    * In the GCP cloud console under *Kubernetes Engine/Services & Ingress/Ingress* (selecting the respective cluster and the `istio-system` namespace), you can observe the status of the ingress, its managed certificate, and its backends. Only proceed if all statuses are green. The creation of the GCP load balancer configured by the ingress and of the managed certificate can take up to 30 minutes during the first deployment.


7. Connect flyteadmin and flyteconsole to the istio ingress gateway:

    So far, we created a GCE ingress (which creates a GCP load balancer). The load balancer is configured to forward all requests to the istio ingress gateway at the edge of the service mesh via http2 and TLS.

    Next, we configure the Istio service mesh to route requests from the Istio ingress gateway to flyteadmin and flyteconsole.

    In istio, this is configured using a so-called `VirtualService` object.

    Please fill in your flyte domain in the following manifest and apply it to the cluster:

    ```yaml
    apiVersion: networking.istio.io/v1beta1
    kind: VirtualService
    metadata:
      name: flyte-virtualservice
      namespace: flyte
    spec:
      gateways:
      - istio-system/default-gateway
      hosts:
      - <fill in your flyte domain>
      http:
      - match:
        - uri:
            prefix: /console
        name: console-routes
        route:
        - destination:
            host: flyteconsole
            port:
              number: 80
      - match:
        - uri:
            prefix: /api
        - uri:
            prefix: /healthcheck
        - uri:
            prefix: /v1/*
        - uri:
            prefix: /.well-known
        - uri:
            prefix: /login
        - uri:
            prefix: /logout
        - uri:
            prefix: /callback
        - uri:
            prefix: /me
        - uri:
            prefix: /config
        - uri:
            prefix: /oauth2
        name: admin-routes
        route:
        - destination:
            host: flyteadmin
            port:
              number: 80
      - match:
        - uri:
            prefix: /flyteidl.service.SignalService
        - uri:
            prefix: /flyteidl.service.AdminService
        - uri:
            prefix: /flyteidl.service.DataProxyService
        - uri:
            prefix: /flyteidl.service.AuthMetadataService
        - uri:
            prefix: /flyteidl.service.IdentityService
        - uri:
            prefix: /grpc.health.v1.Health
        name: admin-grpc-routes
        route:
        - destination:
            host: flyteadmin
            port:
              number: 81
    ```

    In this `VirtualService`, the routing rules for flyteadmin and flyteconsole are configured which in Flyte's default deployment are configured in the Nginx ingress.

    Note that the virtual service references the `Gateway` object we created above which configures the istio ingress gateway to use TLS for these connections.

8. Test your Flyte deployment with IAP by e.g. executing this python script:

    ```python
    from flytekit.remote import FlyteRemote

    from flytekit.configuration import Config


    remote = FlyteRemote(
        config=Config.auto(),
        default_project="flytesnacks",
        default_domain="development",
    )


    print(remote.recent_executions())
    ```

    A browser window should open and ask you to login with your Google account. You should then see confirmation that you *"Successfully logged into accounts.google.com"* (this was for the IAP), finally followed by confirmation that you *"Successfully logged into 'your flyte domain'"* (this was for Flyte itself).



9. At this point your Flyte deployment should be successfully protected by a GCP identity aware proxy using a zero trust model.

    You should check in the GCP cloud console's *IAP* page that IAP is actually activated and configured correctly for the Istio ingress gateway (follow up on any yellow or red status symbols next to the respective backend).

    You could also open the flyte console in an incognito browser window and verify that you are asked to login with your Google account.

    Finally, you could also comment out the `proxyCommand` line in your `~/.flyte/config.yaml` and verify that you are no longer able to access your Flyte deployment behind IAP.

10. The double login observed above is due to the fact that the Flyte clients send `"proxy-authorization"` headers generated by the CLI provided by this plugin with every request in order to make it past IAP. They still also send the regular `"authorization"` header issued by flyteadmin itself.

      Since the refresh token for Flyte and the one for IAP by default don't have the same lifespan, you likely won't notice this double login  again. However, since your deployment is already protected by IAP, the ID token (issued by flyteadmin) in the `"authorization"` header mostly serves to identify users. Therefore, you can consider to increase the lifespan of the refresh token issued by flyteadmin to e.g. 7 days by setting `configmap.adminServer.auth.appAuth.selfAuthServer.refreshTokenLifespan` to e.g. `168h0m0s` in your Flyte helm values file. This way, your users should barely notice the double login.
