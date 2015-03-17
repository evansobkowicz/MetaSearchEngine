# COMP 490 - Lab 3/4
# Evan Sobkowicz

from indexer import *
from spider import *
import math

class Query:

    spider = Spider()   # Initialize Spider
    db = WebDB("data/cache.db")     # Connect to the database
    total_docs = db.totalURLs()     # Get total documents (URLs)

    # Initializer - generate the index and weights
    def __init__(self, document_type, query_type):
        self.document_type = document_type
        self.query_type = query_type
        # Set Up Index
        i = Indexer()
        i.index()
        if self.document_type == 'ltc':
            i.generate_idf_index()
            i.calculate_tf_idf()
            i.normalize_weights()
        else:
            i.calculate_nnn()
        self.index = i.get_index()

    # Scored Query (takes list() of terms)
    def score_query(self, terms, show_scores=True):
        scores = dict()         # { doc_id : weight accumulation }
        query = dict()          # { term : count of appearances in query }
        query_tf_idf = dict()   # { term : tf-idf }
        results = dict()        # { doc_id : score * index weight }
        stemmed = self.spider.stem(self.spider.lower(terms))
        for word in stemmed:
            if word not in query:
                query[word] = 0
            query[word] += 1
        if self.query_type == 'ltc':
            # ltc
            norm = 0
            for term in query:
                query_tf_idf[term] = (1 + math.log10(query[term])) * (math.log10(self.total_docs/len(self.index[term])))
                norm += math.pow(query_tf_idf[term], 2)
            for term in query:
                scores[term] = query_tf_idf[term] / math.sqrt(norm)
        else:
            # nnn
            for term in query:
                scores[term] = query[term]
        doc_ids = self.get_doc_ids(stemmed)
        for doc_id in doc_ids:
            for term in scores:
                if doc_id not in list(results.keys()):
                    results[doc_id] = 0
                if doc_id in list(self.index[term].keys()):
                    weight = self.index[term][doc_id][0]
                else:
                    weight = 0
                # dot product
                results[doc_id] += (scores[term] * weight)
        sorted_results = sorted(results.items(), key=lambda x: (-x[1], x[0]))
        if show_scores:
            return sorted_results
        else:
            sorted_list = list()
            for r in sorted_results:
                sorted_list.append(r[0])
            return sorted_list

    # Get all doc ids for each term's token query
    def get_doc_ids(self, terms):
        doc_ids = list()
        for term in terms:
            doc_ids.extend(self.token_query(term))
        return list(set(doc_ids))

    # Token Query
    def token_query(self, term):
        results = list()
        if term in list(self.index.keys()):
            results = list(self.index[term].keys())
        return results

    # AND Query
    def and_query(self, first, second):
        results = list()
        first_ids = self.token_query(first)
        second_ids = self.token_query(second)
        for id in first_ids:
            if id in second_ids:
                results.append(id)
        return results

    # OR Query
    def or_query(self, first, second):
        first_ids = self.token_query(first)
        second_ids = self.token_query(second)
        return first_ids + second_ids

    # Phrase Query
    def phrase_query(self, first, second):
        results = list()
        matches = list()
        and_results = self.and_query(first, second)
        for id in and_results:
            for position in self.index[first][id]:
                for position2 in self.index[second][id]:
                    if position == (position2 - 1):
                        matches.append(id)
        for id in matches:
            if id not in results:
                results.append(id)
        return results

    # Near Query
    def near_query(self, first, second, distance):
        results = list()
        matches = list()
        and_results = self.and_query(first, second)
        for id in and_results:
            for position in self.index[first][id]:
                for position2 in self.index[second][id]:
                    if (position - position2) <= distance:
                        matches.append(id)
        for id in matches:
            if id not in results:
                results.append(id)
        return results
