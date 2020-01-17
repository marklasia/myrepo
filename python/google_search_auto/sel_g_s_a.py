# tested with ipython on macOS 10.14

#importing necessary libraries
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import date

#importing selenium webdriver that will control Chrome in an automated way
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#import user_agents commented out until library is used

#make sure the webdriver is in the correct directory and that it matches the browser version you have runnning on your machine
chrome_driver = '/Users/marklasia/Desktop/chromedriver'
driver = webdriver.Chrome(chrome_driver)


#this function fetches the google search query and checks if the function is being called correctly
def fetch_results(search_term, number_results, language_code, number_pages):
    assert isinstance(search_term, str), 'Search term must be a string' #checking if the search term is a string
    assert isinstance(number_results, int), 'Number of results must be an integer' #checking if the number of results is an integer to prevent the code crashing
    assert isinstance(number_pages, int), 'Number of results must be an integer' #checking if the number of results is an integer to prevent the code crashing
    escaped_search_term = search_term.replace(' ', '+') #replace spaces in the search term with '+' so every search term is included in the results 

    
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code) #inputting our keywords in google url
    url_get = driver.get(google_url)

    date_accessed = date.today() #setting today's date that will be used to save the date the data was scraped
    found_results = [] #initializing [list to store results]
    rank = 1 #initializing rank variable used to keep track of which result we're scraping
    #result_block = soup.find_all('div', attrs={'class': 'g'}) #finding all div tags
    result_block = driver.find_elements_by_xpath('//a') #finding all links

    for result in result_block:
        if not 'google' in str(result.get_attribute("href")) and result.get_attribute("href") is not None: #skip any google or null links
            link = result.get_attribute("href")
            if link.endswith('.pdf'): #if the link is a pdf, save the link but don't parse the pdf (will have to develop code to support pdf scraping in the future)
                    link_html = 'File is a pdf, code currently does not support PDF scraping'
            
            found_results.append({'keyword': search_term, 'link':link, 'date accessed':date_accessed, 'html':link_html}) #NEED TO GET BEAUTIFUL SOUP TO SAVE THE LINK HTML HERE
     
    time.sleep(10) #sleep between requests so they seem human
    next_button = driver.find_element_by_id('pnnext')                 
    next_button.click() #going to the next page to start scraping

    #contact_df = pd.DataFrame(list(set(contact_list)))
    
    if number_pages > 1:
        #Switching to next page on Google. NEED TO ADAPT CODE WITH NEW APPROACH ABOVE
        for num_page in range(number_pages):
            try: 
                result_block = driver.find_elements_by_xpath('//a')
                for result in result_block:
                    if not 'google' in str(result.get_attribute("href")) and result.get_attribute("href") is not None:
                        found_results.append(result.get_attribute("href"))

                next_button = driver.find_element_by_id('pnnext')                 
                next_button.click()
            except Exception as e:
                print(e)
            finally:
                time.sleep(5)
    
            
    return found_results
    """
    for result in result_block: #looping through all results
        link = result.find('a', href=True) #saving the link from html file
        title = result.find('h3') #saving title from result
        description = result.find('span', attrs={'class': 'st'}) #saving description from result
        
        if link and title: #only saving if both link and title successfully found
            link = link['href']
            title = title.get_text()
            
            if description:
                description = description.get_text()
                
            if link != '#': #link is not a anchor
                
                if link.endswith('.pdf'): #if the link is a pdf, save the link but don't parse the pdf (will have to develop code to support pdf scraping in the future)
                    link_html = 'File is a pdf, code currently does not support PDF scraping'
                    found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description, 'link':link, 'date accessed':date_accessed, 'html':link_html})
                    rank += 1
                
                else :
                    link_request = requests.get(link)
                    link_soup = BeautifulSoup(link_request.text, 'html.parser') 
                    #link_html = link_request.text
                    p_tags = link_soup.findAll('p') #returns a list of all <p> elements in the html code
                    #found_results.append(p_tags)
                    found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description, 'link':link, 'date accessed':date_accessed, 'html':p_tags})
                    rank += 1
                    
    return found_results   
    """

#calls fetch_results function and returns an error message if there's one of three common errors
def scrape_google(search_term, number_results, language_code):
    try:
        results = fetch_results(search_term, number_results, language_code)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

#main function calling all the other functions
def main():
    """
    #collecting user input
    user_input_keyword = input('Please enter the keyword(s) you would like to scrape google for ')
    keywords = [user_input_keyword]
    user_input_numresults = input('Please enter the number of google results you want to scrape ')
    user_input_numresults = int(user_input_numresults) #setting the input to an integer
    #user_input_lang = input('Please enter the language you would like google search for \("en" for English results\) ') commented out as we are only interested in English results
"""
    
    #keywords = ['boeing note to financial statements'] #future upgrade will prompt the user asking what keywords should be searched for
    scraping_data = []
    data = pd.read_csv('csr_report.csv')

    """
    counter_scrapes = 0
    #Checking if keywords were already scraped
    #Only scrape if haven't scraped already
    for keyword_data in data['keyword']:
        try: 
            if keyword_data == keywords[0]:
                counter_scrapes += 1
        except Exception as e:
            print(e)
            
    if counter_scrapes > 0:
        print('Already scraped for "' + keywords[0] + '" ' + str(i) + ' times.')
    else:
    """

    for quote in data['Quote']: #looping for each quote we're searching for
        try:
            results = scrape_google(keyword, user_input_numresults, "en")
            for result in results:
                scraping_data.append(result)
        except Exception as e:
            print(e) #catch and print out any error that pops up
        finally:
            time.sleep(20) #pausing(sleeping) between requests to make sure google doesn't block access
    #print(data)
                
    df_scraping_data = pd.DataFrame(scraping_data) #putting the data scrapped into a dataframe allowing us to save it to csv
    #print(df_scraping_data)
    df_scraping_data.to_csv('scraping_results.csv')
    """
    merged_data = data.append(df_scraping_data, sort=False)
    print(merged_data)
    merged_data.to_csv('merged_data.csv') #saving merged dataframe to a separate csv
    #df_scraping_data.to_csv('scraped_data.csv') #saving data to csv. Future uprade will include several ways of saving the data, including to a database
"""

#Start running the code if the file is initialised
if __name__ == '__main__':
    main()

