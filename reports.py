import os
from datetime import datetime
from analytics import summary_text
from storage import export_csv

def export_reports(records):
    os.makedirs("reports",exist_ok=True)
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    txt=summary_text(records)
    md="## "+txt.replace("\\n","\\n")
    with open(f"reports/summary_{stamp}.md","w",encoding="utf-8") as f:f.write(md)
    with open(f"reports/summary_{stamp}.txt","w",encoding="utf-8") as f:f.write(txt)
    export_csv(records,f"reports/records_{stamp}.csv")
    return [f"reports/summary_{stamp}.md",f"reports/summary_{stamp}.txt",f"reports/records_{stamp}.csv"]

def audit(message):
    os.makedirs("logs",exist_ok=True)
    with open("logs/audit.log","a",encoding="utf-8") as f:f.write(f"{datetime.now().isoformat()} | {message}\\n")
