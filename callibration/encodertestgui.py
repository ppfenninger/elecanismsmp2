#
## Copyright (c) 2018, Bradley A. Minch
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met: 
## 
##     1. Redistributions of source code must retain the above copyright 
##        notice, this list of conditions and the following disclaimer. 
##     2. Redistributions in binary form must reproduce the above copyright 
##        notice, this list of conditions and the following disclaimer in the 
##        documentation and/or other materials provided with the distribution. 
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
## POSSIBILITY OF SUCH DAMAGE.
#

import Tkinter as tk
import encodertest
import csv

class encodertestgui:

	def __init__(self):
		self.dev = encodertest.encodertest()
		if self.dev.dev >= 0:
			self.update_job = None
			self.root = tk.Tk()
			self.update_status()

	def update_status(self):
		angleAndTime = self.dev.get_angle_and_time()
		print(angleAndTime)
		angle = angleAndTime[0]
		time = angleAndTime[1]
		with open(r'document.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(angleAndTime)
		self.update_job = self.root.after(1, self.update_status)

	def shut_down(self):
		self.root.after_cancel(self.update_job)
		self.root.destroy()
		self.dev.close()

if __name__=='__main__':
	gui = encodertestgui()
	gui.fd = open('document.csv','a')
	gui.root.mainloop()

