import mingus.core.scales as scales
from json import loads

scales_content = []
with open("scales.json", "r") as f:
    scales_content = loads(f.read())

all_scales = []
for scale in scales_content['scales']:
    determined_scale = scales.determine(scale['scale'])
    if determined_scale:
        full_scale = f"{scale['scale']} - {determined_scale}"
        all_scales.append(full_scale)
    else:
        continue

with open("named_scales.txt", "w") as f:
    for full_scale in all_scales:
        f.write(f"{str(full_scale)}\n\n")