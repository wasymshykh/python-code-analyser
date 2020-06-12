from os import path

if __name__ == '__main__':
    
    file_name = 'test.java'
    file_path = path.join(path.dirname(path.abspath(__file__)), file_name)
    source = open(file_path, 'r')
    
    extension = path.splitext(source.name)[1][1:]

    if extension == 'java' and source.mode == 'r':
        
        source_lines = source.readlines()
        source.close()

        loc = 0
        sloc = 0
        cloc = 0
        iscomment = False

        for source_line in source_lines:
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


        print("Line of code", loc)
        print("Source line of code", sloc)
        print("Commented line of code", cloc)
        print("None Commented line of code", loc - cloc)