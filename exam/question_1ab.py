import sys
from math import log2
import re
from pandas import DataFrame
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

if(len(sys.argv) != 2):
    print("Usage: python3 question_1ab.py name_of_program")
    exit()

operatorsFileName = "operators"
programFileName = sys.argv[1]

operators = {}
operands = {}

with open(operatorsFileName) as f:
    for op in f:
        operators[op.replace('\n','')] = 0

isAllowed = True

with open(programFileName) as f:
    for line in f:
        line = line.strip("\n").strip(' ')

        if(line.startswith("/*")):
            isAllowed = False
       
        if((not line.startswith("//")) and isAllowed == True and (not line.startswith('#'))):
            # remove strings from line
            # re.findall(r"class\s(\w+)*", source_line)
            line = re.sub(r"'(\w+)'*", '', line)
            

            for key in operators.keys():
                operators[key] = operators[key] + line.count(key)
                line = line.replace(key,' ')
            for key in line.split():
                if key in operands:
                    operands[key] = operands[key] + 1
                else:
                    operands[key] = 1

        if(line.endswith("*/")):
            isAllowed = True

# ------------ almost similar to https://github.com/m0nk3ydluffy/Halstead-Metrics/

def source_details(_operators: dict, _operands):
    
    # removing _operators used < 1 and calculating total
    total_operators_used = 0
    temp = _operators.copy()
    for operator in _operators:
        if temp[operator] < 1 or operator in ")}]":
            del temp[operator]
        else:
            total_operators_used += _operators[operator]
    total_operators = len(temp)

    # calculating total _operands
    total_operands_used = 0
    for operand in _operands:
        total_operands_used += _operands[operand]
    total_operands = len(_operands)

    program_length = total_operands_used + total_operators_used
    program_volume = (total_operands_used + total_operators_used) * log2(total_operands + total_operators)
    program_difficulty = total_operators * total_operands_used / 2 / total_operands_used
    program_level = program_volume / program_difficulty / program_difficulty
    est_length = total_operators * log2(total_operators) + total_operands * log2(total_operands)
    effort = (program_difficulty * program_volume) / est_length
    time = effort * program_difficulty

    bugs = check_bugs(operators, operands)
    data = {"Program Length": program_length, "Program Volume": program_volume, "Program Level": program_level, 
    "Program estimated length": est_length, "Effort": effort, "Time": time, "Difficulty level": program_difficulty, "Remaining bugs": bugs }

    return data

def check_bugs(_operators, _operands):
    errors = 0

    # brackets not equal
    if _operators['{'] != _operators['}']:
        errors += 1
    if _operators['['] != _operators[']']:
        errors += 1
    if _operators['('] != _operators[')']:
        errors += 1

    # used variables/functions
    for o in _operands:
        if _operands[o] < 2:
            errors += 0.25

    return errors

source_data = source_details(operators, operands)

print(source_data)

window = tk.Tk()
window.title("VSA")
window.minsize(800, 800)

data = {'Name': [],
         'Value': []
        }

for s in source_data:
    data['Name'].append(s)
    data['Value'].append(source_data[s])

df = DataFrame(data,columns=['Name','Value'])

figure = plt.Figure(figsize=(12,7), dpi=80)
axi = figure.add_subplot(111)
bar = FigureCanvasTkAgg(figure, window)
bar.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df = df[['Name','Value']].groupby('Name').sum()
df.plot(kind='bar', legend=True, ax=axi)
axi.set_title('Program details')

window.mainloop()