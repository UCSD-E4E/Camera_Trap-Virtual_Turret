# CALLBACKS
#
# file: managertest.py
# date: 26 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#
# simple example of how callbacks work

import threading
from threading import Thread



class Manager(object):
    def __init__(self):
        self.name = "managerThread"
        
    def new_thread(self):
        return SubThread(parent=self)

    def callback(self, fromthread, data):
        print self.name +  ": " + fromthread.name, data
    def callback2(self, x):
        print self.name + ": " + str(x)

class SubThread(Thread):
    def on_thread_finished(self, thread, data):
        pass

    def __init__(self, parent=None):
        threading.Thread.__init__(self)
        self.parent = parent
        self.setName("subthread")

    def run(self):
        print self.name + ": hi"
        self.parent.callback(self, 42)
        self.parent.callback2(8)

mgr    = Manager()
thread = mgr.new_thread()
thread.run()