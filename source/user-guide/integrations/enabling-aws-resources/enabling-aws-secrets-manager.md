# Enabling AWS Secrets Manager

```{note}
This documentation is for customers who must use AWS Secrets Manager for organizational reasons. For everyone else, we strongly recommend using the [Union secrets manager](../../development-cycle/managing-secrets.md) to manage secrets rather than AWS Secrets Manager.
```

To enable your code to access secrets from AWS Secrets Manager you will need to

* Make sure AWS Secrets Manager is enabled.
* Create your secrets in AWS Secrets Manager.
* Create an AWS policy granting access to your secrets.
* Bind that policy to the User Flyte Role in your Union data plane.
* Retrieve your secrets from within your Flyte code.

## Ensure that AWS Secrets Manager is enabled

The first step is to make sure that AWS Secrets Manager is enabled in your AWS environment.
Contact the Union team if you are unsure.

## Create your secrets

:::{note}
Secrets must be defined within the same region as your Union data plane.
For example, if your Union data plane is located in `us-west-2`, ensure that the secrets are also in `us-west-2`.
:::

Create your secrets in **AWS Secrets Manager** (see the [AWS documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) for details):

* Go to **AWS Secrets Manager**.
* Select **Store a new secret**.
* Under **Choose Secret type**:
  * Select **Other type of secret**.
  * Select **Plaintext** (**Key/value** is not supported).
  * Enter your **secret value**.
  * For **Encryption key,** leave the default setting: `aws/secretmanager`.
  * Select **Next**.
* Under **Configure secret**:
  * For **Secret name**, enter a string (this string will form part of the `SECRET_KEY` that you will use to access your secret from within your Flyte code).
  * Select **Next**.
* Under **Configure rotation** adjust the settings if needed, or skip the section if not. Then select **Next**.
* Under **Review** check that everything is correct and then select **Store**.

## Get the secret ARN

Once you have created a secret, navigate to **AWS Secrets Manager > Secrets** and select the secret you just created.
From there select **Secret ARN** and record the ARN.
Do this for each secret that you create.

A secret ARN looks like this:

```{code-block} shell
arn:aws:secretsmanager:<Region>:<AccountId>:secret:<SecretName>-<SixRandomCharacters>
```

:::{note}
You will need your secret ARN when you access your secret from within your code.
Specifically, you will need to divide it into two strings:

* **`SECRET_GROUP`**: The part of the ARN up to and including `:secret:`
Above, it is `arn:aws:secretsmanager:<Region>:<AccountId>:secret:`.

* **`SECRET_KEY`**: The part of the ARN after `:secret:`
Above, it is `<SecretName>-<SixRandomCharacters>`.

See [Using AWS secrets in your Flyte code](./enabling-aws-secrets-manager.md#using-aws-secrets-in-your-flyte-code) for details on how these are used.
:::

## Create a policy providing access to your secrets

To provide access to your newly created secrets in your code, you will first need to create a policy that grants read access to those secrets:

* Go to **IAM > Access management > Policies**.
* Select **Create Policy**.
* Open the **JSON** tab and paste in the following definition:

```{code-block} json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:<Region>:<AccountId>:secret:*"
    }
  ]
}
```

:::{note}
The`Resource`entry takes a wildcard string that must match the ARNs of the secrets in your environment that you want to grant access to.
This can be all the secrets in your environment (as shown above) or some subset (achieved by making the wildcard match more specific).
Be sure to substitute the appropriate`<Region>`and`<AccountNumber>`.
:::

* Select **Next: Tags** and add tags if you wish.
* Select **Next: Review** and enter a **Name** for the policy
* Select **Create Policy**.
* Find your newly created policy in the policy list that comes up next and select it.
* Record the **Policy Name** and **Policy ARN** of your newly created policy.
It should be at the top of the policy summary page.
We will refer to the name as `<SecretManagerPolicyName>` and the ARN as `<SecretManagerPolicyArn>`.

:::{note}
Alternatively, you can create the policy from the command line like this (remember to substitute the`<Region>`and`<AccountId>`appropriately):

```{code-block} shell
$ aws iam create-policy \
      --policy-name <YourPolicyName> \
      --policy-document \
      { \
        "Version": "2012-10-17", \
        "Statement": [ \
          { \
            "Effect": "Allow", \
            "Action": "secretsmanager:GetSecretValue", \
            "Resource": "arn:aws:secretsmanager:<Region>:<AccountId>:secret:*" \
          } \
        ]\
      }
```
:::

## Bind the policy to the User Flyte Role

To grant your code the permissions defined in the policy above, you must bind that policy to the `<UserFlyteRole>` used in your Union data plane.
The precise name of this role differs by organization.
You will need this name as well as the ARN of the policy (`<SecretManagerPolicyArn>`, above) to perform the binding.
See [here](./index.md) for directions. Once the binding is done, your secrets are now accessible from within your Flyte code.

## Using AWS secrets in your Flyte code

To use an AWS secret in your Flyte task code, do the following:

* Define a `Secret` class using the `SECRET_GROUP` and `SECRET_KEY` derived from the secret ARN, above, and pass it in the `secret_requests` parameter of the `@task` decorator.
* Inside the task code, retrieve the value of the secret with a call to\
  `flytekit.current_context().secrets.get(SECRET_GROUP, SECRET_KEY)`.

Here is an example:

```{code-block} python

from flytekit import task, workflow
from flytekit import Secret
import flytekit

SECRET_GROUP = "arn:aws:secretsmanager:<Region>:<AccountId>:secret:"
SECRET_KEY = "<SecretName>-<SixRandomCharacters>"
SECRET_REQUEST = Secret(
  group=SECRET_GROUP,
  key=SECRET_KEY,
  mount_requirement=Secret.MountType.FILE
)

@task(secret_requests=[SECRET_REQUEST])
def t1():
    secret_val = flytekit.current_context().secrets.get(
        SECRET_GROUP,
        group_version=SECRET_GROUP_VERSION
    )
    # do something with the secret. For example, communication with an external API.
    ...
```

```{warning}
Do not return secret values from tasks, as this will expose secrets to the control plane.
```
