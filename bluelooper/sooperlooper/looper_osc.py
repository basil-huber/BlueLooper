import liblo
import time

class LooperOSC:

    

    def __init__(self, target_ip="localhost", home_ip="localhost", home_port="9952"):
        try:
           self.target = liblo.Address(target_ip,"9951");
           self.home_url = home_ip+":"+home_port
           self.home_server = liblo.Server(home_port)
           self.home_server.add_method("/state", "isf", self.receive_state, self)
           self.home_server.add_method("/ping", None, self.receive_ping, self)
           self.loop_count = 1

           self.ping_received = 0   # used for callback
           self.state = -1
        except liblo.AddressError:
            print("error")

    def wait_for_ready(self):
        # ping looper until it responds
        while True:
            try:
                print("waiting for looper")
                if self.ping():
                    # if we received answer, leave infinite loop
                    break
            except IOError:
                print("Looper not Found")
                time.sleep(1)

    def register_state_update(self):
        liblo.send(self.target, "/sl/-1/register_update", "state", self.home_url, "/state")

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

    def ping(self):
        self.ping_received = 0
        liblo.send(self.target, "/ping", self.home_url, "/ping")
        self.receive()
        return self.ping_received

    def quit(self):
        liblo.send(self.target, "/quit")

    def add_loop(self):
        liblo.send(self.target, "/loop_add",2,50)
        self.loop_count = self.loop_count + 1

    def get_state(self):
        liblo.send(self.target, "/sl/-1/get","state", self.home_url, "/state")
        self.receive()
        return self.state

    def receive_state(self, path, answer):
        self.state = answer[2]
        
    def receive_ping(self, path, answer):
        self.ping_received = 1

    def receive(self):
        return self.home_server.recv(500)

