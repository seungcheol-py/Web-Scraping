from flask import Flask, render_template, request, redirect
from indeed import get_jobs as get_indeed_jobs
# from so import get_jobs as get_so_jobs

app=Flask("SuperScrapper")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    word=request.args.get("word")
    if word:
        word=word.lower()
        indeed_jobs=get_indeed_jobs(word)
        # so_jobs= get_so_jobs(word)
        if indeed_jobs==None:
        # and so_jobs==None:
            return render_template("none.html", word=word)
        print(indeed_jobs)
    else:
        return redirect("/")
    # URL에서 report 뒤를 지우면 word는 None이 되어 error가 뜨니 이를 막자
    return render_template("report.html", word=word)

app.run(host="192.168.1.3")