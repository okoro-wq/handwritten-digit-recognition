"""Quick manual sanity check for a trained model, without spinning up the API.

Usage:
    python predict.py path/to/digit.png

Expects a white-background, dark-stroke image (the same convention the
frontend canvas produces), not a raw MNIST-style sample.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from tensorflow import keras

MODEL_PATH = Path(__file__).resolve().parent / "mnist_model.h5"


def preprocess(image_path: Path) -> np.ndarray:
    image = Image.open(image_path).convert("L")
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    image = ImageOps.invert(image)

    array = np.asarray(image, dtype=np.float32) / 255.0
    return array.reshape(1, 28, 28, 1)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python predict.py path/to/digit.png")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"No such file: {image_path}")
        sys.exit(1)

    if not MODEL_PATH.exists():
        print(f"No trained model at {MODEL_PATH}. Run train.py first.")
        sys.exit(1)

    model = keras.models.load_model(MODEL_PATH)
    probabilities = model.predict(preprocess(image_path), verbose=0)[0]
    digit = int(np.argmax(probabilities))
    confidence = float(probabilities[digit])

    print(f"Digit: {digit}")
    print(f"Confidence: {confidence * 100:.1f}%")


if __name__ == "__main__":
    main()
