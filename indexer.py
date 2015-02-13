import os
import string

class Indexer:

    # the_index = { term : { document_id : [position] } }
    the_index = dict()

    def index(self):
        path = 'data/clean/'
        for subdir, dirs, files in os.walk(path):
            for file in files:
                file_name, file_extension = os.path.splitext(file)
                file_path = path + file_name + file_extension
                if file_extension == '.txt':
                    terms = self.read_file(file_path)
                    self.process_terms(int(file_name), terms)
        return self.the_index



    def read_file(self, file):
        results = list()
        f = open(file, "r", encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            clean_line = line.strip('\n')
            results.append(clean_line)
        f.close()
        return results


    def process_terms(self, id, terms):
        position = 0
        for term in terms:
            if term in self.the_index.keys():
                if id in list(self.the_index[term].keys()):
                    self.the_index[term][id].append(position)
                else:
                    self.the_index[term][id] = [position]
            else:
                self.the_index[term] = { id : [position] }
            position += 1


