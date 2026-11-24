import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date,datetime,timedelta
from config import APP_NAME,HABITS
from storage import load_records,save_records
from habit_engine import make_record,filter_records,weekly_summary
from analytics import make_chart,summary_text
from reports import export_reports,audit
from importer import import_into_app
import os

BG="#F3F6F8"; NAV="#152B3C"; ACC="#14B8A6"; TEXT="#243746"; MUTED="#718096"; CARD="#FFFFFF"
class HabitApp:
    def __init__(self,root):
        self.root=root; self.root.title(APP_NAME); self.root.geometry("1180x760"); self.root.minsize(980,640)
        self.root.configure(bg=BG); self.records=load_records(); self.page="Dashboard"
        self.setup_style(); self.build_shell(); self.show_page("Dashboard")
    def setup_style(self):
        s=ttk.Style(); s.theme_use("clam")
        s.configure("Treeview",font=("Segoe UI",10),rowheight=32,background="white",fieldbackground="white",foreground=TEXT)
        s.configure("Treeview.Heading",font=("Segoe UI",10,"bold"),background="#E8EEF2",foreground=TEXT)
        s.configure("TButton",font=("Segoe UI",10),padding=(10,7))
        s.configure("Accent.TButton",font=("Segoe UI",10,"bold"),padding=(12,8))
    def build_shell(self):
        self.sidebar=tk.Frame(self.root,bg=NAV,width=220); self.sidebar.pack(side="left",fill="y"); self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar,text="◈  Healthy Habits",bg=NAV,fg="white",font=("Segoe UI",16,"bold")).pack(anchor="w",padx=20,pady=(26,6))
        tk.Label(self.sidebar,text="WEEKLY WELLNESS",bg=NAV,fg="#94A8B8",font=("Segoe UI",9,"bold")).pack(anchor="w",padx=20,pady=(0,22))
        for page in ["Dashboard","Habits","Records","Analytics","Reports","Import CSV"]:
            b=tk.Button(self.sidebar,text="   "+page,command=lambda p=page:self.show_page(p),anchor="w",bg=NAV,fg="#E6EEF4",activebackground="#27445A",activeforeground="white",relief="flat",font=("Segoe UI",11),padx=12,pady=12)
            b.pack(fill="x",padx=10,pady=2)
        tk.Label(self.sidebar,text="Local-first • Private data",bg=NAV,fg="#8DA3B3",font=("Segoe UI",9)).pack(side="bottom",pady=18)
        self.main=tk.Frame(self.root,bg=BG); self.main.pack(side="left",fill="both",expand=True)
    def clear(self):
        for w in self.main.winfo_children():w.destroy()
    def header(self,title,subtitle=""):
        top=tk.Frame(self.main,bg=BG); top.pack(fill="x",padx=28,pady=(22,14))
        tk.Label(top,text=title,font=("Segoe UI",23,"bold"),fg=TEXT,bg=BG).pack(anchor="w")
        if subtitle:tk.Label(top,text=subtitle,font=("Segoe UI",10),fg=MUTED,bg=BG).pack(anchor="w",pady=3)
    def card(self,parent,title,value,sub=""):
        f=tk.Frame(parent,bg=CARD,highlightbackground="#E4EAF0",highlightthickness=1); f.pack(side="left",fill="both",expand=True,padx=6)
        tk.Label(f,text=title,bg=CARD,fg=MUTED,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=16,pady=(15,5))
        tk.Label(f,text=value,bg=CARD,fg=TEXT,font=("Segoe UI",22,"bold")).pack(anchor="w",padx=16)
        tk.Label(f,text=sub,bg=CARD,fg=MUTED,font=("Segoe UI",9)).pack(anchor="w",padx=16,pady=(4,15))
        return f
    def show_page(self,page):
        self.page=page; self.clear()
        if page=="Dashboard": self.dashboard()
        elif page=="Habits": self.habits_page()
        elif page=="Records": self.records_page()
        elif page=="Analytics": self.analytics_page()
        elif page=="Reports": self.reports_page()
        elif page=="Import CSV": self.import_page()
    def dashboard(self):
        self.header("Good day!","Your weekly wellness snapshot • "+date.today().strftime("%A, %d %B %Y"))
        dates,summ,current=weekly_summary(self.records)
        row=tk.Frame(self.main,bg=BG);row.pack(fill="x",padx=22)
        self.card(row,"ENTRIES THIS WEEK",str(len(current)),"Recorded habit sessions")
        self.card(row,"HABITS TRACKED",str(len(set(r["habit"] for r in current))),"Out of 3 habit categories")
        self.card(row,"WEEK"," "+dates[0].strftime("%d %b")+" – "+dates[-1].strftime("%d %b"),"Monday to Sunday")
        panel=tk.Frame(self.main,bg=CARD,highlightbackground="#E4EAF0",highlightthickness=1);panel.pack(fill="x",padx=28,pady=20)
        tk.Label(panel,text="Weekly habit progress",font=("Segoe UI",14,"bold"),bg=CARD,fg=TEXT).pack(anchor="w",padx=18,pady=(14,8))
        for h,s in summ.items():
            line=tk.Frame(panel,bg=CARD);line.pack(fill="x",padx=18,pady=8)
            tk.Label(line,text=h,width=12,anchor="w",bg=CARD,fg=TEXT,font=("Segoe UI",10,"bold")).pack(side="left")
            tk.Label(line,text=f"{s['total']:.1f} / {s['goal']:.1f} {s['unit']}",width=23,anchor="w",bg=CARD,fg=MUTED).pack(side="left")
            bar=ttk.Progressbar(line,maximum=100,value=s["percentage"]);bar.pack(side="left",fill="x",expand=True,padx=8)
            tk.Label(line,text=f"{s['percentage']:.0f}%",width=5,bg=CARD,fg=TEXT).pack(side="left")
        actions=tk.Frame(self.main,bg=BG);actions.pack(fill="x",padx=28)
        ttk.Button(actions,text="+ Add habit entry",command=self.add_dialog).pack(side="left",padx=5)
        ttk.Button(actions,text="View records",command=lambda:self.show_page("Records")).pack(side="left",padx=5)
        ttk.Button(actions,text="Open analytics",command=lambda:self.show_page("Analytics")).pack(side="left",padx=5)
        recent=tk.Frame(self.main,bg=CARD);recent.pack(fill="both",expand=True,padx=28,pady=18)
        tk.Label(recent,text="Recent entries",font=("Segoe UI",14,"bold"),bg=CARD,fg=TEXT).pack(anchor="w",padx=16,pady=12)
        self.table(recent,filter_records(self.records)[:6])
    def table(self,parent,records):
        cols=("date","habit","amount","unit","note")
        tree=ttk.Treeview(parent,columns=cols,show="headings",height=8)
        for c,w in zip(cols,[120,140,90,100,360]):
            tree.heading(c,text=c.title());tree.column(c,width=w,anchor="w")
        tree.pack(fill="both",expand=True,padx=12,pady=(0,12))
        for r in records:tree.insert("", "end",values=(r.get("date"),r.get("habit"),r.get("amount"),r.get("unit"),r.get("note","")))
        return tree
    def habits_page(self):
        self.header("Habits","Track daily habits against your weekly targets.")
        for h,info in HABITS.items():
            f=tk.Frame(self.main,bg=CARD,highlightbackground="#E4EAF0",highlightthickness=1);f.pack(fill="x",padx=30,pady=10)
            tk.Label(f,text=h,font=("Segoe UI",15,"bold"),fg=TEXT,bg=CARD).pack(anchor="w",padx=18,pady=(14,4))
            tk.Label(f,text=f"Daily target: {info['daily_goal']} {info['unit']}   •   Suggested max entry: {info['maximum']} {info['unit']}",font=("Segoe UI",10),fg=MUTED,bg=CARD).pack(anchor="w",padx=18)
            ttk.Button(f,text="Add entry",command=lambda habit=h:self.add_dialog(habit)).pack(anchor="w",padx=18,pady=12)
        ttk.Button(self.main,text="Add custom note to a habit",command=self.add_dialog).pack(anchor="w",padx=30,pady=5)
    def add_dialog(self,preselect=None,edit_record=None):
        win=tk.Toplevel(self.root);win.title("Edit entry" if edit_record else "Add habit entry");win.geometry("420x420");win.configure(bg=BG);win.transient(self.root);win.grab_set()
        tk.Label(win,text="Habit entry",font=("Segoe UI",18,"bold"),bg=BG,fg=TEXT).pack(pady=16)
        frm=tk.Frame(win,bg=CARD);frm.pack(fill="both",expand=True,padx=20,pady=10)
        def field(label):
            tk.Label(frm,text=label,bg=CARD,fg=TEXT,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=18,pady=(10,3))
        field("Date (YYYY-MM-DD)");d=tk.Entry(frm,font=("Segoe UI",11));d.pack(fill="x",padx=18);d.insert(0,edit_record["date"] if edit_record else date.today().isoformat())
        field("Habit");h=ttk.Combobox(frm,values=list(HABITS),state="readonly");h.pack(fill="x",padx=18);h.set(edit_record["habit"] if edit_record else (preselect or "Reading"))
        field("Amount");a=tk.Entry(frm,font=("Segoe UI",11));a.pack(fill="x",padx=18);a.insert(0,str(edit_record["amount"]) if edit_record else "")
        field("Note (optional)");n=tk.Entry(frm,font=("Segoe UI",11));n.pack(fill="x",padx=18);n.insert(0,edit_record.get("note","") if edit_record else "")
        def save():
            try:
                r=make_record(d.get().strip(),h.get(),a.get().strip(),n.get())
                if edit_record:r["id"]=edit_record["id"];self.records=[x for x in self.records if x["id"]!=r["id"]]
                self.records.append(r);save_records(self.records);audit("Added/edited habit entry");win.destroy();self.show_page(self.page)
            except ValueError as e:messagebox.showerror("Validation error",str(e),parent=win)
        ttk.Button(win,text="Save entry",command=save).pack(pady=12)
    def records_page(self):
        self.header("Records","Search and filter your stored habit activity.")
        f=tk.Frame(self.main,bg=BG);f.pack(fill="x",padx=28)
        tk.Label(f,text="Keyword",bg=BG).grid(row=0,column=0,padx=4,pady=4);kw=tk.Entry(f,width=22);kw.grid(row=0,column=1,padx=4)
        tk.Label(f,text="Habit",bg=BG).grid(row=0,column=2,padx=4);h=ttk.Combobox(f,values=["All"]+list(HABITS),width=14,state="readonly");h.set("All");h.grid(row=0,column=3,padx=4)
        tk.Label(f,text="From",bg=BG).grid(row=0,column=4,padx=4);start=tk.Entry(f,width=12);start.grid(row=0,column=5,padx=4)
        tk.Label(f,text="To",bg=BG).grid(row=0,column=6,padx=4);end=tk.Entry(f,width=12);end.grid(row=0,column=7,padx=4)
        area=tk.Frame(self.main,bg=CARD);area.pack(fill="both",expand=True,padx=28,pady=15)
        tree=self.table(area,[])
        def refresh():
            for i in tree.get_children():tree.delete(i)
            for r in filter_records(self.records,kw.get(),"" if h.get()=="All" else h.get(),start.get().strip(),end.get().strip()):
                tree.insert("", "end",values=(r["date"],r["habit"],r["amount"],r["unit"],r.get("note","")),tags=(r["id"],))
        ttk.Button(f,text="Apply filters",command=refresh).grid(row=0,column=8,padx=8)
        ttk.Button(f,text="Clear",command=lambda:(kw.delete(0,"end"),h.set("All"),start.delete(0,"end"),end.delete(0,"end"),refresh())).grid(row=0,column=9,padx=4)
        row=tk.Frame(self.main,bg=BG);row.pack(fill="x",padx=28)
        ttk.Button(row,text="Add record",command=self.add_dialog).pack(side="left",padx=4)
        def selected_id():
            sel=tree.selection()
            if not sel:return None
            vals=tree.item(sel[0],"values");return next((r for r in self.records if r["date"]==vals[0] and r["habit"]==vals[1] and str(r["amount"])==str(vals[2]) and r.get("note","")==vals[4]),None)
        def edit():
            r=selected_id()
            if r:self.add_dialog(edit_record=r)
            else:messagebox.showinfo("Select entry","Select a row first.")
        def delete():
            r=selected_id()
            if r and messagebox.askyesno("Delete","Delete selected record?"):
                self.records.remove(r);save_records(self.records);audit("Deleted habit entry");refresh()
        ttk.Button(row,text="Edit selected",command=edit).pack(side="left",padx=4);ttk.Button(row,text="Delete selected",command=delete).pack(side="left",padx=4)
        refresh()
    def analytics_page(self):
        self.header("Analytics","Weekly totals, goal progress and visual activity trends.")
        tk.Label(self.main,text=summary_text(self.records),font=("Consolas",11),bg=BG,fg=TEXT,justify="left").pack(anchor="w",padx=35,pady=10)
        p=make_chart(self.records)
        if p:
            try:
                from PIL import Image,ImageTk
                im=Image.open(p);im.thumbnail((850,420));self.chart_img=ImageTk.PhotoImage(im)
                tk.Label(self.main,image=self.chart_img,bg=BG).pack(padx=20,pady=8)
            except ImportError:tk.Label(self.main,text=f"Chart saved at {p}. Install Pillow to display it in-app.",bg=BG,fg=MUTED).pack()
        else:tk.Label(self.main,text="Matplotlib is not installed. Install requirements to enable chart plotting.",bg=BG,fg=MUTED).pack()
        ttk.Button(self.main,text="Export chart",command=lambda:messagebox.showinfo("Chart",f"Saved at {p}" if p else "Matplotlib unavailable")).pack(pady=10)
    def reports_page(self):
        self.header("Reports","Export summaries and records for external review.")
        ttk.Button(self.main,text="Generate Markdown, text and CSV reports",command=self.export_now).pack(anchor="w",padx=30,pady=10)
        tk.Label(self.main,text="Reports are saved in the local reports/ folder.",bg=BG,fg=MUTED).pack(anchor="w",padx=30)
    def export_now(self):
        paths=export_reports(self.records);p=make_chart(self.records);messagebox.showinfo("Export complete","Generated:\\n"+"\\n".join(paths)+("\\n"+p if p else ""))
    def import_page(self):
        self.header("Import CSV","Import a legacy dataset and review row-level validation errors.")
        ttk.Button(self.main,text="Choose CSV file",command=self.choose_import).pack(anchor="w",padx=30,pady=10)
        tk.Label(self.main,text="Required columns: date, habit, amount. Optional columns: id, unit, note, created_at.",bg=BG,fg=MUTED).pack(anchor="w",padx=30)
    def choose_import(self):
        path=filedialog.askopenfilename(filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not path:return
        accepted,errors=import_into_app(path,self.records);self.records=load_records()
        messagebox.showinfo("Import results",f"Imported {len(accepted)} records.\\nRejected rows: {len(errors)}\\n\\n"+"\\n".join(errors[:30]))
        self.show_page("Import CSV")
def launch_gui():
    root=tk.Tk();HabitApp(root);root.mainloop()
