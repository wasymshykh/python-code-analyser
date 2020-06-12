import re

class Calculate:
    def __init__(self, source: list):
        if type(source) is not list:
            print("Source code must be list!")
        
        if len(source) < 1:
            print("Source code cannot be empty!")
            
        self.source = source
        self.clean_source = self.normalize_code()

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

    def normalize_code(self):
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

        return { 'all': classes, 'public': public_classes, 'private': private_classes,
        'abstract': abstract_classes, 'final': final_classes, 'static': static_classes }


    def variables(self):
        # returned data: format -> {'[type]': ['[name]']}
        data = {}

        for source_line in self.clean_source:
            
            # instance variables: format -> [str] [name] = new [str];
            temp = re.findall(r"(\w+)\s+(\w+)\s*=\s*new\s+(\w+)\s*[().\w]+;", source_line)
            if len(temp) > 0:
                if temp[0][0] in data.keys():
                    if temp[0][1] not in data[temp[0][0]]:
                        data[temp[0][0]].append(temp[0][1])
                else:
                    data[temp[0][0]] = [temp[0][1]]

            # instance variables: format -> [name] = new [str];
            temp = re.findall(r"(\w+)\s*=\s*new\s+(\w+)\s*[().\w]+;", source_line)
            if len(temp) > 0:
                if temp[0][1] in data.keys():
                    if temp[0][0] not in data[temp[0][1]]:
                        data[temp[0][1]].append(temp[0][0])
                else:
                    data[temp[0][1]] = [temp[0][0]]
                
            # primitive variables: format -> [int|float|byte|char|boolean|short|long|double] [name] = [str];
            temp = re.findall(r"(int|float|byte|char|boolean|short|long|double)\s+(\w+)\s*(=\s*|\w|\s*)*;", source_line)
            if len(temp) > 0:
                if temp[0][0] in data.keys():
                    if temp[0][1] not in data[temp[0][0]]:
                        data[temp[0][0]].append(temp[0][1])
                else:
                    data[temp[0][0]] = [temp[0][1]]

            # non-primitive variables: format -> [String] [name] = [str];
            temp = re.findall(r"(String)\s+(\w+)\s*(=\s*|\w|\s*)*;", source_line)
            if len(temp) > 0:
                if temp[0][0] in data.keys():
                    if temp[0][1] not in data[temp[0][0]]:
                        data[temp[0][0]].append(temp[0][1])
                else:
                    data[temp[0][0]] = [temp[0][1]]

            # array variables: format -> [str[]] [name] = [str];
            temp = re.findall(r"(\w+)(\[{1}\]{1})+\s+(\w+)\s*", source_line)
            if len(temp) > 0:
                print(temp)
                key = temp[0][0] + temp[0][1]
                if key in data.keys():
                    if temp[0][2] not in data[key]:
                        data[temp[0][0]].append(temp[0][2])
                else:
                    data[key] = [temp[0][2]]

        return data

    def print_data(self):
        classes = self.classes()

        print("--------------------------------------------")
        print("------------------ START -------------------")
        print("--------------------------------------------")
        print("")
        print("CLASSES - {}".format(len(classes['all'])))
        print("Overall classes {}".format(classes['all']))
        print("")
        print("-- TYPES")
        for key in classes:
            if key != 'all' and len(classes[key]) > 0:
                print("---- {} - {} -> {}".format(key, len(classes[key]), classes[key]))
        print("--------------------------------------------")

        variables = self.variables()

        print("---------------------")
        print("---------------------")
        print("")
        print("VARIABLES")
        variables_types = [n for n in variables]
        print("Type of variables used - {} -> {}".format(len(variables), variables_types))
        print("")
        print("-- TYPES")
        for key in variables:
            if len(variables[key]) > 0:
                print("---- {} - {} -> {}".format(key, len(variables[key]), variables[key]))
        print("--------------------------------------------")

        loc = self.loc()

        print("---------------------")
        print("---------------------")
        print("")
        print("OTHER INFORMATION")
        print("")
        print("-- Lines of code")
        print("---- LOC -> {}".format(loc['loc']))
        print("-- Source Lines of code")
        print("---- SLOC -> {}".format(loc['sloc']))
        print("-- Comments Lines of code")
        print("---- CLOC -> {}".format(loc['cloc']))
        print("-- Non-Comments Lines of code")
        print("---- NCLOC -> {}".format(loc['ncloc']))
        print("")
        print("--------------------------------------------")
        print("------------------- END --------------------")
        print("--------------------------------------------")
