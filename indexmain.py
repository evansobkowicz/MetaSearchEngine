from WebDB import *
from query import *

db = WebDB("data/cache.db")

def get_input():
    print_options()
    option = input("Please type a number (1-6): ")
    first = input("Please enter first word: ")
    if int(option) != 1:
        second = input("Please enter second word: ")
    else:
        second = ""
    return int(option), first, second


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
    print("Welcome to Evan's Boolean Search Engine!")
    print(" ")


def print_result(count, id):
    url, docType, title = db.lookupCachedURL_byID(id)
    item, type = db.lookupItem_ByURLID(id)
    print(str(count) + ".\t", title)
    print("\t", url)
    print("\t", type + ": " + item)



def main():
    q = Query()
    query_type = 0
    print_welcome()
    while query_type != 6:
        query_type, first_word, second_word = get_input()
        if query_type == 1:
            results = q.token_query(first_word)
        elif query_type == 2:
            results = q.and_query(first_word, second_word)
        elif query_type == 3:
            results = q.or_query(first_word, second_word)
        elif query_type == 4:
            results = q.phrase_query(first_word, second_word)
        elif query_type == 5:
            results = q.near_query(first_word, second_word)
        else:
            print("See you next time!")
            break

        print(query_type, first_word, second_word)
        print("Results:")
        if results == 0:
            print("No results found.")
        else:
            count = 1
            for result in results:
                print_result(count, result)
                count += 1



    # PRINT INDEX
    # for k, v in index.items():
    #     print(k, ':', v)



main()