import liblo
from threading import Event
from enum import Enum
from time import sleep  # TODO remove


class LooperOSC:

    class State(Enum):
        UNKNOWN = -1
        OFF = 0
        WAIT_START = 1
        RECORDING = 2
        WAIT_STOP = 3
        PLAYING = 4
        OVERDUBBING = 5
        MULTIPLYING = 6
        INSERTING = 7
        REPLACING = 8
        DELAY = 9
        MUTED = 10
        SCRATCHING = 11
        ONESHOT = 12
        SUBSTITUTE = 13
        PAUSED = 14
        MUTED_OFF = 20 # undocumented

    def __init__(self, target_ip="localhost", home_ip="localhost", home_port="9952"):
        try:
           self.home_server = liblo.ServerThread(home_port)
           self.target = liblo.Address(target_ip, "9951")
           self.home_url = home_ip+":"+home_port
           self.home_server.add_method("/state", "isf", self.receive_state, self)
           self.home_server.add_method("/ping", None, self.receive_ping, self)
           self.loop_count = 1

           self.state = LooperOSC.State.UNKNOWN
           self.ping_event = Event()
           self.state_event = Event()
        except liblo.AddressError:
            print("error")

    def connect(self, timeout=None):
        print('sooperlooper starting')
        self.home_server.start()
        print('pinignig')
        while True:
            if self.ping(timeout):
                break
        print('connected')
        self.request_state()

    def register_state_update(self):
        liblo.send(self.target, "/sl/-1/register_update", "state", self.home_url, "/state")
        # currently not working!

    def send_sldown(self,command):
        liblo.send(self.target, "/sl/-1/down",command)

    def record(self):
        self.send_sldown("record")

    def pause(self):
        self.send_sldown("pause")

    def overdub(self):
        self.send_sldown("overdub")

    def multiply(self):
        self.send_sldown("multiply")

    def undo(self):
        self.send_sldown("undo")

    def mute(self):
        self.send_sldown("mute")

    def reset(self):
        liblo.send(self.target, "/loop_del",-1)
        self.add_loop()
        self.loop_count = 1

    def set_threshold(self, threshold):
        liblo.send(self.target, "/sl/-1/set", "rec_thresh", threshold)

    def ping(self, timeout=20):
        self.ping_event.clear()
        liblo.send(self.target, "/ping", self.home_url, "/ping")
        return self.ping_event.wait(timeout)

    def quit(self):
        liblo.send(self.target, "/quit")

    def add_loop(self):
        liblo.send(self.target, "/loop_add",2,50)
        self.loop_count = self.loop_count + 1

    def get_state(self):
        return self.state

    def request_state(self, timeout=1):
        self.state_event.clear()
        liblo.send(self.target, "/sl/-1/get","state", self.home_url, "/state")
        self.state_event.wait(timeout)
        return self.state

    def receive_state(self, path, answer):
        try:
            self.state = LooperOSC.State(answer[2])
        except ValueError:
            self.state = LooperOSC.State.UNKNOWN
        self.state_event.set()

    def receive_ping(self, path, answer):
        self.ping_event.set()
