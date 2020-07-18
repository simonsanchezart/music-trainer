from json import loads
from random import choice, uniform
from itertools import repeat
from time import time, sleep
import mingus.extra.lilypond as LilyPond
import mingus.core.chords as chords
import mingus.core.scales as scales
from mingus.containers import Bar, Track, Note
from mingus.midi.midi_file_out import write_Track
from midiutil import MIDIFile
import pyinputplus as pyip

complete_notes = ["C", "B#", "C#", "Db", "D", "D#", "Eb", "E", "Fb", "F", "E#","F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B", "Cb"]

scales_content = []
with open("scales.json", "r") as f:
    scales_content = loads(f.read())

def generate_melodies():
    amount_of_notes = pyip.inputInt(prompt="How many notes do you want for this melody? ")
    scale = choice(scales_content["scales"])["scale"]

    print(f"Generating melody with scale: {scale} - {scales.determine(scale)}\n")
    for _ in repeat(None, amount_of_notes):
        print(f"\t{choice(scale)}")

def generate_melodies_with_chords():
    amount_of_notes = pyip.inputInt(prompt="How many notes do you want for this melody? ")
    chords_each_x = pyip.inputInt(prompt="How many notes you want between chords? ")
    chord_in_note = [x for x in range(0, amount_of_notes, chords_each_x)]
    chosen_scale = choice(scales_content["scales"])
    track = 0
    channel  = 0
    time     = 0
    duration = 1
    tempo    = 120
    volume   = 100

    midi_melody = MIDIFile(1)
    midi_melody.addTempo(track, time, tempo)

    print(f"Generating melody with scale: {chosen_scale['scale']}\n")
    for i in range(amount_of_notes):
        if i in chord_in_note:
            chosen_chord = choice(chosen_scale['chords'])
            chosen_chord = chosen_chord[:4]
            for note in chosen_chord:
                note_midi_value = int(Note(note)) + 12
                midi_melody.addNote(track, channel, note_midi_value, time, duration, volume)
            print(f"\n\t{chosen_chord}\n")
        chosen_note = choice(chosen_scale['scale'])
        note_midi_value = int(Note(chosen_note)) + 12
        midi_melody.addNote(track, channel, note_midi_value, time + duration, duration, volume)
        time += duration
        print(f"\t{chosen_note}")

    return midi_melody
        
def note_practice():
    minutes_to_practice = pyip.inputInt(prompt="How many minutes do you want to practice? ")
    seconds_between = pyip.inputFloat(prompt="How many rest seconds you want between notes? ")
    start_time = time()
    while (True):
        print(f"\t{choice(complete_notes)}")
        sleep(seconds_between)
        if (time() - start_time) >= minutes_to_practice * 60:
            break

def chord_practice():
    minutes_to_practice = pyip.inputInt(prompt="How many minutes do you want to practice? ")
    seconds_between = pyip.inputFloat(prompt="How many rest seconds you want between chords? ")
    start_time = time()
    while (True):
        chosen_chord = choice(choice(scales_content['scales'])['chords'])
        determined_chord = chords.determine(chosen_chord, True)
        
        if determined_chord:
            print(f"\t{chosen_chord} - {determined_chord[0]}")
        else:
            print(f"\t{chosen_chord}")

        sleep(seconds_between)
        if (time() - start_time) >= minutes_to_practice * 60:
            break

def scale_practice():
    minutes_to_practice = pyip.inputInt(prompt="How many minutes do you want to practice? ")
    seconds_between = pyip.inputFloat(prompt="How many rest seconds you want between scales? ")
    start_time = time()
    while (True):
        chosen_scale = choice(scales_content['scales'])['scale']
        determined_scale = scales.determine(chosen_scale)

        if determined_scale:
            print(f"\t{chosen_scale} - {determined_scale[0]}")
        else:
            print(f"\t{chosen_scale}")

        sleep(seconds_between)
        if (time() - start_time) >= minutes_to_practice * 60:
            break

def generate_melody():
    my_midi = generate_melodies_with_chords()
    with open(f"my_midi.mid", "wb") as output_file:
        my_midi.writeFile(output_file)

    # track = LilyPond.from_Track(t)
    # print(t)
    # write_Track("test.mid", t)
    # LilyPond.to_pdf(track, "my_first_bar")

def main():
    generate_melody()

main()