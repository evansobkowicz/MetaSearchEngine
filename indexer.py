# COMP 490 - Lab 3
# Evan Sobkowicz

import os
import string
import math
import pickle
from WebDB import *
import calc


class Indexer:

    # Initialize
    the_index = dict()              # Index Structure: the_index = { term : { document_id : [position] } }
    df_index = dict()               # Initialize document frequency index. Structure: df_index = { term : idf }
    norm_index = dict()             # Initialize normalized index. Structure: norm_index = { docID : magnitude }
    regenerate_index = False        # Change this to use pickle file or regenerate index
    db = WebDB("data/cache.db")     # Connect to the database
    total_docs = db.totalURLs()     # Get total documents (URLs)
    calc = calc.Calc()              # Initialize calculations object

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

    # Done: Get Total # Documents (query db)
    # Done: Add -1 or some weight as the first item in the position list
    # Done: Maybe? Add DF Index df['term'] = idf_score
    # Done: Normalization (pass 2 - loop over all terms and docs in the index)
    #   Done: (continued) norm[docID] = (float) sum over all terms for 1+log(len(index['term'][docID])) * idf[term]
    # Done: (pass 3 - loop over all terms and docs in the index) set this
    #   Done: (continued)   as the weight in the position index (ltc): len([term][docID])/sqrt(norm[docID]

    # Normalization
    def normalize_scores(self):
        for term in self.the_index:
            idf = self.df_index[term]
            for doc_id in self.the_index[term]:
                self.norm_index[doc_id] = self.calc.log_tf(len(self.the_index[term][doc_id])) * idf
        print(self.norm_index)

    # Set Weight Magnitudes
    def assign_weights(self):
        for term in self.the_index:
            for doc_id in self.the_index[term]:
                self.the_index[term][doc_id][0] = len(self.the_index[term][doc_id]) / math.sqrt(self.norm_index[doc_id])
        self.print_index()

    '''
     For a query (nnn)...
     "Honey Badger"
     1. break into stemmed tokens
     2. setup score[docID]
     3. loop over query terms
            loop over docIDs for term
                score[docID] += weight (from positional index)
    4. sort docIDs by score
    5. print out top 5 docIDs w/score

     '''

    # Generate Document Frequency Index
    def generate_df_index(self):
        for term in self.the_index:
            self.df_index[term] = self.calc.idf(len(self.the_index[term]), self.total_docs)


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



    def print_index(self):
        for term in self.the_index:
            print(term)
            for doc_id in self.the_index[term]:
                print("\t", doc_id, "\t---\t", self.the_index[term][doc_id][0])
                for position in self.the_index[term][doc_id]:
                    print("\t\t", position)