from indexer import *

def main():
    i = Indexer()
    index = i.index()

    for k, v in index.items():
        print(k, ':', v)





main()