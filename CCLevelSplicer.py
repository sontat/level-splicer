# Chip's Challenge Level Splicer by Tyler Sontag
# input:  Chip's Challenge level set filename,
#         then one or more level numbers, separated by tabs, on each line

import sys
import struct

if (len(sys.argv) != 3):
    print "Usage: {0} input output".format(sys.argv[0])
    sys.exit()

in_name = sys.argv[1] 
out_name = sys.argv[2]

try:
    input_file = open(in_name,'rb')
except IOError as e:
    print "I/O error: {0} {1}".format(e.strerror, in_name)
    sys.exit()

lines = input_file.read().split('\n')
level_buffer = []
level_sets = {}
n = 0

for x in lines:
    if (x in ('\n')):
        continue
    line_data = x.split('\t')
    level_set = line_data[0]
    if (level_set not in level_sets):
        try:
            cur_file = open(level_set,'rb')
            level_sets[level_set] = cur_file
        except IOError as e:
            print "I/O error: {0} {1}".format(e.strerror, level_set)
            sys.exit()
    else:
        cur_file = level_sets[level_set]
    cur_file.seek(4, 0)
    num_levels = struct.unpack("<h", cur_file.read(2))[0]
    for y in line_data[1:]:
        n += 1
        while (True):
            lb = cur_file.read(2)
            ln = cur_file.read(2)
            num_bytes = struct.unpack("<h", lb)[0]
            level_num = struct.unpack("<h", ln)[0]
            if (level_num == int(y)):
                level_bytes = cur_file.read(num_bytes-2)
                level_buffer += [(lb + struct.pack("<h", n) + level_bytes)]
                break
            cur_file.seek(num_bytes-2,1)
            if (level_num == num_levels):
                print "Error: reached end of {0} without finding level {1}".format(level_set, str(y))
                sys.exit()

for x in level_sets:
    level_sets[x].close()
level_sets.clear()

output_buffer = b'\xac\xaa\x02\x00' + struct.pack("<h", n)
for x in level_buffer:
    output_buffer += x
output_f = open(out_name,'wb')
output_f.write(output_buffer)
output_f.close()
print "Constructed {0} with {1} levels".format(out_name, str(n))