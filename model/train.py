"""Train a small CNN on MNIST and save it to model/mnist_model.h5.

MNIST is downloaded automatically by Keras on first run (cached in
~/.keras/datasets) -- it is not vendored in this repo.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

MODEL_DIR = Path(__file__).resolve().parent
DOCS_DIR = MODEL_DIR.parent / "docs"
EPOCHS = 8
BATCH_SIZE = 128


def load_data():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    x_train = np.expand_dims(x_train, axis=-1)
    x_test = np.expand_dims(x_test, axis=-1)

    return (x_train, y_train), (x_test, y_test)


def build_model() -> keras.Model:
    model = keras.Sequential(
        [
            keras.Input(shape=(28, 28, 1)),
            layers.Conv2D(32, kernel_size=3, activation="relu"),
            layers.Conv2D(64, kernel_size=3, activation="relu"),
            layers.MaxPooling2D(pool_size=2),
            layers.Dropout(0.25),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.5),
            layers.Dense(10, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def plot_history(history: keras.callbacks.History) -> None:
    DOCS_DIR.mkdir(exist_ok=True)

    fig, (ax_acc, ax_loss) = plt.subplots(1, 2, figsize=(10, 4))

    ax_acc.plot(history.history["accuracy"], label="train")
    ax_acc.plot(history.history["val_accuracy"], label="validation")
    ax_acc.set_title("Accuracy")
    ax_acc.set_xlabel("Epoch")
    ax_acc.legend()

    ax_loss.plot(history.history["loss"], label="train")
    ax_loss.plot(history.history["val_loss"], label="validation")
    ax_loss.set_title("Loss")
    ax_loss.set_xlabel("Epoch")
    ax_loss.legend()

    fig.tight_layout()
    fig.savefig(DOCS_DIR / "training_history.png", dpi=150)


def main() -> None:
    (x_train, y_train), (x_test, y_test) = load_data()

    model = build_model()
    model.summary()

    history = model.fit(
        x_train,
        y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_split=0.1,
    )

    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test accuracy: {test_accuracy:.4f} (loss: {test_loss:.4f})")

    model.save(MODEL_DIR / "mnist_model.h5")
    plot_history(history)
    print(f"Saved model to {MODEL_DIR / 'mnist_model.h5'}")


if __name__ == "__main__":
    main()
