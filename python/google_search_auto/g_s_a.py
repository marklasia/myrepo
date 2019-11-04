# tested with ipython on macOS 10.14



#importing necessary libraries
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import date
#import user_agents commented out until library is used

#setting the user agent to mask our requests from python and make sure google does not block the requests made
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


#this function fetches the google search query and checks if the function is being called correctly
def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string' #checking if the search term is a string
    assert isinstance(number_results, int), 'Number of results must be an integer' #checking if the number of results is an integer to prevent the code crashing
    escaped_search_term = search_term.replace(' ', '+') #replace spaces in the search term with '+' so every search term is included in the results 

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code) #inputting our keywords in google url
    response = requests.get(google_url, headers=USER_AGENT) #fetches html of google search page
    response.raise_for_status() #returns http error if one arised

    return search_term, response.text #returns the search term and the html code of the google search page

#this function goes through the google page html and extracts the links from the results, their rank, title, description, and the timestamp of access
def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser') #initializing beautiful soup which will help us parse the google html webpage code
    date_accessed = date.today() #setting today's date that will be used to save the date the data was scraped
    found_results = [] #initializing [list to store results]
    rank = 1 #initializing rank variable used to keep track of which result we're scraping
    result_block = soup.find_all('div', attrs={'class': 'g'}) #finding all div tags 
    for result in result_block: #looping through all results

        link = result.find('a', href=True) #saving the link from html file
        title = result.find('h3') #saving title from result
        #html_save = requests.get(str(link)) #commented out code in progress
        description = result.find('span', attrs={'class': 'st'}) #saving description from result
        if link and title: #only saving if both link and title successfully found
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description, 'link':link, 'date accessed':date_accessed})
                rank += 1
    return found_results

#calls fetch_results function and returns an error message if there's one of three common errors
def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

#This is the main function that calls the functions defined above. Upgrades are needed here for usability
if __name__ == '__main__':
    keywords = ['boeing note to financial statements'] #future upgrade will prompt the user asking what keywords should be searched for
    data = []
    for keyword in keywords: #looping for each keyword we're searching
        try:
            results = scrape_google(keyword, 10, "en")
            for result in results:
                data.append(result)
        except Exception as e:
            print(e) #catch and print out any error that pops up
        finally:
            time.sleep(20) #pausing(sleeping) between requests to make sure google doesn't block access
    print(data)
    df = pd.DataFrame(data) #putting the data scrapped into a dataframe allowing us to save it to csv
    print(df)
    df.to_csv('scraped_data.csv') #saving data to csv. Future uprade will include several ways of saving the data, including to a database
