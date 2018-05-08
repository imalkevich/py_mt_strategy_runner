""" run task """
import sys
from subprocess import Popen
import time

def _done(p):
    return p.poll() is not None
def _success(p):
    return p.returncode == 0
def _fail():
    print("Process failed...")
    sys.exit(1)

task_running = dict()

def exec_commands(cmds, degree_of_parallelism):
    ''' Exec commands in parallel in multiple process '''
    if not cmds: return # empty list

    max_task = degree_of_parallelism
    processes = []

    def check_running_processes():
        """ check if processes are running """
        for p in processes:
            if _done(p):
                mt_worker = p.args.split('"')[1]
                del task_running[mt_worker]

                if _success(p):
                    processes.remove(p)
                else:
                    _fail()

    while True:
        while cmds and len(processes) < max_task:
            task = cmds.pop()

            # get MT4 path
            mt_worker = task.split('"')[1]
            if mt_worker in task_running:
                while True:
                    #print("Waiting for worker - {} ...".format(mt_worker))
                    time.sleep(1)
                    check_running_processes()
                    if mt_worker not in task_running:
                        break

            task_running[mt_worker] = 1
            processes.append(Popen(task))

        check_running_processes()

        if not processes and not cmds:
            break
        else:
            time.sleep(1)
