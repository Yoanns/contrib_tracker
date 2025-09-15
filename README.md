## Sibling Contributions Tracker
A simple [Streamlit](https://streamlit.io/) app to track family members’ contributions, demonstrating Python basics with dataclasses, lists/dicts, CSV file I/O, and [Matplotlib](https://matplotlib.org/) charts.

### Features
- Member management: add members with an optional monthly amount, prevent duplicates, and list current members.
- Contribution tracking: record date and amount, and view full or per‑member history.
- Reporting: compute totals per member and visualize them with a basic Matplotlib bar chart.
- Persistence: store members and contributions as CSV files in a local data/ folder using the standard csv module.
- KISS design: small codebase, readable functions, and beginner‑level constructs only.

### Tech stack
- Python 3, dataclasses for simple models (Member, Contribution).
- Streamlit for a beginner‑friendly GUI in the browser.
- Matplotlib (pyplot) for basic bar charts.
- CSV I/O with the standard csv module and basic os path handling.

### Project structure
```
- project_root/
  - app.py
  - models.py
  - storage.py
  - data/
    - members.csv
    - contributions.csv
  - .gitignore
  - README.md
```

### Installation
- Create an environment: `python3 -m venv venv` where the second `venv` is the environment name
- Activate the environment: `source venv/bin/activate`
- install dependencies with pip, e.g., `pip install streamlit matplotlib`.
- Ensure Python 3 is available on the system PATH.

### Running the app
- From the project directory, run: `streamlit run app.py`.
- A local server starts and opens the app in a browser tab automatically.

### Usage
- Members tab: add a member name and optional monthly amount, then review the members table.
- Contributions tab: select a member, enter amount and date, record the contribution, and review the contributions table.
- Reports tab: view per‑member totals in a table and a Matplotlib bar chart for a quick overview.

### Data and persistence
- Data is saved to CSV files in `data/` (members.csv and contributions.csv) with headers for readability.
- Files are created automatically if missing when the app first saves data.

### Design notes
- OOP: dataclasses define simple data models, and Tracker encapsulates member/contribution operations using lists/dicts and loops.
- CSV I/O: csv.DictReader/DictWriter and header rows keep file handling clear and robust.
- Paths: `data_dir` uses `os` to resolve a local `data/` folder consistent with simple setups.
- Visualization: Matplotlib pyplot is used for a basic bar chart with titles, labels, and a grid.

### Limitations and next steps
- User logins
- Filtering by date ranges and CSV import/export from the UI could be added later if needed.
- Optional enhancements include validation messages and additional charts while keeping the app simple.