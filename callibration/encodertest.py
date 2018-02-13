
import usb.core
import time

class encodertest:

	def __init__(self):
		# self.READ_SW1 = 3
		self.ENC_READ_REG_AND_TIME = 6
		self.dev = usb.core.find(idVendor = 0x6666, idProduct = 0x0003)
		if self.dev is None:
			raise ValueError('no USB device found matching idVendor = 0x6666 and idProduct = 0x0003')
		self.dev.set_configuration()

# AS5048A Register Map
		self.ENC_NOP = 0x0000
		self.ENC_CLEAR_ERROR_FLAG = 0x0001
		self.ENC_PROGRAMMING_CTRL = 0x0003
		self.ENC_OTP_ZERO_POS_HI = 0x0016
		self.ENC_OTP_ZERO_POS_LO = 0x0017
		self.ENC_DIAG_AND_AUTO_GAIN_CTRL = 0x3FFD
		self.ENC_MAGNITUDE = 0x3FFE
		self.ENC_ANGLE_AFTER_ZERO_POS_ADDER = 0x3FFF

	def close(self):
		self.dev = None


	def read_sw1(self):
		try:
			ret = self.dev.ctrl_transfer(0xC0, self.READ_SW1, 0, 0, 1)
		except usb.core.USBError:
			print "Could not send READ_SW1 vendor request."
		else:
			return int(ret[0])


	def get_angle_and_time(self):
		try:
			ret = self.dev.ctrl_transfer(0xC0, self.ENC_READ_REG_AND_TIME, 0x3FFF, 0, 6)
		except usb.core.USBError:
			print "Could not send ENC_READ_REG vendor request."
		else:
			return [(int(ret[0]) +  (int(ret[1])*256))& 0x3FFF, (int(ret[2]) + (int(ret[3])<< 8) +  (int(ret[4])<< 16) + (int(ret[5])<<24))]


