import pretty_midi
import numpy as np
import tensorflow as tf
from data_processing import extract_features

PREDICTION_MULTIPLIER = 1.0
DURATION_LIMIT_UPPER = 1.75
DURATION_LIMIT_LOWER = 0.25

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
    
   # new_midi.instruments.append(single_track)
    
  #  return new_midi


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

    for i in range(min_length - n - 1):  # Use the minimum length to set the loop range
        input_sequence = np.array([[(note.pitch, note.velocity, note.end - note.start) for note in notes[i:i+n]]])
        predicted_values = model.predict(input_sequence)
        next_note = notes[i+n]

        # Calculate the original duration and the predicted duration
        original_end_time = original_notes[i+n].end
        original_duration = original_end_time - next_note.start
        predicted_duration = predicted_values[0][0] * PREDICTION_MULTIPLIER

        # Adjust the note's end time based on the predicted duration, but limit the adjustment 
        # to prevent the duration from becoming too short or too long compared to the original duration
        new_duration = max(min(predicted_duration, original_duration * DURATION_LIMIT_UPPER), original_duration * DURATION_LIMIT_LOWER)
        next_note.end = next_note.start + new_duration

        next_note.velocity = int(predicted_values[0][1])

    # ... (the ending part of the function remains the same)
    return midi_data


if __name__ == "__main__":
    model = tf.keras.models.load_model("humanize_model.h5")
    with open("midi_file_path.txt", "r") as f:
        midi_file_path = f.readline().strip() # Replace with your actual input MIDI file path
    humanized_data = humanize_midi(midi_file_path, model)
    humanized_data.write("humanized_output.mid")
