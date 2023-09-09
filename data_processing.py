# data_processing.py

import csv
import pretty_midi
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
    midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    if not midi_data.instruments:
        return []

    notes = midi_data.instruments[0].notes
    features = []
    labels = []

    for i in range(len(notes) - n):
    #    input_sequence = [(note.pitch, note.velocity, note.end - note.start) for note in notes[i:i+n]]
        input_sequence = [(note.pitch, note.velocity, note.end - note.start, note.end - note.start) for note in notes[i:i+n]]
        next_note = notes[i+n]
        output_sequence = (next_note.end - next_note.start, next_note.velocity)
        
        features.append(input_sequence)
        labels.append(output_sequence)

    return list(zip(features, labels))