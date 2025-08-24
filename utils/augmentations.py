import cv2
import numpy as np
import random

def apply_blur(image, config):
    """Applies Gaussian blur to the image."""
    k_size_range = config['kernel_size_range']
    k_size = random.randrange(k_size_range[0], k_size_range[1] + 1, 2)
    return cv2.GaussianBlur(image, (k_size, k_size), 0)

def apply_tilt(image, config):
    """Applies a horizontal tilt (shear) to the image."""
    angle = random.uniform(*config['angle_range'])
    
    # create a transformation matrix.
    m = np.tan(np.deg2rad(angle)) 
    h, w, _ = image.shape
    matrix = np.float32([[1, m, 0], [0, 1, 0]])
    
    # calculate the new width and apply the warp affine transformation 
    return cv2.warpAffine(image, matrix, (int(w + h * abs(m)), h))

def apply_warp(image, config):
    """Applies a perspective warp to the image."""
    h, w, _ = image.shape
    magnitude = config['magnitude']

    # define the og corners of the image.
    src_points = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

    # define the 4 destination points with random shifts.
    dx1, dy1 = random.uniform(-magnitude, magnitude), random.uniform(-magnitude, magnitude)
    dx2, dy2 = random.uniform(-magnitude, magnitude), random.uniform(-magnitude, magnitude)
    dst_points = np.float32([
        [0 + dx1, 0 + dy1],             # Top-left
        [w - dx2, 0 + dy2],             # Top-right
        [0 + dx1, h - dy1],             # Bottom-left
        [w - dx2, h - dy2]              # Bottom-right
    ])
    
    # get the perspective transformation matrix and apply it.
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    return cv2.warpPerspective(image, matrix, (w, h))

def apply_brightness_contrast(image, config):
    """Adjusts brightness and contrast."""
    brightness = random.uniform(*config['brightness_range'])
    contrast = random.uniform(*config['contrast_range'])

    # convert brightness from [-1, 1] range to [-255, 255]
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness * 255)

def apply_noise(image, config):
    """Applies salt-and-pepper noise to the image."""
    if config['type'] != 's&p':
        return image

    output = np.copy(image) # creating a copy of the image
    h, w, _ = output.shape
    amount = random.uniform(*config['amount_range'])
    
    num_salt = int(np.ceil(amount * (h * w) * 0.5))
    coords = [np.random.randint(0, i - 1, num_salt) for i in (h, w)]
    output[coords[0], coords[1], :] = (255, 255, 255) # Set the pixels at these coordinates to white

    num_pepper = int(np.ceil(amount * (h * w) * 0.5))
    coords = [np.random.randint(0, i - 1, num_pepper) for i in (h, w)]
    output[coords[0], coords[1], :] = (0, 0, 0) # Set the pixels at these coordinates to black

    return output