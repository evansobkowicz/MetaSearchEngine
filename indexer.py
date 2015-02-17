# COMP 490 - Lab 3
# Evan Sobkowicz

import os
import string
import pickle

class Indexer:

    # Initializers
    the_index = dict()          # Index Structure: the_index = { term : { document_id : [position] } }
    regenerate_index = False     # Change this to use pickle file or regenerate index

    # Index Generator (or load from file)
    def index(self):
        if self.regenerate_index:
            path = 'data/clean/'
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    file_name, file_extension = os.path.splitext(file)
                    file_path = path + file_name + file_extension
                    if file_extension == '.txt':
                        terms = self.read_file(file_path)
                        self.process_terms(int(file_name), terms)
            self.save_index()
            return self.the_index
        else:
            self.load_index()
            return self.the_index


    # Save the index to a pickle file
    def save_index(self):
        pickle.dump(self.the_index, open("data/index.p", "wb"))


    # Load the index from the pickle file
    def load_index(self):
        self.the_index = pickle.load(open("data/index.p", "rb"))


    # Read lines from file
    def read_file(self, file):
        results = list()
        f = open(file, "r", encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            clean_line = line.strip('\n')
            results.append(clean_line)
        f.close()
        return results


    # Add terms to index
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
