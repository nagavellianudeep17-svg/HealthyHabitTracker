from datetime import datetime
from config import HABITS

def validate_record(date_text, habit, amount_text, note=""):
    errors=[]
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except (ValueError, TypeError):
        errors.append("Date must be in YYYY-MM-DD format.")
    if habit not in HABITS:
        errors.append("Choose a supported habit.")
    try:
        amount=float(amount_text)
        if amount <= 0:
            errors.append("Amount must be greater than zero.")
        elif habit in HABITS and amount > HABITS[habit]["maximum"]:
            errors.append(f"Amount exceeds the maximum ({HABITS[habit]['maximum']} {HABITS[habit]['unit']}).")
    except (ValueError, TypeError):
        errors.append("Amount must be a valid number.")
    if len(str(note)) > 300:
        errors.append("Notes must be 300 characters or fewer.")
    return errors
