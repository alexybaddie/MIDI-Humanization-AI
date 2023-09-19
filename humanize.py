import pretty_midi
import numpy as np
import tensorflow as tf
import random
from data_processing import extract_features

PREDICTION_MULTIPLIER = 0.5
DURATION_LIMIT_UPPER = 0.75 # 1.25
MIN_DURATION_LIMIT = 0.5 / 8  # Duration of a 32nd note at 120 BPM
MAX_DURATION_LIMIT = 0.5 * 8  # Duration of two quarter notes at 120 BPM

def convert(midi_data):
    new_midi = pretty_midi.PrettyMIDI(resolution=midi_data.resolution, initial_tempo=midi_data.get_tempo_changes()[1][0])
    single_track = pretty_midi.Instrument(program=0)
    
    # Getting the original tempo
    original_tempo = midi_data.estimate_tempo()
    
    # Calculating the time-stretching factor
    time_stretching_factor = original_tempo / 120.0
    
    # List to hold the events with their time offsets
    events = []
    
    # List to hold tempo changes and their time offsets
    tempo_changes = [(0, 500000)]  # Default tempo (500000 microseconds per beat)
    
    # Extract events and tempo changes
    for track in midi_data.instruments:
        time_offset = 0
        for note in track.notes:
            start_time = note.start
            end_time = note.end
            velocity = note.velocity
            pitch = note.pitch
            events.append((start_time, pretty_midi.Note(start=start_time, end=end_time, pitch=pitch, velocity=velocity)))
    
    # Sort events by their start times
    events.sort(key=lambda x: x[0])
    
    for event in events:
        single_track.notes.append(event[1])
    
    # Create a new PrettyMIDI object with a tempo of 120 BPM
    new_midi_120 = pretty_midi.PrettyMIDI(initial_tempo=120.0)
    
    # Add the time-stretched notes to the new PrettyMIDI object
    new_single_track = pretty_midi.Instrument(program=0)
    new_single_track.notes = single_track.notes
    new_midi_120.instruments.append(new_single_track)
    
    return new_midi_120


def humanize_midi(midi_file_path, model, n=32):
    # Load the MIDI data
    original_midi = pretty_midi.PrettyMIDI(midi_file_path)
    
    # Convert the MIDI data to Type 0
    original_midi_data = convert(original_midi)
    midi_data = convert(original_midi)
    
    # Check if there are any instruments in the MIDI data
    if not midi_data.instruments:
        return []
    
    # Extract and humanize the notes
    original_notes = original_midi_data.instruments[0].notes
    notes = midi_data.instruments[0].notes

    min_length = min(len(notes), len(original_notes))  # Find the minimum length
    min_velocity = min(len(notes), len(original_notes))  # Find the minimum velocity

    for i in range(min_length - n - 1):  # Use the minimum length to set the loop range
        input_sequence = np.array([[(note.pitch, note.velocity, note.end - note.start) for note in notes[i:i+n]]])
        predicted_values = model.predict(input_sequence)
        next_note = notes[i+n]

        # Calculate the original duration and the predicted duration
        original_end_time = original_notes[i+n].end
        original_duration = original_end_time - next_note.start
     #   predicted_duration = predicted_values[0][0] * PREDICTION_MULTIPLIER

        # Adjust the note's end time based on the predicted duration, but limit the adjustment 
        # to prevent the duration from becoming too short or too long compared to the original duration
        
     
        if original_duration > 0.5:  # If the original duration is longer than a quarter note at 120 BPM
            predicted_duration = max(min(predicted_values[0][0], MAX_DURATION_LIMIT), original_duration * 0.75)  # Set the predicted duration to be 75% of the original duration
        else:
            predicted_duration = max(min(predicted_values[0][0] * PREDICTION_MULTIPLIER, original_duration * 1.25), original_duration * 0.5)
            
        # Adding a small random variation to the predicted duration (between -5% and +5% of the predicted duration)
        random_variation = random.uniform(-0.25, 0)
        predicted_duration += predicted_duration * random_variation
        
     #   new_duration = max(min(predicted_duration, original_duration * DURATION_LIMIT_UPPER), MIN_DURATION_LIMIT)
        
        new_duration = max(min(predicted_duration, MAX_DURATION_LIMIT), MIN_DURATION_LIMIT)
        next_note.end = next_note.start + new_duration
        
     #   new_duration = max(min(predicted_duration, MAX_DURATION_LIMIT), MIN_DURATION_LIMIT)
        
     #   next_note.end = next_note.start + new_duration
        
     #   next_note.end = int(predicted_values[0][1])

        next_note.velocity = int(predicted_values[0][1])

    return midi_data


if __name__ == "__main__":
    model = tf.keras.models.load_model("humanize_model.h5")
    with open("midi_file_path.txt", "r") as f:
        midi_file_name = f.readline().strip() # Read the file name from the text document
    midi_file_path = "./mid/" + midi_file_name # Construct the full path by adding the folder path
    humanized_data = humanize_midi(midi_file_path, model)
    humanized_data.write("humanized_output.mid")
