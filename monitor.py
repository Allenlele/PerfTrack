# -*- coding: utf-8-*-
import psutil
import time
import threading

def get_proc_by_name(pname):
    """ get process by name
    
    return the first process if there are more than one
    """
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == pname.lower():
                return proc  # return if found one
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
    return None


class ProcWatcher(threading.Thread):
    def __init__(self, proc, output, interval):
        threading.Thread.__init__(self)
        self.m_proc = proc
        self.thread_stop = False
        self.output = output
        self.interval = interval

    def run(self):
        while not self.thread_stop:
            self.output(self.m_proc.memory_info().rss)
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True  


if '__main__' == __name__:
    def tout(msg):
        print msg
    mem_watcher = ProcWatcher(get_proc_by_name("CHrome"), tout, 1)
    mem_watcher.start()
    time.sleep(10)
    mem_watcher.stop()