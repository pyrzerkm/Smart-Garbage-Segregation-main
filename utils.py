"""
Utility functions for waste classification model.
This module handles model architecture and image preprocessing.
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import numpy as np
from PIL import Image
import os

# Enable OneDNN optimizations for better performance
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'

# Hardcoded labels (as per requirements - no dataset dependency)
LABELS = {
    0: "cardboard",
    1: "glass",
    2: "metal",
    3: "paper",
    4: "plastic",
    5: "trash"
}

# Recyclable categories
RECYCLABLE_CATEGORIES = ['cardboard', 'glass', 'metal', 'paper', 'plastic']
OTHER_CATEGORIES = ['trash']


def preprocess(image):
    """
    Preprocess image for model input.
    
    Args:
        image: PIL Image object
        
    Returns:
        numpy array: Preprocessed image (300x300x3, normalized to [0,1])
    """
    # Resize to model input size
    image = image.resize((300, 300), Image.Resampling.LANCZOS)
    # Convert to numpy array
    image = np.array(image, dtype='uint8')
    # Normalize to [0, 1]
    image = np.array(image) / 255.0
    
    return image


def model_arc():
    """
    Create and return the CNN model architecture.
    This matches the architecture used during training.
    
    Returns:
        Compiled Keras model
    """
    model = Sequential()

    # Convolution blocks
    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', 
                     input_shape=(300, 300, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=2))

    model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=2))

    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=2))

    # Classification layers
    model.add(Flatten())

    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))

    model.add(Dropout(0.2))
    model.add(Dense(6, activation='softmax'))

    # Compile model
    model.compile(optimizer='adam', 
                 loss='sparse_categorical_crossentropy', 
                 metrics=['accuracy'])

    return model


def load_model(model_path):
    """
    Load the trained model from weights file.
    
    Args:
        model_path: Path to the .h5 weights file
        
    Returns:
        Loaded Keras model
    """
    model = model_arc()
    model.load_weights(model_path)
    return model


def classify_recyclable(predicted_class):
    """
    Classify waste as Recyclable or Other based on predicted class.
    
    Args:
        predicted_class: String name of predicted class
        
    Returns:
        tuple: (bin_type, servo_angle)
            - bin_type: "Recyclable" or "Other"
            - servo_angle: 90 for Recyclable, 0 for Other
    """
    if predicted_class.lower() in RECYCLABLE_CATEGORIES:
        return "Recyclable", 90
    else:
        return "Other", 0

