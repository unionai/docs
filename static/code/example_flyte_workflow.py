from flytekit import workflow, task, FlyteDirectory, ImageSpec, FlyteFile, Resources
from dataclasses import dataclass


@dataclass
class DemoModel:
    file: FlyteFile
    metrics: dict


container_image = ImageSpec(
    name="my-demo-image",
    registry="ghcr.io/<your github handle>",
    packages=["tensorflow"],
)


@task(
    container_image=container_image,
    requests=Resources(cpu=2),
    limits=Resources(mem="2Gi"),
    retries=2,
)
def train_conv_model(dataset: FlyteDirectory) -> DemoModel:
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

    dataset.download()
    # Set directories on volume
    TRAINING_DIR = f"{dataset}/train"
    TEST_DIR = f"{dataset}/test"

    # Make logging visible in Panel
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
    export_path = f"{MODEL_DIR}/{version}"
    os.makedirs(export_path, exist_ok=True)
    model_path = f"{export_path}/model.keras"
    # Save model Binary
    tf.keras.models.save_model(
        model,
        model_path,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
    )

    return DemoModel(file=FlyteFile(path=model_path), metrics=hist.history)


@workflow
def wf(
    dataset_dir: FlyteDirectory = "s3://my-demo-bucket/flower_photos",
) -> DemoModel:
    return train_conv_model(dataset=dataset_dir)
