import threading
import subprocess
import traceback
import shlex
import os
import signal
import resource

class Command(object):
    """
    Enables to run subprocess commands in a different thread with TIMEOUT option.

    Based on jcollado's solution:
    http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933
    """
    command = ''
    output = ''
    process = None
    status = None
    thread = None


    def __init__(self, command):
        if isinstance(command, basestring):
            command = shlex.split(command)
        self.command = command
    
    def setsessionId(self):
        if not os.getsid:
            os.setsid()


    def run(self, timeout=None):
        """ Run a command then return: (status, output, error). """
        
        def target():
            try:
                print self.command
                #os.open("exec ulimit -v 43;",os.O_NONBLOCK)
                self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=self.setsessionId())
                print self.process.pid
                #self.output = self.process.stdout.read()
                self.output, self.error = self.process.communicate()
                self.status = self.process.returncode
            except:
                self.error = traceback.format_exc()
                self.status = -1
        # default stdout and stderr
        # thread
        self.thread = threading.Thread(target=target)
        self.thread.start()
        self.thread.join(timeout)

        if self.thread.is_alive():
            print "inside thread kill"
            print self.process.pid
            #self.process.kill()
            #os.killpg(self.process.pid, signal.SIGTERM) - Strange & Doesn't work
            subprocess.Popen("kill -TERM "+ str(self.process.pid), shell=True) 
            print "process killed"
            self.error = "Your Program reached maxmum timeout of" + str(timeout) + " seconds"
            self.thread.join()
        return self.status, self.error, self.output
