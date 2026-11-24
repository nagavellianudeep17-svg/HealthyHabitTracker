import json, csv, os
from config import DATA_DIR
from datetime import datetime

JSON_PATH=os.path.join(DATA_DIR,"habits.json")
CSV_PATH=os.path.join(DATA_DIR,"habits.csv")
FIELDS=["id","date","habit","amount","unit","note","created_at"]

def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(JSON_PATH):
        save_records([])
    if not os.path.exists(CSV_PATH):
        export_csv([])

def load_records():
    ensure_files()
    try:
        with open(JSON_PATH,"r",encoding="utf-8") as f:
            raw=json.load(f)
        if not isinstance(raw,list): raise ValueError("Data file must contain a list.")
        valid=[]
        for item in raw:
            if isinstance(item,dict) and all(k in item for k in ["id","date","habit","amount","unit"]):
                try: item["amount"]=float(item["amount"]); valid.append(item)
                except (ValueError,TypeError): pass
        return valid
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        os.makedirs("logs",exist_ok=True)
        with open("logs/recovery.log","a",encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - Storage recovery: {exc}\\n")
        if os.path.exists(JSON_PATH):
            backup=JSON_PATH+".corrupt"
            try: os.replace(JSON_PATH,backup)
            except OSError: pass
        save_records([])
        return []

def save_records(records):
    os.makedirs(DATA_DIR,exist_ok=True)
    with open(JSON_PATH,"w",encoding="utf-8") as f:
        json.dump(records,f,indent=2,ensure_ascii=False)
    export_csv(records)

def export_csv(records, path=CSV_PATH):
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        for r in records: w.writerow({k:r.get(k,"") for k in FIELDS})

def import_csv(path):
    accepted, errors=[],[]
    with open(path,"r",newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        required={"date","habit","amount"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            return [], ["CSV must include date, habit and amount columns."]
        for rownum,row in enumerate(reader,2):
            try:
                from validation import validate_record
                habit=row.get("habit","").strip()
                date=row.get("date","").strip()
                amount=row.get("amount","").strip()
                note=row.get("note","").strip()
                problems=validate_record(date,habit,amount,note)
                if problems: errors.append(f"Row {rownum}: "+"; ".join(problems)); continue
                from config import HABITS
                accepted.append({"id":row.get("id") or "", "date":date,"habit":habit,"amount":float(amount),
                    "unit":HABITS[habit]["unit"],"note":note,"created_at":row.get("created_at") or ""})
            except Exception as e: errors.append(f"Row {rownum}: {e}")
    return accepted,errors
