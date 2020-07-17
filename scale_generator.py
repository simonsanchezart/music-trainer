from itertools import combinations

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
scales_file = open("scales.json", "w")
all_scales = []
for i in range(len(notes) + 1):
    combinations_object = combinations(notes, i)
    combinations_list = list(combinations_object)
    all_scales += combinations_list

for i in range(len(notes) + 1):
    del all_scales[0]

# all_scales = all_scales[:]

scales_file.write("{\n")
scales_file.write('''\t"scales":[\n''')
for i in range(len(all_scales)):
    scale = list(all_scales[i])

    all_chords = []
    for x in range(len(scale) + 1):
        combinations_object = combinations(scale, x)
        combinations_list = list(combinations_object)
        all_chords += combinations_list

    for y in range(len(scale) + 1):
        del all_chords[0]

    scales_file.write("\t\t{")
    scales_file.write(f'''"scale": {scale}, "chords": {list(all_chords)}''') # 

    if i != len(all_scales) - 1:
        scales_file.write("},\n")
    else:
        scales_file.write("}\n")

scales_file.write("\t]")
scales_file.write("\n}")

scales_file.close()

with open(r"scales.json", "r") as file:
    file_data = file.read()

file_data = file_data.replace("'", '"')
file_data = file_data.replace("(", '[')
file_data = file_data.replace(")", ']')

with open(r"scales.json", "w") as file:
    file.write(file_data)
