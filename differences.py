import pretty_midi

original_midi = pretty_midi.PrettyMIDI("./mid/midi.mid")
humanized_midi = pretty_midi.PrettyMIDI("./humanized_output.mid")

original_notes = original_midi.instruments[0].notes
humanized_notes = humanized_midi.instruments[0].notes

differences = {
    "number_of_notes": (len(original_notes), len(humanized_notes)),
    "different_start_times": sum(1 for o, h in zip(original_notes, humanized_notes) if o.start != h.start),
    "different_end_times": sum(1 for o, h in zip(original_notes, humanized_notes) if o.end != h.end),
    "different_pitches": sum(1 for o, h in zip(original_notes, humanized_notes) if o.pitch != h.pitch)
}

print(differences)
