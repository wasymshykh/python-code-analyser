'''
    ---------------
    # y u opened ⚰
    ---------------
    @purpose: just testing code
'''

from os import path
import re


class ReadFile:
    def __init__(self, file_path):
        if type(file_path) != str:
            print('file path must be in string!')
        
        source = open(file_path, 'r')
        extension = path.splitext(source.name)[1][1:]
        
        if extension != 'java':
            print('only java files are allowed!')
        
        if source.mode != 'r':
            print('file read mode error!')

        self.file = source

    def get_lines_list(self):
        return self.file.readlines()

    def get_lines_list_clean(self):
        cleaned = []
        for line in self.get_lines_list():
            cleaned.append(line.replace("\n", "").strip())
        return cleaned
    
    def get_content_string(self):
        string = ""
        for line in self.get_lines_list():
            string += line
        return string

    def clear(self):
        self.file.close()


class Calculate:
    def __init__(self, source: list):
        if type(source) is not list:
            print("Source code must be list!")
        
        if len(source) < 1:
            print("Source code cannot be empty!")
            
        self.source = source
        self.clean_source = self.remove_comments()

    def loc(self):
        loc = 0
        sloc = 0
        cloc = 0

        iscomment = False
        for source_line in self.source:
            loc += 1
            if source_line.strip() != "":
                sloc += 1
            
            # Mutiline comments checker
            if source_line.startswith('/*') or iscomment:
                iscomment = True
                cloc += 1
                if iscomment is True:
                    if source_line.find("*/") != -1:
                        iscomment = False
            
            # Singleline comment checker
            if not iscomment and source_line.find("//") != -1:
                cloc += 1
        return { 'loc': loc, 'sloc': sloc, 'cloc': cloc, 'ncloc': loc - cloc }

    def remove_comments(self):
        without_comments = []

        iscomment = False
        for source_line in self.source:
            # Mutiline comments checker
            if source_line.startswith('/*') or iscomment:
                iscomment = True
                if iscomment is True:
                    if source_line.find("*/") != -1:
                        iscomment = False
                    source_line = source_line[:0]

            # Singleline comment removing and list populating
            single_c = source_line.find('//')
            if not iscomment and single_c != -1:
                clean = source_line[:single_c].strip()
                if len(clean):
                    without_comments.append(clean)
            elif not iscomment and len(source_line.strip()):
                without_comments.append(source_line)
        
        return without_comments
        


    def classes(self):
        classes, public_classes, private_classes, abstract_classes, final_classes, static_classes = [],[],[],[],[],[]

        for source_line in self.clean_source:
            # all classes
            temp = re.findall(r"class\s(\w+)*", source_line)
            if len(temp) > 0:
                classes += temp

                # public classes
                temp = re.findall(r"public\sclass\s(\w+)*", source_line)
                if len(temp) > 0:
                    public_classes += temp
                    
                # private classes
                temp = re.findall(r"private\sclass\s(\w+)*", source_line)
                if len(temp) > 0:
                    private_classes += temp

                # abstract classes
                temp = re.findall(r"abstract\sclass\s(\w+)*", source_line)
                if len(temp) > 0:
                    abstract_classes += temp

                # final classes
                temp = re.findall(r"final\sclass\s(\w+)*", source_line)
                if len(temp) > 0:
                    final_classes += temp

                # static classes
                temp = re.findall(r"static\sclass\s(\w+)*", source_line)
                if len(temp) > 0:
                    static_classes += temp

        return { 'all_classes': classes, 'public_classes': public_classes, 'private_classes': private_classes,
        'abstract_classes': abstract_classes, 'final_classes': final_classes, 'static_classes': static_classes }


    def variables(self):
       return




if __name__ == '__main__':
    
    file_name = 'test.java'
    file_path = path.join(path.dirname(path.abspath(__file__)), file_name)
    
    r = ReadFile(file_path)

    c = Calculate(r.get_lines_list_clean())
    
    