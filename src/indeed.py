import requests
from bs4 import BeautifulSoup

LIMIT=50
URL=f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"
def extract_indeed_pages():
    result= requests.get(URL)

    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find("div", {"class":"pagination"})

    links= pagination.find_all('a')

    pages=[]

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page=pages[-1]
    return max_page

def extract_job(div):
    title=div.find("h2", {"class": "title"}).find("a")["title"]
    company=div.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company=company_anchor.string
    else:
        company=company.string
    company =company.strip()
    print(title, company)

def extract_indeed_jobs(last_page):
    jobs=[]
    for page in range(last_page):
        result= requests.get(f"{URL}&start={LIMIT*page}")
        soup = BeautifulSoup(result.text, 'html.parser')
        divs= soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for div in divs:
            extract_job(div)
    return jobs
