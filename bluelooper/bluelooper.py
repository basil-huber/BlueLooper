from .bluepedal import BluePedal
from .sooperlooper import LooperOSC
from  functools import partial

looper_state = 0


def button_callback(looper, button_id, state):
    global looper_state
    if button_id == 0:
        if state == BluePedal.RELEASED:
            if looper_state == 0:
                print("start record")
                looper.record()
                looper_state = 1
            elif looper_state == 1:
                print("stop record")
                looper.record()
                looper_state = 2
            elif looper_state == 2:
                print("start overdubbing")
                looper.multiply()
                looper_state = 3
            elif looper_state == 3:
                print("stop overdubbing")
                looper.multiply()
                looper_state = 2
        elif state == BluePedal.RELEASED_LONG:
            looper.undo()
            print("undo")
    elif button_id == 1:
        if state == BluePedal.RELEASED:
            print("mute")
            looper.mute()
        elif state == BluePedal.RELEASED_LONG:
            looper.reset()
            looper_state = 0
            print("reset looper")


def main():
    ###########################
    #   Set up blue_pedal     #
    ###########################

    pedal = BluePedal("BLUE")
    pedal.connect()

    ###########################
    #     Set up looper       #
    ###########################
    looper = LooperOSC()
    looper.wait_for_ready()
    looper.register_state_update()
    print("Looper ready")

    ###########################
    # Connect pedal to looper #
    ###########################
    pedal.button_callback = partial(button_callback, looper=looper)

    ###########################
    #       Main loop         #
    ###########################
    while True:
        pedal.waitForNotifications()

