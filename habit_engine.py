from datetime import date, datetime, timedelta
import uuid
from config import HABITS
from validation import validate_record

def make_record(date_text, habit, amount, note=""):
    errors=validate_record(date_text,habit,amount,note)
    if errors: raise ValueError("; ".join(errors))
    return {"id":str(uuid.uuid4()),"date":date_text,"habit":habit,"amount":float(amount),
            "unit":HABITS[habit]["unit"],"note":note.strip(),"created_at":datetime.now().isoformat(timespec="seconds")}

def filter_records(records, keyword="", habit="", start="", end=""):
    out=[]
    for r in records:
        if habit and r.get("habit")!=habit: continue
        if start and r.get("date","")<start: continue
        if end and r.get("date","")>end: continue
        if keyword and keyword.lower() not in " ".join(str(r.get(k,"")) for k in ["habit","note","date"]).lower(): continue
        out.append(r)
    return sorted(out,key=lambda r:(r.get("date",""),r.get("created_at","")),reverse=True)

def week_dates(anchor=None):
    anchor=anchor or date.today()
    monday=anchor-timedelta(days=anchor.weekday())
    return [monday+timedelta(days=i) for i in range(7)]

def weekly_summary(records, anchor=None):
    dates=week_dates(anchor)
    date_set={d.isoformat() for d in dates}
    current=[r for r in records if r.get("date") in date_set]
    result={}
    for habit,info in HABITS.items():
        items=[r for r in current if r.get("habit")==habit]
        total=sum(float(r.get("amount",0)) for r in items)
        daily={d.isoformat():sum(float(r.get("amount",0)) for r in items if r.get("date")==d.isoformat()) for d in dates}
        goal=info["daily_goal"]*7
        result[habit]={"total":total,"average":total/7,"goal":goal,"percentage":min(100,total/goal*100 if goal else 0),"daily":daily,"unit":info["unit"]}
    return dates,result,current
