# Log Analyzer CLI

A command-line tool for parsing and analyzing log files — built to simulate 
real support engineering workflows: filtering errors, spotting peak failure 
hours, and exporting diagnostic reports to CSV.

## Features
	- Read and parse log files
	- Filter records by log level (ERROR, WARNING, INFO, DEBUG)
	- Filter records by date
	- Filter records by keyword in message
	- Generate message statistics
	- Find the top N most frequent ERROR messages
	- Display error distribution by hour
	- Export results to CS
	- Display result in txt or json format

## Requirements
	- Python 3.10 or higher

	The project uses only Python standard library modules:
		- argparse
		- csv
		- collections
		- datetime
		- os
		- sys
		- logging
		- json

## Usage

```bash
# Analyze the entire log file
python analyzer.py --file log_data/app.log 

# Analyze logs for a specific date
python analyzer.py --file log_data/app.log --date 2026-05-20   

# Filter by log level
python analyzer.py --file log_data/app.log --level DEBUG  

# Show top 5 errors instead of top 3
python analyzer.py --file log_data/app.log --n 5

# Keyword Search
python analyzer.py --file log_data/app.log --keyword "timeout"

# JSON output
python analyzer.py --file log_data/app.log --format json

# Save CSV in another place
python analyzer.py --file log_data/app.log --output results/my_report.csv

# Filter combination
python analyzer.py --file log_data/app.log --level ERROR --keyword "timeout" --date 2026-05-20 --format json

```

## Output
```
WARNING: Skipped 2 malformed lines
=== Log Report ===
Total lines: 200
ERROR: 13
WARNING: 32
INFO: 104
DEBUG: 51

Top 3 ERROR messages:
1. Permission denied (x4)
2. SSL handshake failed (x2)
3. Disk full (x2)

=== Hourly Error Distribution ===
00:00  ██ 2
01:00  █ 1
02:00  █ 1
..
INFO: CSV saved: reports/report.csv
```

## Project structure
log-analyzer/
├── analyzer.py
├── generate_logs.py
├── log_data/
│   └── app.log
├── reports/
│   └── report.csv
|── README_EN.md
└── README_RU.md