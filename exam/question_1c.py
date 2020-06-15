import sys
from os import path
import re

if(len(sys.argv) != 2):
    print("Usage: python3 question_1c.py name_of_program")
    exit()

programfile = sys.argv[1]


class Calculate:
    def __init__(self, source_code):
        self.source_lines = source_code

    def loc(self):
        length = 0
        loc = 0
        cloc = 0

        iscomment = False
        for source_line in self.source_lines:
            length += 1
            if source_line.strip() != "":
                loc += 1
            
            # Mutiline comments checker
            if source_line.startswith('/*') or iscomment:
                iscomment = True
                cloc += 1
                if iscomment is True:
                    if source_line.find("*/") != -1:
                        iscomment = False
            
            # Singleline comment checker
            if not iscomment and source_line.find("#") != -1:
                cloc += 1

        # code lines minus comment lines (plus one) divided by total number of lines
        density = float((loc - cloc) + 1) / length

        return { 'length': length, 'loc': loc, 'nloc': loc - cloc, 'code_density': density}




class ReadFile:
    def __init__(self, file_path):
        if type(file_path) != str:
            print('file path must be in string!')
        
        source = open(file_path, 'r')
        self.file = source

    def get_lines_list(self):
        return self.file.readlines()

    def clear(self):
        self.file.close()


file_path = path.join(path.dirname(path.abspath(__file__)), programfile)
rf = ReadFile(file_path)
calc = Calculate(rf.get_lines_list())
rf.clear()
print(calc.loc())

