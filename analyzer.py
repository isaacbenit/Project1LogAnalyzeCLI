import json
import sys

# =====================================================================
# STEP 1: GET THE COMMAND LINE INPUTS
# =====================================================================

file_path = sys.argv[1]  

filter_level = None
filter_from = None
filter_to = None
export_file = None

for i in range(len(sys.argv)):
    if sys.argv[i] == "--level":
        filter_level = sys.argv[i + 1] 
    elif sys.argv[i] == "--from":
        filter_from = sys.argv[i + 1]
    elif sys.argv[i] == "--to":
        filter_to = sys.argv[i + 1]
    elif sys.argv[i] == "--export":
        export_file = sys.argv[i + 1]

# =====================================================================
# STEP 2: SET UP COUNTERS
# =====================================================================
total_logs = 0
errors = 0
warnings = 0
info = 0

error_messages = {}     
failure_timestamps = [] 

# =====================================================================
# STEP 3: READ THE FILE AND PROCESS LINE BY LINE
# =====================================================================
with open(file_path, "r") as file:
    for line in file:
        line = line.strip()  
        if not line:
            continue         

    
        timestamp = ""
        level = ""
        message = ""

       
        if line.startswith("{"):
            log_data = json.loads(line)
            timestamp = log_data.get("timestamp")
            level = log_data.get("level")
            message = log_data.get("message")
        else:
            parts = line.split(" ", 3) 
            if len(parts) >= 4:
                timestamp = parts[0] + " " + parts[1]
                level = parts[2]
                message = parts[3]
            else:
                continue 

        if filter_level is not None and level != filter_level:
            continue 
            
        if filter_from is not None and timestamp < filter_from:
            continue 
            
        if filter_to is not None and timestamp > filter_to:
            continue 

        total_logs += 1

        if level == "ERROR":
            errors += 1
            failure_timestamps.append(timestamp)
            
            if message not in error_messages:
                error_messages[message] = 1
            else:
                error_messages[message] += 1
                
        elif level == "WARNING":
            warnings += 1
        elif level == "INFO":
            info += 1

# =====================================================================
# STEP 4: CALCULATE FINAL RESULTS
# =====================================================================
most_common_error = "None"
if error_messages:
    most_common_error = max(error_messages, key=error_messages.get)

# =====================================================================
# STEP 5: PRINT SUMMARY TO THE TERMINAL
# =====================================================================
print(f"Total logs:           {total_logs}")
print(f"Errors:                 {errors}")
print(f"Warnings:              {warnings}")
print(f"Info:                 {info}")
print(f'Most frequent error:  "{most_common_error}"')

just_times = []
for t in failure_timestamps:
    parts = t.split(" ")
    just_times.append(parts[1]) 
print(f"Failure timestamps:   {', '.join(just_times)}")

# =====================================================================
# STEP 6: EXPORT TO CSV (IF REQUESTED)
# =====================================================================
if export_file is not None:
    with open(export_file, "w") as f:
        f.write("metric,value\n")
        f.write(f"total_logs,{total_logs}\n")
        f.write(f"errors,{errors}\n")
        f.write(f"warnings,{warnings}\n")
        f.write(f"info,{info}\n")
        f.write(f"most_common_error,{most_common_error}\n")
    print(f"\nExported to {export_file} successfully!")