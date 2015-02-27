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
    df_index = dict()               # Initialize document frequency index. Structure: df_index = { term : idf }
    norm_index = dict()             # Initialize normalized index. Structure: norm_index = { docID : magnitude }
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

    # Generate Document Frequency Index
    def generate_df_index(self):
        for term in self.the_index:
            self.df_index[term] = math.log10(self.total_docs/len(self.the_index[term].keys()))

    # tf_idf
    def tf_idf(self):
        print("Calculating tf-idf weights...")
        for term in self.the_index:
            idf = self.df_index[term]
            for doc_id in self.the_index[term]:
                if doc_id not in list(self.norm_index.keys()):
                    # If key doesn't exist, create it
                    self.norm_index[doc_id] = 0
                self.norm_index[doc_id] += ((1 + math.log10(len(self.the_index[term][doc_id]) - 1)) * idf)


    # Set Weight Magnitudes
    def assign_weights(self):
        tf_idf_total = dict()
        for term in self.the_index:
            for doc_id in self.the_index[term]:
                if term not in list(tf_idf_total.keys()):
                    tf_idf_total[doc_id] = 0
                tf_idf_total[doc_id] += math.pow(self.norm_index[doc_id], 2)
        for term in self.the_index:
            for doc_id in self.the_index[term]:
                self.the_index[term][doc_id][0] = self.norm_index[doc_id] / math.sqrt(tf_idf_total[doc_id])

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


# Done: Get Total # Documents (query db)
# Done: Add -1 or some weight as the first item in the position list
# Done: Maybe? Add DF Index df['term'] = idf_score
# Done: Normalization (pass 2 - loop over all terms and docs in the index)
#   Done: (continued) norm[docID] = (float) sum over all terms for 1+log(len(index[term][docID])) * idf[term]
# Done: (pass 3 - loop over all terms and docs in the index) set this
#   Done: (continued)   as the weight in the position index (ltc): len([term][docID])/sqrt(norm[docID]