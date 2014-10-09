#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  game.py
#  
#  Copyright 2014 Guillermo Aguilar <guille@schneebeere>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


from pyglet import window
from pyglet import clock
from pyglet import font


class SpaceGameWindow(window.Window):

	def __init__(self, *args, **kwargs):

		#Let all of the standard stuff pass through
		window.Window.__init__(self, *args, **kwargs)


	def main_loop(self):

		#Create a font for our FPS clock
		ft = font.load('Arial', 28)
		#The pyglet.font.Text object to display the FPS
		fps_text = font.Text(ft, y=10)

		while not self.has_exit:
			self.dispatch_events()
			self.clear()

			#Tick the clock
			clock.tick()
			#Gets fps and draw it
			fps_text.text = ("fps: %d") % (clock.get_fps())
			fps_text.draw()

			self.flip()



if __name__ == "__main__":
	space = SpaceGameWindow(width=1200, height=800, caption="Space Invaders !!", resizable=True)
	space.main_loop()


