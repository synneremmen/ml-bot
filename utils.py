import os
import csv
import time

def initialize_log_file(filename):
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "duration"])

def log_event(start, end, filename):
    duration = int(end - start)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), duration])
    return duration // 60  # return duration in minutes