# MIDI-Humanization-AI
AI to humanize MIDI velocities and note length

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

1. Put your midi file into the `mid` folder. (It can be easier renaming the file)
2. Open `midi_file_path.txt` in any text editor of your choice.
3. Edit the midi file path to `./mid/` and then the name of your midi file, in the example it is `midi.mid`

> [!IMPORTANT]
> The midi file needs to have either the extension `.mid` or `.midi`

### Start the humanization process

```bash
  py humanize.py
```

# Advanced

### If you're not happy with your results, you can proceed to some more fine-tuning adjustments.

1. Open up `humanize.py` in a text editor
2. Play around with these values at the very top of the code.

```python
PREDICTION_MULTIPLIER = 1.0
DURATION_LIMIT_UPPER = 1.75
DURATION_LIMIT_LOWER = 0.25
```

3. I wouldn't recommend you go above `2.0` or anything below `0.25`, because you could get some weird results.
