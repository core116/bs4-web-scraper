# import request and Beautiful Soup
import requests
from bs4 import BeautifulSoup
import argparse

def scrape_jobs(location=None):
    """Scrapes Data Scientist job postings from Monster, optionally by location.

    :param location: Where the job is located
    :type location: str
    :return: all job posting from first page that matches the search result
    :rtype: BeautifulSoup Object
    """
    if location:
        url = (f'https://www.monster.com/jobs/search/'
               f'?q=Data-Scientist&where={location}&rad=200&tm=14')
    else:
        url = 'https://www.monster.com/jobs/search/?q=Data-Scientist'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    return results

def filter_jobs_by_keyword(results, word):
    """Filter job posting by word and print matching job title and link

    :param results: Parsed HTML container with all job listings
    :type results: BeautifulSoup Object
    :param word: keyword to filter by
    :return: None - meant to just print results
    :rtype: None
    """
    data_scientist_jobs = results.find_all('h2', string=lambda text: word in text.lower())
    for ds_jobs in data_scientist_jobs:
        link = ds_jobs.find('a')['href']
        print(ds_jobs.text.strip())
        print(f'Apply here: {link}\n')

def print_all_jobs(results):
    """Print all jobs return by the search
    The printed job details are job title, company name, job location and link

    :param results: Parsed HTML container with all job listing
    :type results: BeautifulSoup Object
    :return: None - meant to just print results
    :rtype: None
    """
    job_elems = results.find_all('section', class_='card-content')

    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('div', class_='company')
        location_elem = job_elem.find('div', class_='location')
        if None in (title_elem, company_elem, location_elem):
            continue
            # print(job_elem.prettify()) # to inspect the 'None' element
        print(title_elem.text.strip())
        print(company_elem.text.strip())
        print(location_elem.text.strip())
        link_elem = title_elem.find('a')
        print(link_elem['href'])
        print()

# USE THE SCRIPT AS A COMMAND-LINE INTERFACE
#______________________________________________________________________________________
my_parser = argparse.ArgumentParser(
    prog='jobs', description='Find Data Scientist Jobs'
)
my_parser.add_argument(
    '-location', metavar='location', type=str, help='The location of the job'
)
my_parser.add_argument(
    '-word', metavar='word', type=str, help='What keyword to filter by'
)

args = my_parser.parse_args()
location, keyword = args.location, args.word

results = scrape_jobs(location)
if keyword:
    filter_jobs_by_keyword(results, keyword.lower())
else:
    print_all_jobs(results)