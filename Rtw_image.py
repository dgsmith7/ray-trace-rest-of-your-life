import os
import numpy as np
from PIL import Image

class RtwImage:
    def __init__(self, image_filename=None):
        self.image_width = 0
        self.image_height = 0
        self.bytes_per_pixel = 3
        self.bytes_per_scanline = 0
        self.fdata = None  # float32 numpy array, shape (H, W, 3)
        self.bdata = None  # uint8 numpy array, shape (H, W, 3)
        if image_filename:
            self.load_with_search(image_filename)

    def load_with_search(self, image_filename):
        filename = image_filename
        imagedir = os.environ.get('RTW_IMAGES')
        search_paths = []
        if imagedir:
            search_paths.append(os.path.join(imagedir, image_filename))
        search_paths.append(filename)
        search_paths.append(os.path.join('images', filename))
        for i in range(1, 7):
            search_paths.append(os.path.join('../' * i + 'images', filename))
        for path in search_paths:
            if self.load(path):
                return
        print(f"ERROR: Could not load image file '{image_filename}'.")

    def load(self, filename):
        try:
            img = Image.open(filename).convert('RGB')
            self.image_width, self.image_height = img.size
            self.bytes_per_scanline = self.image_width * self.bytes_per_pixel
            arr = np.asarray(img).astype(np.float32) / 255.0
            self.fdata = arr
            self.convert_to_bytes()
            return True
        except Exception:
            return False

    def width(self):
        return self.image_width if self.fdata is not None else 0

    def height(self):
        return self.image_height if self.fdata is not None else 0

    def pixel_data(self, x, y):
        # Returns a bytes object of 3 RGB values for pixel (x, y), or magenta if out of bounds
        magenta = bytes([255, 0, 255])
        if self.bdata is None:
            return magenta
        x = self.clamp(x, 0, self.image_width)
        y = self.clamp(y, 0, self.image_height)
        return bytes(self.bdata[y, x])

    @staticmethod
    def clamp(x, low, high):
        return max(low, min(x, high - 1))

    @staticmethod
    def float_to_byte(value):
        if value <= 0.0:
            return 0
        if value >= 1.0:
            return 255
        return int(256.0 * value)

    def convert_to_bytes(self):
        # Converts float32 [0,1] data to uint8 [0,255]
        if self.fdata is None:
            self.bdata = None
            return
        arr = np.clip(self.fdata, 0.0, 1.0)
        self.bdata = (arr * 255.0 + 0.5).astype(np.uint8)
