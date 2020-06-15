import nltk
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import copy

class Util:
    @staticmethod
    def normalize_string(lines):
        replaceLines=lines
        normalizedLines=''
        for line in replaceLines.split('\n'):
            for word in line.split(' '):
                if word not in features:
                    line=line.replace(word,'')
            normalizedLines+=line
        return normalizedLines

    @staticmethod
    def tokenize_string(normalized):
        return nltk.word_tokenize(normalized)
        
    @staticmethod
    def token_ngram(tokenized):
        return nltk.ngrams(tokenized, ngram_value)
        
    @staticmethod
    def frequency(ngram_object):
        return nltk.FreqDist(ngram_object)

    @staticmethod
    def vector_assignment(frequency, feature_vector):
        
        dup = copy.deepcopy(feature_vector)
        for vector in dup:
            if vector in frequency:
                dup[vector] = frequency[vector]
        return dup

    @staticmethod
    def cosine_similarity(dataframe_1, dataframe_2):
        return float(cosine_similarity(dataframe_1.values, dataframe_2.values))


    @staticmethod
    def empty_feature_vector():
        empty_feature = {}
        for f in nltk.ngrams(features, ngram_value):
            empty_feature[f] = 0
        return empty_feature
    

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


if __name__ == "__main__":
    
    features = ['package','public','private','protected','class','abstract','interface','extends','implements','try','catch','finally','throw','throws','void','static','final','finalize','import']
    ngram_value = 2

    rf = ReadFile('test/file_1.java')
    string_data_1 = rf.read_string()
    rf.clear()
    normalized_1 = Util.normalize_string(string_data_1)
    tokenized_1 = Util.tokenize_string(normalized_1)
    feature_vector_1 = Util.empty_feature_vector()
    ngram_object_1 = Util.token_ngram(tokenized_1)
    frequency_1 = Util.frequency(ngram_object_1)
    vector_1 = Util.vector_assignment(frequency_1, feature_vector_1)
    df_1 = pd.DataFrame([vector_1])

    rf = ReadFile('test/file_2.java')
    string_data_2 = rf.read_string()
    rf.clear()
    normalized_2 = Util.normalize_string(string_data_2)
    tokenized_2 = Util.tokenize_string(normalized_2)
    feature_vector_2 = Util.empty_feature_vector()
    ngram_object_2 = Util.token_ngram(tokenized_2)
    frequency_2 = Util.frequency(ngram_object_2)
    vector_2 = Util.vector_assignment(frequency_2, feature_vector_2)
    df_2 = pd.DataFrame([vector_2])

    similarity = Util.cosine_similarity(df_1, df_2)
    print(similarity)
