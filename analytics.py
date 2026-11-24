from habit_engine import weekly_summary,week_dates
from config import HABITS
import os

def make_chart(records, anchor=None, output_path="charts/weekly_progress.png"):
    os.makedirs(os.path.dirname(output_path) or ".",exist_ok=True)
    dates,summary,_=weekly_summary(records,anchor)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    fig,ax=plt.subplots(figsize=(10,4.8))
    labels=[d.strftime("%a") for d in dates]
    for habit,info in summary.items():
        vals=[info["daily"][d.isoformat()] for d in dates]
        ax.plot(labels,vals,marker="o",linewidth=2,label=f"{habit} ({info['unit']})")
    ax.set_title("Weekly Habit Activity"); ax.set_ylabel("Amount"); ax.grid(axis="y",alpha=.25); ax.legend()
    fig.tight_layout(); fig.savefig(output_path,dpi=160); plt.close(fig)
    return output_path

def summary_text(records, anchor=None):
    dates,summ,current=weekly_summary(records,anchor)
    lines=["HEALTHY HABIT TRACKER — WEEKLY SUMMARY",f"Week: {dates[0]} to {dates[-1]}",""]
    for habit,s in summ.items():
        lines += [habit,f"  Total: {s['total']:.2f} {s['unit']}",f"  Daily average: {s['average']:.2f} {s['unit']}",f"  Weekly goal: {s['goal']:.2f} {s['unit']}",f"  Goal progress: {s['percentage']:.1f}%",""]
    lines.append(f"Entries this week: {len(current)}")
    return "\\n".join(lines)
