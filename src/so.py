import requests
from bs4 import BeautifulSoup

URL="https://stackoverflow.com/jobs?q=python"

def extract_so_pages():
    result=requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    links =soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page= links[-2].text.strip()
    # last_page= links[-2].get_text(strip=True)
    return last_page

def extract_job(div):
    title=div.find("a", {"class": "s-link"})["title"]
    company, location=div.find("h3", {"class": "fc-black-700"}).find_all("span", recursive=False)
    company=company.get_text(strip=True)
    location=location.get_text(strip=True)
    job_id=div["data-jobid"]
    return{"title":title, "company":company, "location": location,
    "address": f"https://stackoverflow.com/jobs/{job_id}"}

def extract_so_jobs(last_page):
    jobs=[]
    for page in range(int(last_page)):
        page=page+1
        print(f"Scraping page {page}")
        result=requests.get(f"{URL}&pg={page}")
        soup = BeautifulSoup(result.text, 'html.parser')
        divs= soup.find_all("div", {"class": "-job"})
        for div in divs:
            job= extract_job(div)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page=extract_so_pages()
    jobs=extract_so_jobs(last_page)
    return jobs