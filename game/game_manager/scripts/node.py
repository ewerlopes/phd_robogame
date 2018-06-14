#!/usr/bin/env python

import rospy, copy
from std_msgs.msg import Bool
from sensor_msgs.msg import Joy
from game_manager.msg import ButtonState, TowerState, TiltSensor, Towers, ChangeLEDs
from game_manager.srv import SetLEDs

class Tower():
	NUM_CHARGE_LEDS = 4
	ALLOWED_STATUSES = [TowerState.TYPE_TOWER_CAPTURED,
						TowerState.TYPE_TOWER_HAS_FALLEN,
						TowerState.TYPE_TOWER_OFFLINE,
						TowerState.TYPE_TOWER_ONLINE]
	
	LED_COLOR = {'red':(1,0), 'green': (0,1), 'blank': (0,0)}


	def __init__(self, id):
		# the tower id
		self._id = id
		# the current tower state (see Tower.ALLOWED_STATUSES static variable)
		self._status = TowerState.TYPE_TOWER_OFFLINE
		# the current charge led statuses
		self._leds = [0 for i in range(Tower.NUM_CHARGE_LEDS)]
		# the current number of button presses 
		self._num_presses = 0
		# the ration between button presses and leds turned on
		self._press_accuracy = 0.0
		# the current color for the tower status led
		self._status_led_color = Tower.LED_COLOR['red']
	
	@property
	def id(self):
		return self._id

	@property
	def status(self):
		return self._status
	
	@status.setter
	def status(self, value):
		if value in Tower.ALLOWED_STATUSES:
			self._status = value
	
	@property
	def leds(self):
		return self._leds

	@property
	def status_led_color(self):
		return self._status_led_color

	@status_led_color.setter
	def status_led_color(self, value):
		if value in Tower.LED_COLOR.values():
			self._status_led_color = value
	
	@property
	def num_presses(self):
		return self._num_presses

	def num_presses_add_one(self):
		""" Increase number of _num_presses by one.
		To be called each time the button is pressed."""
		self._num_presses +=1
	
	def update_led(self, id_led, state):
		""" 
		Update led state
		Params
			id_led (int, range: 1-NUM_CHARGE_LEDS):	the charge led number
			state (bool):	the new state for the led
			"""
		if self.feedback_timer is not None:
			self.stop_feedback_timer()
		self._leds[id_led] = state

	def num_ON_leds(self):
		""" Returns the number of charge leds turned ON by the player"""
		return sum(self._leds)

	def get_data_as_ros_msg(self):
		"""Return the data as ROS TowerState msg"""
		data = TowerState()
		data.id = self.id
		data.status = self.status
		data.leds = self.leds
		data.bt_presses = self.num_presses
		data.press_accuracy = self.press_accuracy
		return data
	
	@property
	def press_accuracy(self):
		"""Calculates the ratio between button presses and the number of leds captured"""
		return self.num_ON_leds() / float(self._num_presses) if self._num_presses != 0 else 0.0
		

	def reset_data(self):
		"""Reset data to init values"""
		self._status = TowerState.TYPE_TOWER_OFFLINE
		self._leds = [0 for i in range(Tower.NUM_CHARGE_LEDS)]
		self._num_presses = 0
		self._status_led_color = Tower.LED_COLOR['red']
		self._press_accuracy = 0.0

	def __str__(self):
		return "TowerStatus: {}, ChargLEDS:{}, StatusLED:{}, NumPresses: {}".format(self._status, self._leds, self._status_led_color, self._num_presses)


class GameManagerNode:
	
	def __init__(self):
		# init node
		rospy.init_node('game_manager')
		
		self.BT_PRESS_THD = rospy.get_param("/charging_time")
		self.CHAR_LED_PER_TW = rospy.get_param("/num_charge_leds_per_tower")
		self.NUM_TOWERS = rospy.get_param("/num_towers")
		self.FEEDBACK_DURATION =  rospy.get_param("/led_feedback_duration")

		# setup subscriber 
		rospy.Subscriber('/joy', Joy, self.joy_callback)
		rospy.Subscriber(rospy.get_param("/button_topic_name"), ButtonState,  self.tower_bt_callback)
		rospy.Subscriber(rospy.get_param("/tilt_sensor_topic_name"), TiltSensor,  self.tower_tilt_sensor_callback)
		
		# setting towers
		self.towers = dict((int(i),0) for i in range(1,self.NUM_TOWERS+1))
		for id in range(1,self.NUM_TOWERS+1):
			self.towers[int(id)] = Tower(int(id))


		# Setup publishers
		self.pub_game_on = rospy.Publisher('game_manager/isGameON', Bool, queue_size=1)
		self.pub_tws_state = rospy.Publisher('game_manager/towers/State', Towers, queue_size=10)
		self.pub_led = rospy.Publisher('game_manager/towers/ChangeLEDs', ChangeLEDs, queue_size=10)
		
		# ros rate
		self.rate = rospy.Rate(10) # 10hz

		# 
		self.feedback_timer = None
		self.feedback_status = False

		self.trying_reset = False

		self.bt_msg_on_process   = None

		self.feedback_timer = (None,None)
		self.feedback_state = 0
		self.reset_game()


	def start_feedback_timer(self, tw_id):
		"""Starts a timer for blinking the next led to be ON. This gives player a feedback
		when pressing the button."""
		self.feedback_timer = (tw_id,rospy.Timer(self.FEEDBACK_DURATION,
										  self._feedback_callback))
	
	def stop_feedback_timer(self):
		"""Stops a timer for blinking feedback"""
		self.feedback_timer[1].shutdown()
		self.feedback_timer = (None,None)

	def _feedback_callback(self, event):
		"""Feedback callback for the led"""
		tw_id = self.feedback_timer[0]
		msg = ChangeLEDs()
		msg.header.stamp = rospy.Time.now()
		msg.id = tw_id
		current_led_state = self.towers[tw_id].leds[:3]
		current_led_state[self.towers[tw_id].num_ON_leds()] = not feedback_state 
		msg.charge_leds = current_led_state
		msg.status_led_color = self.towers[tw_id].status_led_color
		self.pub_led.publish(msg)
		rospy.logwarn("Feedback LED state published!")
		

	def tower_bt_callback(self, msg):
		"""Tower button callback"""

		rospy.loginfo("Button state from tower #{} is {}!".format(msg.id,msg.value))

		if self.towers[msg.id].status == TowerState.TYPE_TOWER_CAPTURED or \
			self.towers[msg.id].status == TowerState.TYPE_TOWER_HAS_FALLEN:
			return

		if msg.value:
			self.bt_msg_on_process = msg
			self.towers[msg.id].num_presses_add_one()    # add press counter for the corresponding tower
			self.start_feedback_timer(msg.id)

		elif msg.value==False and self.bt_msg_on_process is not None:
			self.stop_feedback_timer()
			time_diff = msg.header.stamp.to_sec() - self.bt_msg_on_process.header.stamp.to_sec()
			if time_diff < 0: rospy.logerr("Time diff bettween pressing and unpressing button cannot be negative!")
			if (time_diff / self.BT_PRESS_THD) >= 1:
				self.update_tw_led(self.bt_msg_on_process.id)
			else:
				rospy.loginfo("Time elapsed from last led: {:.2f}".format(time_diff))
			self.bt_msg_on_process = None

	def tower_tilt_sensor_callback(self, msg):
		"""Tilt sensor callback"""
		self.towers[msg.id].status = TowerState.TYPE_TOWER_HAS_FALLEN if msg.value else TowerState.TYPE_TOWER_ONLINE
	
	def checkCapture(self, tw_id):
		"""
		Checks wether player has captured the tower
		Params
			tw_id (int) :	tower id
		Return
			None
		"""
		return  self.towers[tw_id].num_ON_leds() == self.CHAR_LED_PER_TW


	def update_tw_led(self, tower_number):
		old_num_ON = self.towers[tower_number].num_ON_leds()
		self.towers[tower_number].update_led(old_num_ON, 1)

		if self.checkCapture(tower_number):
			self.towers[tower_number].status = TowerState.TYPE_TOWER_CAPTURED
			self.towers[tower_number].status_led_color = Tower.LED_COLOR['green']
			self.bt_msg_on_process = None
			self.stop_feedback_timer()

		self.publish_LED_update(tower_number)
		rospy.logwarn("#leds in tower{}: {}".format(tower_number,self.towers[tower_number].leds))
		rospy.logwarn("Bt_presses in tower{}: {}".format(tower_number,self.towers[tower_number].num_presses))


	def joy_callback(self, msg):
		"""
		Reads the joy message and checks whether start button was pressed.
		"""
		if msg.buttons[5] and msg.buttons[9] == 1 and not trying_reset:
			self.trying_reset = not trying_reset
			rospy.loginfo("Trying to reset towers AND start game..")
			sucess = reset_game()
			msg = Bool()
			msg.data = self.started
			self.pub_game_on.publish(msg)

	def reset_game(self):
		"""Reset game by reseting tower data"""
		for tw in self.towers.keys():
			self.towers[tw].reset_data()
			rospy.loginfo("Tower {} was reset! New State:\n{}".format(tw,self.towers[tw]))
			for i in range(5):		# make sure the towers listen to the call
				self.publish_LED_update(tw)
				self.rate.sleep()

	def count_time(self):
		"""Counts second past button presses"""
		if self.bt_msg_on_process is not None:
			now = rospy.Time.now()
			time_diff = now.to_sec() - self.bt_msg_on_process.header.stamp.to_sec()
			if time_diff < 0: rospy.logerr("count_time(): Time diff bettween pressing and unpressing button cannot be negative!")
			if (time_diff / self.BT_PRESS_THD) >= 1 and self.towers[self.bt_msg_on_process.id].status == TowerState.TYPE_TOWER_ONLINE:
				self.update_tw_led(self.bt_msg_on_process.id)
				if self.bt_msg_on_process is not None:
					self.bt_msg_on_process.header.stamp = now
				

	def publish_LED_update(self, tw_id):
		"""Publish the new led state to LEDs"""
		msg = ChangeLEDs()
		msg.header.stamp = rospy.Time.now()
		msg.id = tw_id
		msg.charge_leds = self.towers[tw_id].leds[:3]
		msg.status_led_color = self.towers[tw_id].status_led_color
		self.pub_led.publish(msg)
		rospy.logwarn("New LED state published!")
		return True

	def publish_state_of_towers(self):
		"""Publish state of towers"""
		msg = Towers()
		msg.header.stamp = rospy.Time.now()
		for i in self.towers.keys():
			setattr(msg, "tw"+str(i), self.towers[i].get_data_as_ros_msg())
		self.pub_tws_state.publish(msg)


	def run(self):
		"""main loop"""
		while not rospy.is_shutdown():
			rospy.loginfo_throttle(3,"Subscribers to ChangeLEDs: {}".format(self.pub_led.get_num_connections()))
			self.count_time()
			self.publish_state_of_towers()
			self.rate.sleep()
			

if __name__ == '__main__':
	node = GameManagerNode()
	node.run()

