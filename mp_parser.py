# This script leverages multiple process technique to accelerate LISP/Planet experimental log file.
# To achieve this, we employ process pool and queue functionality, provided by python.
# The script is coded by inspiring from the following link:
# http://stackoverflow.com/questions/13446445/python-multiprocessing-safely-writing-to-a-file

import multiprocessing as mp
import os
from utility.RoundInstanceFactory import *

# we need some predefined variables stored in config/config.py, to know such as where store all log files
from config.config import *



# Although many processes could involve in the treatment of log file, we have only one process responsible for
# writing logfile-related entry(a row in the context of CSV file) into the given CSV file. The advantage of this
# is to avoid the concurrence about the write access to target CSV file.
def listener(q):
    with open(csv_file,'wb') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel',delimiter=';')
        spamwriter.writerow(['Log File Name','Locator Count Coherence','Round Type Set'])
        while 1:
            csv_row = q.get()
            if csv_row == "TERMINATE":
                break
            spamwriter.writerow(csv_row)

# In our process pool, except the one in charge of writing records into CSV file, all rest processes are used
# to treat log file stored in a certain directory. Every time a process processes a log file, it store the retrieved
# information into a QUEUE data structure, which will be served by listener process.
def worker(arg,q):
    '''stupidly simulates long running process'''
    R = RoundInstanceFactory(arg)
    #csv_row = [arg, R.isLocatorCoherent(), R.getRoundTypeSet()]
    csv_row = [arg]
    csv_row.extend(R.basicCheck())
    q.put(csv_row)


def main(traces_log_dir):
    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count()+2)

    #put listener to work first
    watcher = pool.apply_async(listener,(q,))

    #fire off workers
    jobs = []
    for lists in os.listdir(traces_log_dir):
    #Do not forget to verify that the current file to be processed is a real log file
    #Otherwise this program may be collapsed.
        if lists.endswith(".log"):
            lists = os.path.join(traces_log_dir, lists)
            job = pool.apply_async(worker,(lists,q))
            jobs.append(job)

    #collect results from the workers through the pool result queue
    for job in jobs:
        job.get()

    #Now we are done, kill the listener
    q.put("TERMINATE")
    pool.close()


if __name__ == "__main__":
    for key, value in traces_log.items():
        csv_file = csv_file_destDir+'statistic_{0}.csv'.format(key)
        main(traces_log[key])