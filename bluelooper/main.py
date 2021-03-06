from bluelooper.bluepedal import BluePedal
from bluelooper.sooperlooper import Looper
from threading import Event


def set_pedal_leds(pedal, looper_state):
    if looper_state == Looper.State.PLAYING:
        pedal.setLEDState(0, BluePedal.LED_ON)
    elif looper_state in [Looper.State.RECORDING, Looper.State.OVERDUBBING, Looper.State.MULTIPLYING]:
        pedal.setLEDState(0, BluePedal.LED_BLINKING)
    else:
        pedal.setLEDState(0, BluePedal.LED_OFF)

def button_callback(looper, pedal, button_id, button_state):
    looper_state = looper.get_state()
    if button_id == 0:
        if button_state == BluePedal.RELEASED:
            if looper_state in [Looper.State.MUTED_OFF, Looper.State.OFF, Looper.State.UNKNOWN, Looper.State.RECORDING]:
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

def set_event(event):
    """Callback for looper connected: set event"""
    event.set()

def main():
    looper_connected_event = Event()

    def looper_connected():
        looper_connected_event.set()
        print('Looper connected!!!!!!!!!!!!!!')

    pedal_connected_event = Event()

    def pedal_connected():
        print('pedal connected!!!!!!!!!!!!!!')
        set_event(pedal_connected_event)
        print('!!!!!!!!!!!!!!pedal connected')

    ###########################
    # Set up looper and pedal #
    ###########################
    with Looper(on_connected=looper_connected) as looper,\
            BluePedal("BLUE", on_connected=pedal_connected) as pedal:
        #######################################
        # wait for looper and pedal connected #
        #######################################
        looper_connected_event.wait()
        pedal_connected_event.wait()

        ###########################
        # Connect pedal to looper #
        ###########################
        pedal.button_callback = lambda button_id, button_state: button_callback(looper, pedal, button_id,  button_state)
        looper.set_state_callback(lambda looper_state: set_pedal_leds(pedal, looper_state))
        set_pedal_leds(pedal, looper.get_state())

        ###########################
        #       Main loop         #
        ###########################
        while looper.sooperlooper.is_alive():
            #pedal.waitForNotifications()
            import  time
            time.sleep(1)


if __name__ == '__main__':
    main()

