# Project 1: Log Analyze CLI

I created a simple Python command-line tool that reads log files and creates a clean summary. 
It helps system administrators see errors, warnings, and system health quickly.

## What it Does (Features)
- Reads log files line-by-line.
- Automatically handles both **Plain Text** and **JSON** log styles.
- Counts how many INFO, WARNING, and ERROR lines are in the file.
- Finds the most common error message.
- Allows users to filter data by log level or time window.
- Can export the final results to a clean CSV spreadsheet.

## How to Run the Script
Run the following in the terminal:
python analyzer.py app.log --level ERROR --export summary.csv