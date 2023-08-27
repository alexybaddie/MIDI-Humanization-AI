import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from data_processing import extract_features, extract_midi_paths_from_metadata

def build_lstm_model(input_shape=(5, 3)):
    """Creates and returns the LSTM-based humanization model."""
    model = Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        tf.keras.layers.LSTM(128, return_sequences=True),
        tf.keras.layers.LSTM(64),
        Dense(32, activation='relu'),
        Dense(2)  # Output two values: duration and velocity
    ])
    
    model.compile(optimizer='adam', loss='mse')
    return model

if __name__ == "__main__":
    BASE_DIR = "./maestro-v3.0.0/"  # Relative directory where the MAESTRO dataset is stored
    
    midi_paths = extract_midi_paths_from_metadata()
    midi_files = [BASE_DIR + path for path in midi_paths]  # Convert relative paths to full local paths

    # Extract sequences and corresponding next note's attributes from the dataset
    data = [extract_features(midi_file, n=5) for midi_file in midi_files]
    features, labels = zip(*[item for sublist in data for item in sublist])

    # Convert to numpy arrays
    features = np.array(features)
    labels = np.array(labels)

    # Train the model
    model = build_lstm_model()
    model.fit(features, labels, epochs=20, batch_size=32, verbose=1)
    
    print("Saving trained model...")
    model.save("humanize_model.h5")  # Save the trained model
