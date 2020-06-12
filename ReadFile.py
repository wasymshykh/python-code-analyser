from os import path

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
