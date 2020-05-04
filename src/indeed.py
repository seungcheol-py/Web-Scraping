import requests
from bs4 import BeautifulSoup

LIMIT=50

def extract_indeed_pages(url):
    result= requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class":"pagination"})
    divs= soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    if pagination == None:
        if divs ==None: 
            return 0
            # 검색 결과가 없음
        else:
            return 1
    links= pagination.find_all('a')
    pages=[]
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page=pages[-1]
    return max_page

def extract_job(div):
    title=div.find("h2", {"class": "title"}).find("a")["title"]
    company=div.find("span", {"class": "company"})
    if company == None:
        company=None
        # company 이름 없는 경우
    else:
        company_anchor = company.find("a")
        if company_anchor==None:
            company=company.text
        else:
            company=company_anchor.string
            company =company.strip()
    location=div.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id=div["data-jk"]
    return {"title":title, "company":company, "location":location,
    "address": f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?cmp=Bepro-Company&t=Ios+Developer&jk={job_id}"}

def extract_indeed_jobs(last_page, url):
    jobs=[]
    for page in range(int(last_page)):
        print(f"Scraping page {page+1}")
        result= requests.get(f"{url}&start={LIMIT*page}")
        # def get_jobs에 선언되어 있는 url 변수가 필요해서
        # url을 두 번째 변수로 받아왔다.. 대단하다..
        soup = BeautifulSoup(result.text, 'html.parser')
        divs= soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for div in divs:
            job= extract_job(div)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url=f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={word}&limit={LIMIT}"
    last_page = extract_indeed_pages(url)
    if last_page == 0:
        return None
    jobs=extract_indeed_jobs(last_page, url)
    return jobs