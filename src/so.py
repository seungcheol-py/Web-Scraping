import requests
from bs4 import BeautifulSoup

def extract_so_pages(url):
    result=requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination =soup.find("div", {"class": "s-pagination"})
    if pagination ==None:
        return 0
    links=pagination.find_all("a")
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

def extract_so_jobs(last_page, url):
    jobs=[]
    for page in range(int(last_page)):
        page=page+1
        print(f"Scraping page {page}")
        result=requests.get(f"{url}&pg={page}")
        soup = BeautifulSoup(result.text, 'html.parser')
        divs= soup.find_all("div", {"class": "-job"})
        for div in divs:
            job= extract_job(div)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url=f"https://stackoverflow.com/jobs?q={word}"
    last_page=extract_so_pages(url)
    if last_page == 0:
        return None
    jobs=extract_so_jobs(last_page, url)
    return jobs