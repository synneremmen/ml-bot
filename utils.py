import ast
import json
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

def get_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist.")
    with open(filename, "r") as file:
        csvdata = csv.reader(file)
        data = [row for row in csvdata]
        cols_name = data[0] # first row should be the column names
        rows = data[1:]
        return {title: d for title, d in zip(cols_name, zip(*rows))}
    
def get_map_id_name():
    try:
        env_map = os.getenv("MAP_ID_NAME", "{}") # should be on the form '{"<@123456789>": "name"}'
        MAP_ID_NAME = json.loads(env_map)
    except Exception:
        try: 
            MAP_ID_NAME = ast.literal_eval(env_map)
        except Exception:
            MAP_ID_NAME = {}
    return MAP_ID_NAME

def get_tournament_mentions(tournament_list, MAX_TOURNAMENT_PARTICIPANTS, filename="logs/konge.csv"):
    num_participants = len(tournament_list)
    ratings = get_data(filename)

    if ratings: # sort list by number of wins to have leagues
        column_values = list(ratings.values())
        get_names = list(column_values[1]) # WEAK: given that the second column contains the names
        get_counts = [get_names.count(name) for name in get_names]

        def get_participant_count(participant):
            try: 
                index = get_names.index(participant)
                return get_counts[index]
            except:
                return 0  # participants is not in the ratings
            
        tournament_list = sorted(tournament_list, key=get_participant_count, reverse=True)
    
    if num_participants > MAX_TOURNAMENT_PARTICIPANTS: # split into groups if more than max participants
        num_groups = num_participants // MAX_TOURNAMENT_PARTICIPANTS + (1 if num_participants % MAX_TOURNAMENT_PARTICIPANTS > 0 else 0)
        group_size = num_participants // num_groups + (1 if num_participants % num_groups > 0 else 0)
        first_group = tournament_list[:group_size]
        mentions = ', '.join([participant.mention for participant in first_group])
    else: # all participants in one group
        group_size = num_participants
        mentions = ', '.join([participant.mention for participant in tournament_list])
    
    return mentions, tournament_list[group_size:]