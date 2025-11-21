
from PIL import Image
import numpy as np
from typing import Dict, Any


def analyze_image_basic(image_path: str) -> Dict[str, Any]:
    """Very simple computer vision analysis: size, average color, brightness.

    This is meant as a lightweight demo you can later replace with a real food
    recognition / portion estimation model.
    """
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Resize to something small and compute basic stats
    small = img.resize((64, 64))
    arr = np.asarray(small) / 255.0

    avg_color = arr.mean(axis=(0, 1))  # R, G, B
    brightness = arr.mean()

    # Very rough heuristic about dish type
    r, g, b = avg_color
    if brightness > 0.7:
        dish_hint = "light-colored, likely higher in refined carbs (like rice, bread, pasta, or potatoes)"
    elif r > g and r > b:
        dish_hint = "red/orange heavy dish, possibly sauces, curries, or fried foods"
    elif g > r and g > b:
        dish_hint = "greenish dish, possibly salads or vegetables"
    else:
        dish_hint = "mixed colors, likely a combo meal with multiple components"

    return {
        "width": width,
        "height": height,
        "avg_color_rgb": {
            "r": float(avg_color[0]),
            "g": float(avg_color[1]),
            "b": float(avg_color[2]),
        },
        "brightness": float(brightness),
        "dish_hint": dish_hint,
    }
