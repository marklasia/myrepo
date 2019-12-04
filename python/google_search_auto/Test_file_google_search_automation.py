from textblob import TextBlob
import requests 
from bs4 import BeautifulSoup
from sys import argv

class SearchGoogle:
    def __init__(self, term):
        self.term = term
        self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.term)

    def run (self):
        response = requests.get(self.url)
        #print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        headline_results = soup.find_all('div', class_='st')
        print(headline_results)
        for h in headline_results:
            print(h)
                


a = SearchGoogle('boeing')
a.run()

print(a.term)

