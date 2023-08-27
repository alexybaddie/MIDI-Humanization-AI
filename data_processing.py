import csv
import mido
import numpy as np

def extract_midi_paths_from_metadata():
    csv_path = "./maestro-v3.0.0/maestro-v3.0.0.csv"
    midi_paths = []
    
    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            midi_paths.append(row['midi_filename'])

    return midi_paths


def extract_features(midi_file_path, n=5):
    """Extracts sequences of notes and their corresponding next note's attributes from a given midi file."""
    
    midi_data = mido.MidiFile(midi_file_path)
    
    if not midi_data.tracks:
        return []

    notes = []
    active_notes = {}
    current_time = 0
    
    for track in midi_data.tracks:
        for msg in track:
            
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                active_notes[msg.note] = (msg.note, msg.velocity, current_time)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                start_note = active_notes.pop(msg.note, None)
                if start_note:
                    duration = current_time - start_note[2]
                    notes.append((*start_note, duration))
                    
    features = []
    labels = []

    # Normalize velocities and durations
    velocities = [note[1] for note in notes]
    durations = [note[3] for note in notes]
    max_velocity = max(velocities)
    max_duration = max(durations)
    
    for i in range(len(notes) - n):
        input_sequence = [(note[0], note[1]/max_velocity, note[3]/max_duration) for note in notes[i:i+n]]
        next_note = notes[i+n]
        output_sequence = (next_note[3]/max_duration, next_note[1]/max_velocity)
        
        features.append(input_sequence)
        labels.append(output_sequence)

    return list(zip(features, labels))
