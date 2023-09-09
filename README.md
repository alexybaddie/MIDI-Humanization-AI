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

Put your midi file into the "mid" folder. (It can be easier renaming the file)
Open "midi_file_path.txt" in any text editor of your choice.
Edit the midi file path to "./mid/" and then the name of your midi file, in the example it is "midi.mid"

> [!IMPORTANT]
> The midi file needs to have either the extension ".mid" or ".midi"

### Start the humanization process

```bash
  py humanize.py
```

# Advanced

If you're not happy with your results
