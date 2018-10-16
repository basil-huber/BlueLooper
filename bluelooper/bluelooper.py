from .bluepedal import BluePedal
from .sooperlooper import LooperOSC
from time import sleep


def set_pedal_leds(pedal, looper_state):
    if looper_state == LooperOSC.State.PLAYING:
        pedal.setLEDState(0, BluePedal.LED_ON)
    elif looper_state in [LooperOSC.State.RECORDING, LooperOSC.State.OVERDUBBING, LooperOSC.State.MULTIPLYING]:
        pedal.setLEDState(0, BluePedal.LED_BLINKING)
    else:
        pedal.setLEDState(0, BluePedal.LED_OFF)

def button_callback(looper, pedal, button_id, button_state):
    looper_state = looper.get_state()
    if button_id == 0:
        if button_state == BluePedal.RELEASED:
            if looper_state in [LooperOSC.State.MUTED_OFF, LooperOSC.State.OFF, LooperOSC.State.UNKNOWN, LooperOSC.State.RECORDING]:
                looper.record()
            else:
                looper.multiply()
        elif button_state == BluePedal.RELEASED_LONG:
            looper.undo()
    elif button_id == 1:
        if button_state == BluePedal.RELEASED:
            looper.mute()
        elif button_state == BluePedal.RELEASED_LONG:
            looper.reset()



def main():
    ###########################
    #     Set up looper       #
    ###########################
    looper = LooperOSC()
    looper.connect()
    looper.register_state_update() # registration does currently not work

    ###########################
    #   Set up blue_pedal     #
    ###########################
    pedal = BluePedal("BLUE")
    pedal.connect()

    ###########################
    # Connect pedal to looper #
    ###########################
    pedal.button_callback = lambda button_id, button_state: button_callback(looper, pedal, button_id,  button_state)
    looper.set_state_callback(lambda looper_state: set_pedal_leds(pedal, looper_state))
    set_pedal_leds(pedal, looper.get_state())

    ###########################
    #       Main loop         #
    ###########################
    while True:
        pedal.waitForNotifications()

