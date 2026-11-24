# Healthy Habit Tracker

A local-first Python desktop application to track Reading, Exercise and Hydration over a week. Includes Tkinter GUI, terminal interface, input validation, JSON/CSV persistence, search, weekly analytics, Matplotlib charts, report exports and bulk CSV import.

## Requirements
- Python 3.10+
- Install optional plotting dependencies: `python -m pip install -r requirements.txt`

Tkinter is included in most Windows Python installations.

## Launch
```bash
python main.py
```
Launch terminal mode:
```bash
python main.py --cli
```

## Features
- Dashboard with weekly progress cards and goal progress
- Add, edit, delete entries with validation
- Search and date/category filters
- JSON persistence with CSV mirror
- Weekly totals, averages and progress calculations
- Matplotlib trend chart
- Markdown, plain-text, CSV report exports
- Bulk CSV import with row-level validation feedback
- Audit/recovery logs
- Demo seed data included in `data/sample_data.json`

## CSV import schema
Required columns: `date,habit,amount`. Optional: `id,unit,note,created_at`. Habits: Reading (minutes), Exercise (minutes), Hydration (litres).

## Test
```bash
python -m unittest discover -s tests
```

## Storage and privacy
All application data remains local in `data/`, `reports/`, `charts/`, and `logs/`. No account, server, or network connection is required.
