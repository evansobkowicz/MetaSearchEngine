# COMP 490 - Lab 2
# Evan Sobkowicz

import os, sys

from WebDB import *
from google import search
from spider import *

# Get item types from file names in item directory
def get_item_types():
    types = list()
    path = "data/item/"
    dirs = os.listdir(path)
    for dir in dirs:
        type = dir.strip('.txt')
        types.append(type)
    return types

# Read items from text file into a list
def get_items_by_type(type):
    results = list()
    path = "data/item/" + type + ".txt"
    f = open(path, "r")
    lines = f.readlines()
    for line in lines:
        clean_line = line.strip('\n')
        results.append(clean_line)
    f.close()
    return results

# Write 'contents' to a file named 'id' in the folder 'dir'
def write_to_file(id, dir, contents):
    file_path = "data/" + dir + "/" + str(id) + ".txt"
    f = open(file_path, "w", encoding='utf-8')
    output = ""
    if type(contents) == list:
        for item in contents:
            output += str(item)
            output += "\n"
    else:
        output = str(contents)
    try:
        f.write(str(output))
    except:
        print('ERROR: Could not write to', dir, 'file!')
    f.close()

# Create directories if they don't exist
def setup_directories():
    directories = ["clean", "header", "item", "raw"]
    for dir in directories:
        dir_path = "data/" + dir
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

# Main Loop
# Google, Parse, Add to DB, and Cache
def main():

    # Initialize
    count = 0
    spider = Spider()
    google_results = 10

    # Setup the Cache File Structure
    setup_directories()

    # Setup Database
    db = WebDB("data/cache.db")

    # For each list of items (movies, books, music)
    for type in get_item_types():

        print(type)

        # For each item in the list
        for item in get_items_by_type(type):

            print("\n", item)

            # Add the item to the database
            item_id = db.insertItem(db._quote(item), type)

            # Check to see if we already have enough URLs
            num_urls = db.numURLToItem(item_id)
            if num_urls >= 8:
                print("\tSKIPPING: Already have", str(num_urls), "urls for", item, ".\n")
                continue

            # Use Search Engine to find N=10 relevant URLs
            # For each URL
            for url in search(str(item), stop=google_results, pause=0.5):

                print("\t " + url)

                # Check if url is already cached
                if db.lookupCachedURL_byURL(url):
                    print("\t\t Already Cached!")
                else:

                    # Download, Parse, & Cache Each Website
                    try:
                      response = spider.fetch(url)
                    except TimeoutError:
                      print ("Skipping URL: timeout error")
                      continue
                    except ConnectionResetError:
                      print ("Skipping URL: Connection Reset Error")
                      continue

                    # Process the Spider's response
                    if response == -1:
                        # Failure in the Spider's fetching
                        print('ERROR: Spider fetch failure!')
                    else:
                        # Successful Spider response
                        page_title = db._quote(response[0])
                        headers = "Title: " + page_title + "\n" + str(response[1])
                        terms = response[2] # These are stemmed! (not unique)
                        html = response[3]
                        doc_type = response[4]

                        # Update information in database
                        url_id = db.insertCachedURL(url, doc_type, page_title)
                        url_to_item_id = db.insertURLToItem(url_id, item_id)

                        # Write cache files
                        write_to_file(url_id, "header", headers)
                        write_to_file(url_id, "raw", html)
                        write_to_file(url_id, "clean", terms)

                        # Status
                        print('\t\t Added Successfully!')
                        count += 1

    # Print the number of processed URLs
    print("Processed " + str(count) + " URLs.")



main()