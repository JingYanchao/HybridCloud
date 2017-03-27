import time
def print_log(str):
    logfile=''
    # logfile+=time.time()
    logfile+=":"
    logfile+="[info] "
    logfile+=str
    print logfile