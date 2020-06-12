# Github project link: https://github.com/wasymshykh/python-code-analyser

from os import path
from ReadFile import ReadFile
from Calculate import Calculate

if __name__ == '__main__':
    
    # File name and path
    file_name = 'test.java'
    file_path = path.join(path.dirname(path.abspath(__file__)), file_name)
    
    # Opening file
    r = ReadFile(file_path)

    # Source code analysing
    c = Calculate(r.get_lines_list_clean())
    c.print_data()

