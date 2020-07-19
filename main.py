from itertools import repeat, combinations
from json import loads
from random import choice
from time import sleep, time

import mingus.core.chords as chords
import mingus.core.scales as scales
import pyinputplus as pyip
import os
from midiutil import MIDIFile
from mingus.containers import Note

complete_notes = ["C", "B#", "C#", "Db", "D", "D#", "Eb", "E", "Fb", "F", "E#","F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B", "Cb"]

scales_content = []
with open("scales.json", "r") as f:
    scales_content = loads(f.read())

random_words = []
with open("random_name_base.json", "r") as f:
    random_words = loads(f.read())

def generate_random_name():
    noun = choice(random_words["nouns"])
    adjective = choice(random_words["adjs"])
    name = f"The {adjective} {noun}"
    if os.path.isdir(f"Melodies/{name}"):
        generate_random_name()
    else:
        return name

def note_to_ly(note_name):
    note_name = note_name.lower()
    note_name = note_name.replace("#", "is")
    return note_name

def generate_melodies_with_chords(with_chords):
    melody_name = generate_random_name()
    melody_path = f"Melodies/{melody_name}"
    os.mkdir(melody_path)

    use_custom_scale = pyip.inputYesNo(prompt="Do you want to use a custom scale? (y/n) ")
    possible_chords = []
    if use_custom_scale == "yes":
        scale_input = input("""Insert the notes from the scale separated by a space, do not use flats, only sharps.
        \t\tExample: C D E F# A\n""")
        chosen_scale = scale_input.upper().split()

        for x in range(len(chosen_scale) + 1):
            combinations_object = combinations(chosen_scale, x)
            combinations_list = list(combinations_object)
            possible_chords += combinations_list

        for _ in range(len(chosen_scale) + 1):
            del possible_chords[0]

        use_custom_scale = True
    else:
        chosen_scale = choice(scales_content["scales"])
        possible_chords = chosen_scale["chords"]
        chosen_scale = chosen_scale["scale"]
        use_custom_scale = False

    try:
        determined_scale = scales.determine(chosen_scale)[0]
    except:
        determined_scale = "Nameless"

    amount_of_notes = pyip.inputInt(prompt="How many notes do you want for this melody? ")
    if with_chords:
        chords_each_x = pyip.inputInt(prompt="How many notes you want between chords? ")
        chord_in_note = [x for x in range(0, amount_of_notes, chords_each_x)]

    track = 0
    channel  = 0
    time     = 0
    duration = 1
    tempo    = 120
    volume   = 100

    midi_melody = MIDIFile(1)
    midi_melody.addTempo(track, time, tempo)

    ly_string = r'''\version "2.20.0"
\header{title = "PLACEHOLDER_NAME" subtitle = "PLACEHOLDER_SUBTITLE" tagline = ##f}
    
\relative c'
{
'''
    ly_string = ly_string.replace("PLACEHOLDER_NAME", melody_name)
    ly_string = ly_string.replace("PLACEHOLDER_SUBTITLE", f"{str(chosen_scale)} - {determined_scale}")

    all_parts = []

    print(f"\nGenerating melody with scale: {chosen_scale} - {determined_scale}\n")
    print(f"\t****{melody_name}****")
    for i in range(amount_of_notes):
        if with_chords:
            if i in chord_in_note:
                if i != 0:
                    time += duration
                chosen_chord = choice(possible_chords)
                try:
                    determined_chord = chords.determine(list(chosen_chord))[0]
                except:
                    determined_chord = "Nameless"
                chosen_chord = chosen_chord[:3]
                ly_string += "\n< "
                for note in chosen_chord:
                    ly_string += f"{note_to_ly(note)} "
                    note_midi_value = int(Note(note)) + 12
                    midi_melody.addNote(track, channel, note_midi_value, time, duration, volume)
                ly_string += ">\n\n"
                all_parts.append(f"\n\t{chosen_chord} - {determined_chord}\n")
        chosen_note = choice(chosen_scale)
        ly_string += f"{note_to_ly(chosen_note)}4 "
        note_midi_value = int(Note(chosen_note)) + 12
        midi_melody.addNote(track, channel, note_midi_value, time + duration, duration, volume)
        time += duration
        all_parts.append(f"\t{chosen_note}")

    with open(f"{melody_path}/{melody_name}.txt", "w") as f:
        for part in all_parts:
            f.write(f"{part}\n")
            print(part)

    ly_string += "\n}"
    with open(f"{melody_path}/{melody_name}.ly", "w") as f:
        f.write(ly_string)

    with open(f"{melody_path}/{melody_name}.mid", "wb") as f:
        midi_melody.writeFile(f)

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

def main():
    if not os.path.isdir("Melodies"):
        os.mkdir("Melodies")
    generate_melodies_with_chords(False)

main()
