import argparse
from storage import ensure_files
from cli import cli
from gui import launch_gui

def main():
    parser=argparse.ArgumentParser(description="Healthy Habit Tracker")
    parser.add_argument("--cli",action="store_true",help="Launch terminal interface")
    args=parser.parse_args()
    ensure_files()
    if args.cli: cli()
    else: launch_gui()
if __name__=="__main__":main()
