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

import pyglet
from pyglet import window
from pyglet import clock
from pyglet import font


class SpaceGameWindow(window.Window):
    
    def __init__(self, *args, **kwargs):

        #Let all of the arguments pass through
        self.win = window.Window.__init__(self, *args, **kwargs)
        self.setup()
        
    def setup(self):
        
        clock.schedule_interval(self.update, 1.0/30) # update at FPS of Hz
        
        # setting text objects
        ft = font.load('Tahoma', 20)    #Create a font for our FPS clock
        self.fpstext = font.Text(ft, y=10)   # object to display the FPS
        
        
    def update(self, dt):
        pass
    
    def on_draw(self):
        self.clear() # clearing buffer
        clock.tick() # ticking the clock
        
        # showing FPS
        self.fpstext.text = "fps: %d" % clock.get_fps()
        self.fpstext.draw()
        
        
        
        # flipping
        self.flip()
        


if __name__ == "__main__":
	win = SpaceGameWindow(caption="Space Invaders !!")
	pyglet.app.run()


