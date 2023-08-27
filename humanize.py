import mido
import numpy as np
import tensorflow as tf
from data_processing import extract_features

def convert(midi_data):
    new_midi = mido.MidiFile(ticks_per_beat=midi_data.ticks_per_beat)
    single_track = mido.MidiTrack()
    new_midi.tracks.append(single_track)
    
    # List to hold the events with their time offsets
    events = []
    
    # List to hold tempo changes and their time offsets
    tempo_changes = [(0, 500000)]  # Default tempo (500000 microseconds per beat)
    
    # Extract events and tempo changes
    for track in midi_data.tracks:
        time_offset = 0
        for msg in track:
            time_offset += msg.time
            if msg.is_meta and msg.type == "set_tempo":
                tempo_changes.append((time_offset, msg.tempo))
            if not msg.is_meta:
                events.append((time_offset, msg.copy(time=0)))
    
    # Sort events by their time offsets
    events.sort(key=lambda x: x[0])
    
    # Process events by adjusting the time based on tempo changes
    last_time_offset = 0
    current_tempo_idx = 0
    for event in events:
        while current_tempo_idx + 1 < len(tempo_changes) and event[0] >= tempo_changes[current_tempo_idx + 1][0]:
            current_tempo_idx += 1
        current_tempo = tempo_changes[current_tempo_idx][1]
        
        # Adjust the time of the event based on the current tempo
        ticks_per_beat = midi_data.ticks_per_beat
        delta_time_in_seconds = mido.tick2second(event[0] - last_time_offset, ticks_per_beat, current_tempo)
        delta_ticks = mido.second2tick(delta_time_in_seconds, ticks_per_beat, 500000)  # Convert back using default tempo
        msg = event[1]
        msg.time = int(round(delta_ticks))
        single_track.append(msg)
        last_time_offset = event[0]
    
    return new_midi

def humanize_midi(midi_file_path, model, n=5, max_duration=1.0, velocity_threshold=0.1, duration_threshold=0.1):
    # Load the MIDI data
    midi_data = mido.MidiFile(midi_file_path)
    # Convert the MIDI data to Type 0
    midi_data = convert(midi_data)

    
    # Check if there are any instruments in the MIDI data
    if not midi_data.tracks:
        return []
    
    # Extract and humanize the notes
    notes = []
    active_notes = {}
    current_time = 0
    for msg in midi_data.tracks[0]:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            active_notes[msg.note] = (msg.note, msg.velocity, current_time)
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            start_note = active_notes.pop(msg.note, None)
            if start_note:
                duration = current_time - start_note[2]
                notes.append((*start_note, duration))

    for i in range(len(notes) - n):
        input_sequence = np.array([[(note[0], note[1], note[3]) for note in notes[i:i+n]]])
        predicted_values = model.predict(input_sequence)
        
        # Normalize predicted values
        predicted_duration = min(max_duration, max(0, predicted_values[0][0]))
        predicted_velocity = min(127, max(0, int(predicted_values[0][1])))
        
        # Apply changes only if they exceed the threshold
        if abs(predicted_velocity - notes[i+n][1]) > velocity_threshold:
            notes[i+n] = (notes[i+n][0], predicted_velocity, notes[i+n][2], notes[i+n][3])
        if abs(predicted_duration - notes[i+n][3]) > duration_threshold:
            notes[i+n] = (notes[i+n][0], notes[i+n][1], notes[i+n][2], predicted_duration)
            
        # Replace the original note with the modified note in the MIDI data
        for idx, msg in enumerate(midi_data.tracks[0]):
            if msg.type == 'note_on' and msg.note == notes[i+n][0] and msg.time == notes[i+n][2]:
                midi_data.tracks[0][idx] = mido.Message('note_on', note=notes[i+n][0], velocity=notes[i+n][1], time=notes[i+n][2])
                break

    return midi_data

if __name__ == "__main__":
    model = tf.keras.models.load_model("humanize_model.h5")
    midi_file_path = "./mid/midi.mid"  # Replace with your actual input MIDI file path
    humanized_data = humanize_midi(midi_file_path, model)
    humanized_data.save("humanized_output.mid")
