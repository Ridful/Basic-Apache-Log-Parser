from os.path import exists
from sys import exit, argv
from datetime import datetime

msgUsage = "Usage: \"python logparse.py [path/to/file] [action]\" \n \
    - [path/to/file]  \t ex: mydir/file.log \n \
    - [action] \t[statistics|error|notice] \n"

validActions = ["statistics", "error", "notice"]

def invalidCommand(userInputArgs):
    """Returns True if provided arguments triggers any unacceptable conditions.\n
    (I.e: returns True if logfile isn't found or if user arg Action/Command doesn't exist)."""
    
    if len(userInputArgs) != 3:
        print(f'Invalid amount of provided arguments.')
        return True

    if not exists(userInputArgs[1]):
        print(f'Unable to locate selected logfile: \"{userInputArgs[1]}\".')
        return True
    
    if isValidAction(userInputArgs[2]): return False
    
    return True
       

def isValidAction(userAction):
    return str(userAction).lower().strip() in validActions
        
def getLogs(logPath):
    """Returns a list of strings from the user selected logfile filename.log."""
    try:
        with open(logPath, "r", encoding="UTF-8") as f:
            logLines = f.read().splitlines() #Assigns each row of logs as an item in list.
            return logLines
    except (OSError) as err:
        print(f'Oops! Exceptions in getLogs whilst doing I/O!\n{err}')
        return 0

def log_generator(logs, runAction):
    """Iterates logs list and parses log_date, err_msg, and log_msg_content from each item list.\n
    On iterations matching user chosen Action; function yields log_date and log_msg_content."""
    for log in logs:
        
        log_date = datetime.strptime(log[1:25], "%a %b %d %H:%M:%S %Y")
        log_err_msg, log_msg_content = log[27::].split(' ', 1)
        
        if log_err_msg == f'[{runAction}]':
            yield F"{log_date} {log_msg_content}"

def runAction(logs, runAction):
    
    """Executes the chosen Action on the selected logs list and returns results"""
    
    if runAction in ["error", "notice"]:
        return list(log_generator(logs, runAction))
    
    elif runAction == "statistics":
        errors = "errors: " + str(len(list(log_generator(logs, "error")))) 
        notices = "notices: " + str(len(list(log_generator(logs, "notice"))))
        return errors, notices

if __name__ == "__main__":
    #Exit if any issues with user input args
    if invalidCommand(argv):
        print(msgUsage)
        exit()
    
    #Gets logs from file as a list of strings
    logs = getLogs(argv[1])
    
    #Executes the chosen arg Action on the logs list
    for i in runAction(logs, argv[2]):
        print(i)
    
    exit(0)
