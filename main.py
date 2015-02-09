# COMP 490 - Lab 2
# Evan Sobkowicz

import os, sys

from WebDB import *
from google import search
from spider import *


def get_item_types():
    types = list()
    path = "data/item/"
    dirs = os.listdir(path)
    for dir in dirs:
        type = dir.strip('.txt')
        types.append(type)
    return types

def get_items_by_type(type):
    results = list()
    path = "data/item/" + type + ".txt"
    f = open(path, "r")
    lines = f.readlines()
    for line in lines:
        cleanline = line.strip('\n')
        results.append(cleanline)
    f.close()
    return results

def write_to_file(id, dir, contents):
    file_path = "data/" + dir + "/" + str(id) + ".txt"
    f = open(file_path, "w", encoding='utf-8')
    output = ""
    if type(contents) == list:
        for item in contents:
            output += str(item)
            output += "\n"
    else:
        output = str(contents
    try:
        f.write(str(output))
    except:
        print('ERROR: Could not write to', dir, 'file!')
    f.close()

def setup_directories():
    directories = ["clean", "header", "item", "raw"]
    for dir in directories:
        dir_path = "data/" + dir
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def main():

    count = 0
    spider = Spider()

    # Setup the Cache Structure
    setup_directories()
    db = WebDB("data/cache.db")

    # For each list of items      movies, books, music artists
    for type in get_item_types():

        print(type)

        # For each item in the list
        for item in get_items_by_type(type):

            print(' ')
            print(item)

            item_id = db.insertItem(db._quote(item), type)

            # Use Search Engine to find N=10 relevant URLs
            # For each URL
            for url in search(str(item), stop=10, pause=0.5):

                print("\t " + url)

                if db.lookupCachedURL_byURL(url):
                    print("\t\t Already Cached!")
                else:

                    # Download, Parse, & Cache Each Website     # if not already in cache
                    response = spider.fetch(url)

                    if response == -1:
                        print('ERROR: Spider fetch failure!')
                    else:
                        page_title = db._quote(response[0])
                        headers = "Title: " + page_title + "\n" + str(response[1])
                        terms = response[2] # These are stemmed!
                        html = response[3]
                        doc_type = None

                        # Update information in cache database
                        url_id = db.insertCachedURL(url, doc_type, page_title)
                        url_to_item_id = db.insertURLToItem(url_id, item_id)

                        # Write files
                        write_to_file(url_id, "header", headers)
                        write_to_file(url_id, "raw", html)
                        write_to_file(url_id, "clean", terms)

                        # Status
                        print('\t\t Added Successfully!')
                        count += 1

    print("Processed " + str(count) + " URLs.")



main()