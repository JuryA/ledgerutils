#!/usr/bin/env python

import sys
import glob

if len(sys.argv) < 4:
    print "Need arguments! %s <file> <old> <new>" % sys.argv[0]
else:
    old_txt = sys.argv[2]
    new_txt = sys.argv[3]

    old_txt_padded = None
    new_txt_padded = None

    if len(new_txt) == len(old_txt):
        old_txt_padded = old_txt
        new_txt_padded = new_txt
    elif len(new_txt) > len(old_txt):
        old_txt_padded = old_txt.ljust(len(old_txt)+len(new_txt)-len(old_txt))
        new_txt_padded = new_txt
    elif len(old_txt) > len(new_txt):
        old_txt_padded = old_txt
        new_txt_padded = new_txt.ljust(len(new_txt)+len(old_txt)-len(new_txt))

    for FILENAME in glob.glob(sys.argv[1]):
        input_file = open(FILENAME, 'r').readlines()
        write_file = open(FILENAME, 'w')

        for line in input_file:
            if line.endswith(old_txt+"\n"):
                new_line = line.replace(old_txt, new_txt)
            else:
                new_line = line.replace(old_txt_padded, new_txt_padded)
            write_file.write(new_line)
