from .bluepedal import BluePedal
from .sooperlooper import LooperOSC

looper_state = 0

def button_callback(button_id, state):
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
			looper_state = 0;
			print("reset looper")

###########################
#   Set up blue_pedal     #
###########################

pedal = BluePedal("BLUE")
pedal.connect()
pedal.button_callback = button_callback


###########################
#     Set up looper       #
###########################

looper = LooperOSC()
looper.wait_for_ready()
looper.register_state_update()
print("Looper ready")
while True:
	pedal.waitForNotifications()
	#looper.get_state()
	#if looper.receive():
	#	print("received")
	#else:
	#	print("npot received")


