from flask import Flask, render_template, request, redirect, send_file
from indeed import get_jobs as get_indeed_jobs
from save import save_to_file
# from so import get_jobs as get_so_jobs

app=Flask("SuperScrapper")

db={}

@app.route("/")
def home():
    print(request)
    return render_template("home.html")

@app.route("/report")
def report():
    word=request.args.get("word")
    if word:
        word=word.lower()
        dbWord=db.get(word)
        if dbWord:
            jobs=dbWord
        else:
            jobs=get_indeed_jobs(word)
            if jobs==None:
                return render_template("none.html", word=word)
            db[word]=jobs  #indeed_jobs의 형태 [{'title':'모집공고','company':'주식회사'},{'title':'~~'}]    {'word': jobs의 형태 그대로}
    else:
        return redirect("/")
    # URL에서 report 뒤를 지우면 word는 None이 되어 error가 뜨니 이를 막자
    return render_template("report.html", word=word, number=len(jobs), jobs=jobs)
    # [] 안에 있는 {}의 숫자

@app.route("/export")
def export():
    try:
        word=request.args.get("word")
        if not word:
            raise Exception()
        word=word.lower()
        dbWord=db.get(word)
        if not dbWord:
            raise Exception()
        save_to_file(dbWord)
        # Web-scraping 폴더에 csv 파일이 저장된다.
        return send_file("storage.csv")
        # export를 누른 사람에게 다운로드된다.
    except:
        return redirect("/")


app.run(host="192.168.1.6")