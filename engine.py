# COMP 490 - Lab 3
# Evan Sobkowicz

from WebDB import *
from query import *
from spider import *
from collections import Counter


# Initializers
db = WebDB("data/cache.db")
spider = Spider()


# Get and return user input
def get_input():
    print_options()
    distance = 0
    second = ""
    option_str = input("Please type a number (1-6): ")
    try:
        option = int(option_str)
    except:
        print("ERROR: Not a number!")
        return 6, "", "", 0
    if option == 6:
        return option, "", ""
    first = input("Please enter first word: ")
    if option != 1:
        second = input("Please enter second word: ")
    if option == 5:
        distance = input("Word Distance (integer): ")
    return option, first, second, int(distance)


# Print Options Menu
def print_options():
    print(" ")
    print("Command Options:")
    print("1) Token query")
    print("2) AND query")
    print("3) OR query")
    print("4) Phrase query")
    print("5) Near query")
    print("6) QUIT")


# Print Welcome Message
def print_welcome():
    print("\n\n\nWelcome to Evan's Boolean Search Engine!\n")


# Print Search Results Heading
def print_results_heading(type, term1, term2):
    print(" ")
    print("---------------------------------------------------------------------------------")
    print("SEARCH RESULTS:\t", type, "\t Term 1:", term1, "| Term 2:", term2)
    print("---------------------------------------------------------------------------------")
    print(" ")


# Print A Result
def print_result(count, id):
    url, docType, title = db.lookupCachedURL_byID(id)
    item, type = db.lookupItem_ByURLID(id)
    if count > 99:
        print(str(count) + ".\t", title)
    else:
        print(str(count) + ".\t\t", title)
    print("\t\t", url)
    print("\t\t", type + ": " + item)
    print(" ")
    return item


# Print Statistics
def print_stats(count, items):
    words_to_count = (term for term in items if term[:1].isupper())
    c = Counter(words_to_count)
    print("\n----------------------------------------------------------\n")
    print(count-1, "Results Found.")
    print("Most Frequent Items:")
    for term, num in c.most_common(3):
        print("\t" + term + ": " + str(num))
    print("\n----------------------------------------------------------\n")


# Lowercase and Stem an Individual Term
def process_term(term):
    term_list = [term]
    return spider.stem(spider.lower(term_list))[0]


# Main Search Engine Class
def main():
    print("Loading...")
    q = Query()
    query_type = 0
    print_welcome()
    while query_type != 6:
        query_type, first_word, second_word, distance = get_input()
        first_term = process_term(first_word)
        second_term = process_term(second_word)
        if query_type == 1:
            query_type_string = "Token Query"
            results = q.token_query(first_term)
        elif query_type == 2:
            query_type_string = "AND Query"
            results = q.and_query(first_term, second_term)
        elif query_type == 3:
            query_type_string = "OR Query"
            results = q.or_query(first_term, second_term)
        elif query_type == 4:
            query_type_string = "Phrase Query"
            results = q.phrase_query(first_term, second_term)
        elif query_type == 5:
            query_type_string = "Near Query"
            results = q.near_query(first_term, second_term, distance)
        else:
            print("See you next time!")
            break

        print_results_heading(query_type_string, first_word, second_word)
        if not results:
            print("***\tNo results found.\t***")
        else:
            count = 1
            items = list()
            for result in results:
                item = print_result(count, result)
                items.append(item)
                count += 1
            print_stats(count, items)


main()