from itertools import combinations
from json import loads
from random import choice
from time import sleep, time
from midiutil import MIDIFile
from mingus.containers import Note
from sys import exit

import mingus.core.chords as chords
import mingus.core.scales as scales
import pyinputplus as pyip
import os

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

def assign_index_input(index_value, input_list):
    return input_list[int(index_value) - 1]

def generate_melody(with_chords, repetitions=1):
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

        get_random_scale = False
        use_custom_scale = True
    else:
        get_random_scale = True
        use_custom_scale = False

    try:
        determined_scale = scales.determine(chosen_scale)[0]
    except:
        determined_scale = ""

    amount_of_notes = pyip.inputInt(prompt="How many notes do you want for this melody? ", min=1)
    if with_chords:
        chords_each_x = pyip.inputInt(prompt="How many notes you want between chords? ", min=1)
        chord_in_note = [x for x in range(0, amount_of_notes, chords_each_x)]

    for _ in range(repetitions):
        melody_name = generate_random_name()
        melody_path = f"Melodies/{melody_name}"
        os.mkdir(melody_path)

        track = 0
        channel  = 0
        time     = 0
        duration = 1
        tempo    = 120
        volume   = 100
        midi_melody = MIDIFile(1)
        midi_melody.addTempo(track, time, tempo)

        if get_random_scale:
            chosen_scale = choice(scales_content["scales"])
            possible_chords = chosen_scale["chords"]
            chosen_scale = chosen_scale["scale"]

        ly_string = r'''\version "2.20.0"
\header{title = "PLACEHOLDER_NAME" subtitle = "PLACEHOLDER_SUBTITLE" tagline = ##f}

\score {        
{
'''
        ly_string = ly_string.replace("PLACEHOLDER_NAME", melody_name)
        ly_string = ly_string.replace("PLACEHOLDER_SUBTITLE", f"{str(chosen_scale)} - {determined_scale}")


        print(f"\nGenerating melody with scale: {chosen_scale} - {determined_scale}\n")
        print(f"\t****{melody_name}****")

        all_parts = []
        for i in range(amount_of_notes):
            if with_chords:
                if i in chord_in_note:
                    if i != 0:
                        time += duration

                    chosen_chord = choice(possible_chords)
                    chosen_chord = chosen_chord[:3]

                    try:
                        determined_chord = chords.determine(list(chosen_chord))[0]
                    except:
                        determined_chord = ""
                    
                    ly_string += "\n< "
                    for note in chosen_chord:
                        ly_string += f"{note_to_ly(note)}' "
                        note_midi_value = int(Note(note)) + 12
                        midi_melody.addNote(track, channel, note_midi_value, time, duration, volume)
                    ly_string += ">\n\n"

                    all_parts.append(f"\n\t{chosen_chord} - {determined_chord}\n")
            
            chosen_note = choice(chosen_scale)

            ly_string += f"{note_to_ly(chosen_note)}4' "

            note_midi_value = int(Note(chosen_note)) + 12
            midi_melody.addNote(track, channel, note_midi_value, time + duration, duration, volume)
            time += duration

            all_parts.append(f"\t{chosen_note}")

        ly_string += """}
\layout { }
\midi { }
}"""

        with open(f"{melody_path}/{melody_name}.txt", "w") as f:
            for part in all_parts:
                f.write(f"{part}\n")
                print(part)

        with open(f"{melody_path}/{melody_name}_pond.ly", "w") as f:
            f.write(ly_string)

        with open(f"{melody_path}/{melody_name}.mid", "wb") as f:
            midi_melody.writeFile(f)
        
def note_practice():
    minutes_to_practice = pyip.inputInt(prompt="How many minutes do you want to practice? ", min=1)
    seconds_between = pyip.inputFloat(prompt="How many rest seconds you want between notes? ", min=1)

    start_time = time()
    while (True):
        print(f"\t{choice(complete_notes)}")

        sleep(seconds_between)
        if (time() - start_time) >= minutes_to_practice * 60:
            break

def chord_practice():
    minutes_to_practice = pyip.inputInt(prompt="How many minutes do you want to practice? ", min=1)
    seconds_between = pyip.inputFloat(prompt="How many rest seconds you want between chords? ", min=1)

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
    minutes_to_practice = pyip.inputInt(prompt="How many minutes do you want to practice? ", min=1)
    seconds_between = pyip.inputFloat(prompt="How many rest seconds you want between scales? ", min=1)

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
    
    menu_items = ["Note Practice", "Chord Practice", "Scale Practice", "Melody Generation", "Melody Generation with Chords"]
    menu_choice = pyip.inputMenu(menu_items, numbered=True, allowRegexes=[r"1|2|3|4|5|q"])

    try:
        menu_choice = assign_index_input(menu_choice, menu_items)
    except:
        pass

    if menu_choice is "q":
        exit()

    if menu_choice is menu_items[0]:
        note_practice()
    elif menu_choice is menu_items[1]:
        chord_practice()
    elif menu_choice is menu_items[2]:
        scale_practice()
    elif menu_choice is menu_items[3]:
        melodies_to_generate = pyip.inputInt(prompt="How many melodies do you want to generate? ", min=1)
        generate_melody(False, repetitions=melodies_to_generate)
    elif menu_choice is menu_items[4]:
        melodies_to_generate = pyip.inputInt(prompt="How many melodies do you want to generate? ", min=1)
        generate_melody(True, repetitions=melodies_to_generate)

    main()

main()
