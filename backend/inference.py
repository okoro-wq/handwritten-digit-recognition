import base64
import io
from functools import lru_cache

import numpy as np
from PIL import Image, ImageOps

from config import settings

IMAGE_SIZE = (28, 28)


class InvalidImageError(ValueError):
    pass


@lru_cache(maxsize=1)
def get_model():
    # Imported lazily so `uvicorn --reload` doesn't pay TensorFlow's import
    # cost on every reload of unrelated modules.
    from tensorflow import keras

    if not settings.model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {settings.model_path}. Run model/train.py first."
        )
    return keras.models.load_model(settings.model_path)


def preprocess_image(data_url: str) -> np.ndarray:
    """Turn a canvas `data:image/png;base64,...` URL into a (1, 28, 28, 1) array
    matching MNIST's white-digit-on-black, [0, 1]-normalized convention."""
    try:
        _, encoded = data_url.split(",", 1)
        raw = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(raw)).convert("L")
    except Exception as exc:
        raise InvalidImageError("Could not decode the submitted image.") from exc

    image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
    image = ImageOps.invert(image)

    array = np.asarray(image, dtype=np.float32) / 255.0
    return array.reshape(1, IMAGE_SIZE[0], IMAGE_SIZE[1], 1)


def predict_digit(image_array: np.ndarray) -> tuple[int, float]:
    model = get_model()
    probabilities = model.predict(image_array, verbose=0)[0]
    digit = int(np.argmax(probabilities))
    confidence = float(probabilities[digit])
    return digit, confidence
