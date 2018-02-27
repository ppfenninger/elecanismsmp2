#
## Copyright (c) 2018, Bradley A. Minch
## All rights reserved.
##Modified by Chloe Grubb Paige Pfenninger 

import Tkinter as tk
import encodertest
import csv

class encodertestgui:

	def __init__(self):
		self.dev = encodertest.encodertest()
		if self.dev.dev >= 0:
			self.update_job = None
			self.root = tk.Tk()
			self.root.title('Haptic Feedback')
			self.root.protocol('WM_DELETE_WINDOW', self.shut_down)
			fm = tk.Frame(self.root)
			tk.Button(fm, text = 'Spring', command = self.dev.toggle_spring).pack(side = tk.LEFT)
			tk.Button(fm, text = 'Damper', command = self.dev.toggle_damper).pack(side = tk.LEFT)
			tk.Button(fm, text = 'Texture', command = self.dev.toggle_texture).pack(side = tk.LEFT)
			tk.Button(fm, text = 'Wall', command = self.dev.toggle_wall).pack(side = tk.LEFT)
			tk.Button(fm, text = 'Regular', command = self.dev.toggle_regular).pack(side = tk.LEFT)
			fm.pack(side = tk.TOP)
			self.mode_status = tk.Label(self.root, text = 'Mode is: ???????')
			self.mode_status.pack(side = tk.TOP)
			self.update_status()

	def update_status(self):
		angleAndTime = self.dev.get_angle_and_time()
		angle = angleAndTime[0]
		time = angleAndTime[1]
		mode = angleAndTime[2]
		motor = angleAndTime[3]
		angleAndTime[3] = motor / 15
		# print(angleAndTime)
		with open(r'document.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(angleAndTime)
		if (mode == 0):
			self.mode_status.configure(text = 'Mode is: Spring')
		elif (mode == 1):
			self.mode_status.configure(text = 'Mode is: Damper')
		elif (mode == 2):
			self.mode_status.configure(text = 'Mode is: Texture')
		elif (mode == 3):
			self.mode_status.configure(text = 'Mode is: Wall')
		elif (mode == 4):
			self.mode_status.configure(text = 'Mode is: Regular')
		self.update_job = self.root.after(10, self.update_status)

	def shut_down(self):
		self.root.after_cancel(self.update_job)
		self.root.destroy()
		self.dev.close()

if __name__=='__main__':
	gui = encodertestgui()
	gui.fd = open('document.csv','a')
	gui.root.mainloop()

