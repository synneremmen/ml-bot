import os
import csv
import time

def initialize_log_file(filename, titles=["timestamp", "duration_seconds"]):
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(titles)

def log_event(information, filename, is_time=True):
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), information])
    if is_time:
        return information // 60 # return duration in minutes
    return information  
