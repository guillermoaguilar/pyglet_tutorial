#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  game.py
#  
#  Copyright (C) 2014 Guillermo Aguilar <gmo.aguilar.c@gmail.com>
#  
#  Based partially on PyGletSpace.py
#  Copyright (C) 2007 Mark Mruss <selsine@gmail.com>
#  http://www.learningpython.com
#
#  Pyglet_tutorial is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyglet_tutorial is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with pyglet_tutorial.  If not, see <http://www.gnu.org/licenses/>


from pyglet import window
from pyglet import clock
from pyglet import font


class SpaceGameWindow(window.Window):

	def __init__(self, *args, **kwargs):

		#Let all of the standard stuff pass through
		window.Window.__init__(self, *args, **kwargs)


	def main_loop(self):

		
		ft = font.load('Tahoma', 20)    #Create a font for our FPS clock

		fps_text = font.Text(ft, y=10)   # object to display the FPS

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


