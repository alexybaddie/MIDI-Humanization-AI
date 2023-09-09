import numpy as np
import tensorflow as tf
from data_processing import extract_features_from_dataset, extract_midi_paths_from_metadata
import time

def build_lstm_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(64, input_shape=(4, 1), return_sequences=True),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Get MIDI paths and select a subset
midi_paths = extract_midi_paths_from_metadata()
midi_files_subset = midi_paths[:100]  # Taking only the first 100 files for the test

# Extract features from the subset
all_features = extract_features_from_dataset(midi_files_subset)
durations = all_features[:, 0]  # Extracting only the duration for the target

model = build_lstm_model()

# Start timing the training process
start_time = time.time()
model.fit(all_features, durations, epochs=3, batch_size=32, verbose=1)
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Time taken for 3 epochs on 100 samples: {elapsed_time} seconds")
