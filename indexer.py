# COMP 490 - Lab 3/4
# Evan Sobkowicz

import os
import string
import math
import pickle
from WebDB import *


class Indexer:

    # Initialize
    the_index = dict()              # Index Structure: the_index = { term : { document_id : [position] } }
    idf_index = dict()              # Initialize document frequency index. Structure: df_index = { term : idf }
    regenerate_index = False        # Change this to use pickle file or regenerate index
    db = WebDB("data/cache.db")     # Connect to the database
    total_docs = db.totalURLs()     # Get total documents (URLs)

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
        else:
            self.load_index()

    # Get the Index
    def get_index(self):
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

    # (ltc) Generate Document Frequency Index (holds idf)
    def generate_idf_index(self):
        print("Generating DF Index & Storing IDF Values...")
        for term in self.the_index:
            self.idf_index[term] = math.log10(self.total_docs/len(self.the_index[term].keys()))

    # (ltc) tf_idf
    def calculate_tf_idf(self):
        print("Calculating TF-IDF...")
        for term in self.the_index:
            idf = self.idf_index[term]
            for doc_id in self.the_index[term]:
                self.the_index[term][doc_id][0] = ((1 + math.log10(len(self.the_index[term][doc_id]) - 1)) * idf)

    # (ltc) Set Weight Magnitudes
    def normalize_weights(self):
        print("Normalizing Weights...")
        for term in self.the_index:
            tf_idf_total = 0
            for doc_id in self.the_index[term]:
                tf_idf_total += math.pow(self.the_index[term][doc_id][0], 2)
            for doc_id in self.the_index[term]:
                self.the_index[term][doc_id][0] = (self.the_index[term][doc_id][0] / math.sqrt(tf_idf_total))

    # (nnn) NNN TF Calculations (check math)
    def calculate_nnn(self):
        for term in self.the_index:
            for doc_id in self.the_index[term]:
                self.the_index[term][doc_id][0] = 1 + math.log10(len(self.the_index[term][doc_id]) - 1)

    # Add terms to index
    def process_terms(self, id, terms):
        position = 0
        for term in terms:
            if term in self.the_index.keys():
                if id in list(self.the_index[term].keys()):
                    self.the_index[term][id].append(position)
                else:
                    self.the_index[term][id] = [-1, position]
            else:
                self.the_index[term] = { id : [-1, position] }
            position += 1

    # Helper method to print out the entire index
    def print_index(self):
        for term in self.the_index:
            print(term)
            for doc_id in self.the_index[term]:
                print("\t", doc_id, "\t---\t", self.the_index[term][doc_id][0])
                print("\t\t", len(self.the_index[term][doc_id]), " positions")
