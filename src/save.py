import csv

def save_to_file(jobs):
    file=open("storage.csv", mode="w", newline="", encoding="utf-8")
    writer=csv.writer(file)
    writer.writerow(["Title", "Company", "Location", "Address"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return
    # 여기서 return은 함수에서 빠져나오는 return인 것 같다.