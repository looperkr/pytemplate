from datetime import datetime as dt
import calendar
import os

def create_dir(output_path):
    now = dt.now()
    year = str(now.year)
    month = calendar.month_abbr[now.month]
    day = str(now.day)

    output_dirname = output_path + "plot_" + year + month + day

    #check if directory for today's date exists; if not, create directory
    if not os.path.exists(output_dirname):
        os.mkdir(output_dirname)
        print("Created directory ",output_dirname)
        
