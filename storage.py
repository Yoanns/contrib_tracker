import csv
import os
import sys
from typing import List, Dict, Tuple
from models import Member, Contribution, Tracker

DATA_DIR_NAME = "data"
MEMBERS_FILE = "members.csv"
CONTRIBS_FILE = "contributions.csv"

def project_root() -> str:
    """
    Resolve the project root directory using os.path and sys for demonstration.
    Falls back to current working directory if __file__ is unavailable.
    """
    # Show sys.path usage to reflect class material (read-only demonstration)
    _ = sys.path  # Not printed; available for debugging if needed
    try:
        here = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        here = os.getcwd()
    return here

def data_dir() -> str:
    """
    Ensure and return the absolute path to the data directory.
    """
    root = project_root()
    d = os.path.join(root, DATA_DIR_NAME)
    os.makedirs(d, exist_ok=True)
    return d

def members_path() -> str:
    """
    Absolute path to members.csv.
    """
    return os.path.join(data_dir(), MEMBERS_FILE)

def contributions_path() -> str:
    """
    Absolute path to contributions.csv.
    """
    return os.path.join(data_dir(), CONTRIBS_FILE)

def load_tracker() -> Tracker:
    """
    Create a Tracker and populate from CSV files if present.
    """
    t = Tracker()
    # Load members
    mpath = members_path()
    if os.path.exists(mpath):
        with open(mpath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", "").strip()
                if not name:
                    continue
                monthly = float(row.get("monthly_amount", "0") or 0)
                t.add_member(name, monthly)
    # Load contributions
    cpath = contributions_path()
    if os.path.exists(cpath):
        with open(cpath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                member = row.get("member", "").strip()
                date_iso = row.get("date", "").strip()
                amount = float(row.get("amount", "0") or 0)
                if member and amount > 0 and date_iso:
                    # Only record if member exists
                    if t.get_member(member):
                        t.record_contribution(member, amount, when=date_iso)
    return t

def save_members(members: List[Member]) -> None:
    """
    Save members to CSV with a header row.
    """
    with open(members_path(), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "monthly_amount"])
        writer.writeheader()
        for m in members:
            writer.writerow({"name": m.name, "monthly_amount": m.monthly_amount})

def save_contributions(contribs: List[Contribution]) -> None:
    """
    Save contributions to CSV with a header row.
    """
    with open(contributions_path(), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["member", "date", "amount"])
        writer.writeheader()
        for c in contribs:
            writer.writerow({"member": c.member, "date": c.date, "amount": c.amount})
