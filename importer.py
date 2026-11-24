from storage import import_csv,save_records
from reports import audit

def import_into_app(path,records):
    accepted,errors=import_csv(path)
    ids={r.get("id") for r in records}
    for r in accepted:
        if not r["id"] or r["id"] in ids:
            import uuid
            r["id"]=str(uuid.uuid4())
        ids.add(r["id"])
    records.extend(accepted)
    save_records(records)
    audit(f"CSV import: {len(accepted)} accepted; {len(errors)} rejected")
    return accepted,errors
