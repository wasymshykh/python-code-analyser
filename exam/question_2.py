
class ReadFile:
    def __init__(self, file_path):
        if type(file_path) != str:
            print('file path must be in string!')
        
        source = open(file_path, 'r')
        self.file = source

    def get_lines_list(self):
        return self.file.readlines()
    
    def read_string(self):
        lines_list = self.get_lines_list()
        source_string = ""
        for line in lines_list:
            source_string += line
        return source_string


    def clear(self):
        self.file.close()