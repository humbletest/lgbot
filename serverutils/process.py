import collections
import logging
import threading
import os
import sys
import signal
import platform
import subprocess

VERBOSE = True

class PopenProcess(object):
    def __init__(self,
            command,
            read_line_callback,
            read_error_callback = None,
            proc_args = None,
            ignore_cwd = False,
            **kwargs
            ):

        self.proc_args = proc_args
        self.ignore_cwd = ignore_cwd

        self.read_line_callback = read_line_callback

        self._receiving_thread = threading.Thread(target=self._receiving_thread_target)
        self._receiving_thread.daemon = True

        self._stdin_lock = threading.Lock()

        cwd = os.getcwd()

        popen_args = {            
            "cwd": cwd,
            "stdout": subprocess.PIPE,            
            "stdin": subprocess.PIPE,
            "bufsize": 1,  # Line buffering
            "universal_newlines": True,        
        }

        self._recerror_thread = None
        self.read_error_callback = read_error_callback

        if not ( self.read_error_callback is None ):
            self._recerror_thread = threading.Thread(target=self._recerror_thread_target)
            self._recerror_thread.daemon = True
            popen_args["stderr"] = subprocess.PIPE

        popen_args.update(kwargs)

        cmdpath = os.path.join(cwd, command)
        if self.ignore_cwd:
            cmdpath = command

        if VERBOSE:
            print("popen", cmdpath, self.proc_args, popen_args)
        else:
            print("popen", cmdpath, self.proc_args)

        if self.proc_args is None:
            self.process = subprocess.Popen(cmdpath, **popen_args)
        else:
            self.process = subprocess.Popen([cmdpath] + self.proc_args, **popen_args)

        if VERBOSE:
            print("process opened")

        self._receiving_thread.start()

        if VERBOSE:
            print("receiving thread started")

        if not ( self._recerror_thread is None ):
            self._recerror_thread.start()
            if VERBOSE:
                print("receiving error thread started")

    def _receiving_thread_target(self):
        while True:
            line = self.process.stdout.readline()
            if not line:
                break

            sline = line.rstrip()
            
            self.read_line_callback(sline)

        self.process.stdout.close()
        with self._stdin_lock:
            self.process.stdin.close()

        if self.is_alive():
            self.terminate()
            self.wait_for_return_code()

    def _recerror_thread_target(self):
        while True:
            line = self.process.stderr.readline()
            if not line:
                break

            sline = line.rstrip()
            
            self.read_error_callback(sline)

    def is_alive(self):
        return self.process.poll() is None

    def terminate(self):
        self.process.terminate()

    def kill(self):
        self.process.kill()

    def send_line(self, string):
        if VERBOSE:
            print("sending line",string)
        with self._stdin_lock:
            self.process.stdin.write(string + "\n")
            self.process.stdin.flush()

    def wait_for_return_code(self):
        self.process.wait()
        return self.process.returncode

    def pid(self):
        return self.process.pid

    def __repr__(self):
        return "<PopenProcess at {0} (pid={1})>".format(hex(id(self)), self.pid())
