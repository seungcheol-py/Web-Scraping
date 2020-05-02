import csv

def save_to_file(jobs):
    file=open("storage.csv", mode="w", newline="", encoding="utf-8")
    writer=csv.writer(file)
    writer.writerow(["Title", "Company", "Location", "Address"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return