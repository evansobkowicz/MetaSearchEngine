# COMP 490 - Lab 3
# Evan Sobkowicz

from WebDB import *
from query import *
from spider import *

db = WebDB("data/cache.db")
spider = Spider()

def get_input():
    print_options()
    option_str = input("Please type a number (1-6): ")
    try:
        option = int(option_str)
    except:
        print("ERROR: Not a number!")
        return 6, "", ""
    if option == 6:
        return option, "", ""
    first = input("Please enter first word: ")
    if option != 1:
        second = input("Please enter second word: ")
    else:
        second = ""
    return option, first, second


def print_options():
    print(" ")
    print("Command Options:")
    print("1) Token query")
    print("2) AND query")
    print("3) OR query")
    print("4) Phrase query")
    print("5) Near query")
    print("6) QUIT")


def print_welcome():
    print(" ")
    print(" ")
    print(" ")
    print("Welcome to Evan's Boolean Search Engine!")
    print(" ")


def print_results_heading(type, term1, term2):
    print(" ")
    print("---------------------------------------------------------------------------------")
    print("SEARCH RESULTS:\t", type, "\t Term 1:", term1, "| Term 2:", term2)
    print("---------------------------------------------------------------------------------")
    print(" ")


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


def process_term(term):
    term_list = [term]
    return spider.stem(spider.lower(term_list))[0]


def main():
    print("Loading...")
    q = Query()
    query_type = 0
    print_welcome()
    while query_type != 6:
        query_type, first_word, second_word = get_input()
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
            results = q.near_query(first_term, second_term)
        else:
            print("See you next time!")
            break

        print_results_heading(query_type_string, first_word, second_word)
        if not results:
            print("***\tNo results found.\t***")
        else:
            count = 1
            for result in results:
                print_result(count, result)
                count += 1


main()