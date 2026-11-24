from storage import load_records,save_records
from habit_engine import make_record,filter_records,weekly_summary
from config import HABITS
from analytics import make_chart,summary_text
from reports import export_reports,audit
from datetime import date
import os

def cli():
    records=load_records()
    while True:
        print("\\n=== HEALTHY HABIT TRACKER ===")
        print("1 Add record  2 View records  3 Search/filter  4 Weekly summary  5 Chart  6 Export reports  0 Exit")
        choice=input("Choose: ").strip()
        if choice=="0": save_records(records); print("Goodbye!"); break
        elif choice=="1":
            d=input("Date YYYY-MM-DD (blank=today): ").strip() or date.today().isoformat()
            print("Habits:",", ".join(HABITS))
            h=input("Habit: ").strip().title(); a=input(f"Amount ({HABITS.get(h,{}).get('unit','unit')}): ").strip(); n=input("Note: ").strip()
            try: records.append(make_record(d,h,a,n)); save_records(records); audit("Added record"); print("Saved.")
            except ValueError as e: print("Validation:",e)
        elif choice=="2":
            for r in filter_records(records): print(f"{r['date']} | {r['habit']} | {r['amount']} {r['unit']} | {r.get('note','')}")
        elif choice=="3":
            kw=input("Keyword: "); h=input("Habit (blank=all): "); start=input("Start date YYYY-MM-DD (blank=any): "); end=input("End date YYYY-MM-DD (blank=any): ")
            for r in filter_records(records,kw,h,start,end): print(f"{r['date']} | {r['habit']} | {r['amount']} {r['unit']} | {r.get('note','')}")
        elif choice=="4": print(summary_text(records))
        elif choice=="5":
            p=make_chart(records); print(f"Chart saved: {p}" if p else "Install matplotlib to create charts.")
        elif choice=="6": print("Created:",export_reports(records))
        else: print("Please choose a valid menu item.")
