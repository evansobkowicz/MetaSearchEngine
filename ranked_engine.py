# COMP 490 - Lab 4
# Evan Sobkowicz

from WebDB import *
from query import *
from spider import *
from collections import Counter


# Initialize
db = WebDB("data/cache.db")
spider = Spider()


# Get and return user input
def get_input():
    return input("Enter Query or 'QUIT': ")


# Print Welcome Message
def print_welcome():
    print("\n\n\nWelcome to Evan's Boolean Search Engine!")
    print("Supported SMART variants: [n,l][n,t][n,c] (default is 'ltc')\n")


# Print Search Results Heading
def print_results_heading(query):
    print(" ")
    print("---------------------------------------------------------------------------------")
    print("SEARCH RESULTS: ", query)
    print("---------------------------------------------------------------------------------")
    print(" ")


# Print A Result
def print_result(count, id, score):
    url, docType, title = db.lookupCachedURL_byID(id)
    item, type = db.lookupItem_ByURLID(id)
    print(str(count) + ".\t\t", title, " (" + str(round(score, 4)) + ")")
    print("\t\t", url)
    print("\t\t", type + ": " + item)
    print(" ")


# Print Statistics
def print_stats(count, items, scores):
    words_to_count = (term for term in items if term[:1].isupper())
    c = Counter(words_to_count)
    print("\n----------------------------------------------------------\n")
    print(count-1, "Results Found.")
    print("Most Frequent Items:")
    for term, num in c.most_common(3):
        print("\t" + term + ": " + str(num) + " (Total Score: " + str(round(scores[term], 2)) + ")")
    print("\n----------------------------------------------------------\n")


# Get SMART Notation Variant Selections From User (use defaults if bad values)
def get_variants():
    document = input("Please enter SMART variant for documents ('ltc' or 'nnn'): ")
    query = input("Please enter SMART variant for queries ('ltc' or 'nnn'): ")
    if document == 'ltc' or document == 'nnn':
        document_out = document
    else:
        document_out = 'ltc'
    if query == 'ltc' or query == 'nnn':
        query_out = query
    else:
        query_out = 'nnn'
    print("\nUsing:", document_out + "." + query_out, "\n\n")
    return document_out, query_out


# Main Search Engine Class
def main():
    print("Loading...")
    query = ""
    print_welcome()
    document_type, query_type = get_variants()
    q = Query(document_type, query_type)
    print("Loading Index...")
    print("\n\n")
    while query != "QUIT":
        query = get_input()
        if query == "QUIT":
            print("Goodbye!")
            break
        tokens = spider.tokenize(query)
        results = q.score_query(tokens)
        print_results_heading(query)
        if not results:
            print("***\tNo results found.\t***")
        else:
            count = 1
            total_scores = dict()
            items = list()
            for result in results:
                # Print N=5 Results for the User
                if count <= 5:
                    print_result(count, result[0], result[1])
                # Accumulate Scores & Stats
                item, type = db.lookupItem_ByURLID(result[0])
                if item not in list(total_scores.keys()):
                    total_scores[item] = 0
                total_scores[item] += result[1]
                items.append(item)
                count += 1
            print_stats(count, items, total_scores)


main()