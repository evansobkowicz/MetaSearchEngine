# Evan Sobkowicz
# COMP 490 - Lab 1

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from socket import timeout
from bs4 import BeautifulSoup
import bs4
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer


class Spider:

    def fetch(self, url):
        req = Request(url, None, {'User-agent': 'Firefox/3.05'})
        try:
            response = urlopen(req)
        except (HTTPError, URLError) as error:
            print('ERROR:  Could not retrieve', url, 'because', error)
            return -1
        except timeout:
            print('ERROR:  Socket timed out - URL: %s', url)
            return -1
        html = response.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html)
        if soup.html.head.title is not None:
            title = soup.html.head.title.get_text()
        else:
            title = ""
        [x.extract() for x in soup.findAll('script')]
        if soup.html.body is not None:
            body = soup.html.body.get_text()
        else:
            body = ""
        tokens = word_tokenize(body)
        terms = self.get_terms(tokens)
        lower_terms = self.get_terms(self.lower(terms))
        stem_terms = self.get_terms(self.stem(lower_terms))
        return title, response.info(), stem_terms, str(soup), self.doctype(soup)

    def doctype(self, soup):
        items = [item for item in soup.contents if isinstance(item, bs4.Doctype)]
        return items[0] if items else None

    def lower(self, tokens):
        lower_tokens = list()
        for w in tokens:
            lower_tokens.append(w.lower())
        return lower_tokens

    def stem(self, tokens):
        stemmed_tokens = list()
        ps = PorterStemmer()
        for word in tokens:
            stemmed_tokens.append(ps.stem(word))
        return stemmed_tokens

    def get_terms(self, tokens):
        terms = list()
        for word in tokens:
            if word not in terms:
                terms.append(word)
        terms.sort()
        return terms
