
from subprocess import call
from datetime import datetime
from datetime import time

def job_function():
    call(["python", "Parser_test.py"])

    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    time.sleep(3600)

