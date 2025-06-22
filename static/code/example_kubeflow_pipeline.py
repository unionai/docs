import os
import sys
import uuid
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

import kfp
import kfp.components as comp
import kfp.dsl as dsl
import kfp.v2.dsl
import kfp_tekton

from kfp_tekton import k8s_client_helper

# Unique ID for your model version
UID = str(uuid.uuid4()).split("-")[0]
# Unique ID for your pipeline version
UID2 = str(uuid.uuid4()).split("-")[0]

PIPELINE_VERSION = UID2
RUN_NAME = UID

# Pipeline Info
SERVER_NAME = f"server-<whatever you want>"
EXPERIMENT_NAME = "EXPERIMENT_NAME"  ## Write experiment name here
PIPELINE_NAME = "PIPELINE_NAME"  ## Write pipeline name here, use naming convension {resource}-{dev_input}. Look in the grading section for more details on naming your pipeline.
PIPELINE_PACKAGE = f"{PIPELINE_NAME}.zip"

# Environment and Auth
KUBEFLOW_PUBLIC_ENDPOINT_URL = "example.com"
TOKEN = os.getenv("AUTH_TOKEN")
# Name of namespace
KUBEFLOW_PROFILE_NAME = "KUBEFLOW_PROFILE_NAME"  ## Write namespace name
# Name of attached volume
PERSISTENT_VOLUME_CLAIM_NAME = "PERSISTENT_VOLUME_CLAIM_NAME"  ## Write volume name

# additional components below....

import kfp
import kfp.components as comp
import kfp.dsl as dsl
import kfp.v2.dsl


LAKEFS_DATASET = "s3://dataset/repo"


@kfp.dsl.component
def fetch_dataset(dataset, data_dir, lakefs_endpoint="https://example.com"):
    import logging
    import os
    import subprocess
    from pathlib import Path

    # LOGS
    logging.basicConfig(level=logging.INFO)

    # Assertions to help users
    assert os.getenv("AWS_ACCESS_KEY_ID") is not None, logging.info(
        "There is no AWS Key set in environment"
    )
    assert os.getenv("AWS_SECRET_ACCESS_KEY") is not None, logging.info(
        "There is no AWS Secret set in environment"
    )

    # Constants
    DOWNLOAD_DIR = data_dir
    DATASET = dataset

    loc = Path(data_dir)
    allfiles = [i for i in loc.rglob("**/*")]

    # Check for persistent version file
    if len(allfiles) > 1:
        logging.info("Data exists in target dir, skipping download.")
        logging.info(f"Downloaded data folder structure: {os.listdir(DOWNLOAD_DIR)}")
        logging.info(
            "If there is no data in your directories, check to make sure that you have the right credentials, then delete the directories that were created and have no data in them."
        )
        logging.info("Good luck and have fun modeling!")
    else:
        # Download data if not already there
        logging.info(f"No local data found. Getting data from {lakefs_endpoint}")
        command = f"aws s3 cp {DATASET} {DOWNLOAD_DIR} --debug --recursive --endpoint {lakefs_endpoint}"
        subprocess.run(
            command,
            stdout=None,
            universal_newlines=True,
            shell=True,
            check=True,
            stderr=subprocess.STDOUT,
        )
        logging.info(f"Downloaded data folder structure: {os.listdir(DOWNLOAD_DIR)}")
    return


def train_conv_model(pvc_alias: str) -> Dict[str, dict]:
    # Import all the libraries
    import datetime
    import json
    import logging
    import os
    from pathlib import Path
    from typing import Dict
    import tensorflow as tf
    from tensorflow.keras.callbacks import History
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    DATA = Path().home() / f"{pvc_alias}/"

    # Set directories on volume
    TRAINING_DIR = f"{DATA}/train"
    TEST_DIR = f"{DATA}/test"

    logging.basicConfig(level=logging.INFO)

    # Instantiate data loaders
    train = tf.keras.utils.image_dataset_from_directory(
        TRAINING_DIR, image_size=(150, 150), color_mode="rgb"
    )
    test = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR, image_size=(150, 150), color_mode="rgb"
    )
    logging.info("Data Generators built")

    # Define Model Architecture
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Rescaling(1.0 / 255, input_shape=(150, 150, 3)),
            tf.keras.layers.Conv2D(filters=64, activation="relu", kernel_size=3),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Conv2D(filters=32, activation="relu", kernel_size=3),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Conv2D(filters=16, activation="relu", kernel_size=3),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Conv2D(filters=128, activation="relu", kernel_size=3),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=512, activation="relu"),
            tf.keras.layers.Dense(units=20, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    logging.info(model.summary())

    # Add experiment tracking code here

    # Create History object for metrics logging
    history = History()

    # Fit Model
    hist = model.fit(train, validation_data=test, epochs=5, callbacks=[history])

    logging.info(hist.history)

    MODEL_DIR = "shire-clothing"

    version = 2
    export_path = os.path.join(os.sep, "data", MODEL_DIR, str(version), str(version))

    # Save model Binary
    tf.keras.models.save_model(
        model,
        export_path,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None,
    )

    # Return information from model for next stage in pipeline
    return json.dumps({"path": export_path, "metrics": hist.history})


fetch_data_op = comp.func_to_container_op(fetch_dataset, base_image="example_image")

train_model_op1 = comp.func_to_container_op(
    train_conv_model,
    base_image="https://example.com/tensorflow:latest",
    packages_to_install=["pillow", "scipy"],
)


# define pipeline
@dsl.pipeline(name=PIPELINE_NAME, description="fetch data, train model, serve model")
def workshop_pipeline():
    fetch_data_r = (
        fetch_data_op("s3://kfp-intro-bywater/cleaned-empties/", "/data/")
        .add_env_variable(
            k8s_client_helper.env_from_secret(
                ## add secrets: "AWS_ACCESS_KEY_ID", {secret name}, "AWS_ACCESS_KEY_ID"
                "AWS_ACCESS_KEY_ID",
                "kfp-intro-lakefs",
                "AWS_ACCESS_KEY_ID",
            )
        )
        .add_env_variable(
            k8s_client_helper.env_from_secret(
                ## add secrets: "AWS_ACCESS_KEY_ID", {secret name}, "AWS_ACCESS_KEY_ID"
                "AWS_SECRET_ACCESS_KEY",
                "kfp-intro-lakefs",
                "AWS_SECRET_ACCESS_KEY",
            )
        )
        .add_env_variable(
            ## add secrets: k8s_client_helper.env_from_secret("AUTH_TOKEN", {secret name}, "AUTH_TOKEN")
            k8s_client_helper.env_from_secret(
                "AUTH_TOKEN", "kfp-intro-rat", "AUTH_TOKEN"
            )
        )
        .add_pvolumes({"/data/": dsl.PipelineVolume(pvc=PERSISTENT_VOLUME_CLAIM_NAME)})
    )

    train_model_r1 = (
        train_model_op1("/data/")
        .add_pvolumes({"/data/": dsl.PipelineVolume(pvc=PERSISTENT_VOLUME_CLAIM_NAME)})
        # Control your resources by stage using these
        # If you get something in the logs along the lines of "OOM" or "SIGKILL"
        # that means you need to raise these. Only use what you need!
        .set_cpu_limit("2000m")
        .set_memory_limit("2Gi")
        .set_retry(2)
        .after(fetch_data_r)
    )


def run_pipeline(
    compiled_pipeline: kfp.dsl.pipeline,
    auth: str,
    pipeline_name: str,
    experiment_name: str,
    ns: str,
    cluster_url: Optional[str] = "https://example.com",
):
    client = kfp_tekton.TektonClient(
        host=f"{cluster_url}/pipeline",
        ssl_ca_cert="/etc/ssl/certs/ca-certificates.crt",
        existing_token=auth,
    )

    try:
        experiment = client.get_experiment(
            experiment_name=experiment_name, namespace=ns
        )
    except ValueError:
        try:
            experiment = client.create_experiment(experiment_name)
        except kfp.ApiException:
            raise Exception("Your Access Token is incorrect")

    kfp_tekton.compiler._op_to_template.RESOURCE_OP_IMAGE = (
        "https://example.com/aipipeline/kubectl-wrapper:0.8.0"
    )

    kfp_tekton.compiler._op_to_template.TEKTON_BASH_STEP_IMAGE = (
        "https://example.com/dockerhub/library/busybox:1.34.1"
    )

    kfp_tekton.compiler.TektonCompiler().compile(
        compiled_pipeline, f"{pipeline_name}.zip"
    )

    pipeline_id = client.get_pipeline_id(pipeline_name)

    if not pipeline_id:
        # upload the package to Kubeflow
        r = client.upload_pipeline(f"{pipeline_name}.zip", pipeline_name=pipeline_name)

        # update the pipeline id
        pipeline_id = r.id

    uniqueid = str(uuid.uuid4()).split("-")[0]
    pipeline_versionName = f"{pipeline_name}_{uniqueid}"
    version = client.pipeline_uploads.upload_pipeline_version(
        uploadfile=f"{pipeline_name}.zip",
        name=pipeline_versionName,
        pipelineid=pipeline_id,
    )

    run = client.run_pipeline(
        experiment.id,
        f"{pipeline_name} {uniqueid}",
        pipeline_id=pipeline_id,
        version_id=version.id,
    )

    return run


if __name__ == "__main__":
    import os
    from pathlib import Path

    assert os.getenv("AUTH_TOKEN")
    auth_rat = os.getenv("AUTH_TOKEN")

    run_pipeline(
        compiled_pipeline=workshop_pipeline,
        auth=auth_rat,
        pipeline_name=PIPELINE_NAME,
        experiment_name=EXPERIMENT_NAME,
        ns="example",
        cluster_url="https://example.com",
    )
