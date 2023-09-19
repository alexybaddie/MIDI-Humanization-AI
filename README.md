# MIDI Humanization AI
AI with note length and velocity prediction

## Setup the Environment

Clone the project

```bash
  git clone https://github.com/alexybaddie/MIDI-Humanization-AI.git
```

Go to the project directory

```bash
  cd MIDI-Humanization-AI
```

Install dependencies

```bash
  pip install -r requirements.txt
```

### Edit the MIDI file path

1. Place your MIDI file in the mid folder (you may find it easier to rename the file).
2. Open `midi_file_path.txt` in any text editor of your choice.
3. Update the path with the name of your MIDI file (e.g., `midi.mid`).

> [!IMPORTANT]
> Ensure your file has a `.mid` or `.midi` extension.

> [!WARNING]
> If the MIDI file contains longer notes, the program might retain them. You may need to 
> adjust the note lengths manually afterwards to achieve the desired effect. This precaution 
> helps preserve the melody.

### Start the humanization process

```bash
  py humanize.py
```

# Advanced

### If you're not happy with your results, you can proceed to some more fine-tuning adjustments.

1. Open up `humanize.py` in a text editor
2. Play around with these values at the very top of the code.

```python
# Fine-tuning parameters
PREDICTION_MULTIPLIER = 0.5
DURATION_LIMIT = 1.25
```