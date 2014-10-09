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

import random
import pyglet
from pyglet import window
from pyglet import clock
from pyglet import font
from pyglet.window import key 


class SpaceGame(window.Window):
    
    def __init__(self, *args, **kwargs):

        #Let all of the arguments pass through
        self.win = window.Window.__init__(self, *args, **kwargs)
        self.setup()
        
        self.maxaliens = 50
        
    def setup(self):
        
        clock.schedule_interval(self.create_alien, 0.3)
        clock.schedule_interval(self.update, 1.0/30) # update at FPS of Hz
        
        #clock.set_fps_limit(30)
        
        # setting text objects
        ft = font.load('Tahoma', 20)    #Create a font for our FPS clock
        self.fpstext = font.Text(ft, y=10)   # object to display the FPS
        
        # reading and saving images
        self.spaceship_image = pyglet.image.load('images/ship2.png')
        self.alien_image = pyglet.image.load('images/monster.png')
        self.bullet_image = pyglet.image.load('images/bullet_white.png')
        # create one spaceship
        self.spaceship = Spaceship(self.spaceship_image, x=50, y=50)
        
        self.aliens=[] # list of Alien objects
        self.bullets=[] # list of Bullet objects
        
    def create_alien(self, dt):
        
        if len(self.aliens) < self.maxaliens:
            self.aliens.append( Alien(self.alien_image, x=random.randint(0, self.width) , y=self.height))
        
        
    def update(self, dt):
        
        # updating aliens
        for alien in self.aliens:
            alien.update()
            if alien.dead:
                self.aliens.remove(alien)
        
        # updating bullets
        for bullet in self.bullets:
            bullet.update()
            if bullet.dead:
                self.bullets.remove(bullet)
            
        

    def on_draw(self):
        self.clear() # clearing buffer
        clock.tick() # ticking the clock
        
        # showing FPS
        self.fpstext.text = "fps: %d" % clock.get_fps()
        self.fpstext.draw()
        
        # drawing objects of the game
        self.spaceship.draw()
        for alien in self.aliens:
            alien.draw()
        for bullet in self.bullets:
            bullet.draw()
            
        # flipping
        self.flip()
    
    
    ## Event handlers
    def on_key_press(self, symbol, modifiers):
        
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')  
            
        elif symbol == key.LEFT:
            self.spaceship.x -= 10
        elif symbol == key.RIGHT:
            self.spaceship.x += 10
            
    def on_mouse_motion(self, x, y, dx, dy):
        self.spaceship.x = x

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.spaceship.x = x
        
    def on_mouse_press(self, x, y, button, modifiers):

        if (button == 1):
            self.bullets.append(Bullet(self.bullet_image, self.spaceship, 
                                       self.height, x=self.spaceship.x + self.spaceship.width/2.0,
                                       y=self.spaceship.y + self.spaceship.height/2.0))



###############################################################################
class Spaceship(pyglet.sprite.Sprite):

	def __init__(self, *args, **kwargs):
         pyglet.sprite.Sprite.__init__(self, *args, **kwargs)
         self.kills = 0
        
	def on_kill(self):
		self.kills += 1


###############################################################################    
class Alien(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)
        self.y_velocity = 5
        self.set_x_velocity()
        self.x_move_count = 0
        self.dead=False

    def set_x_velocity(self):
        self.x_velocity = random.randint(-3,3)

    def update(self):
        # update position
        self.y -= self.y_velocity
        self.x += self.x_velocity
        # and counter
        self.x_move_count += 1
        
        #Have we gone beneath the botton of the screen?
        if (self.y < 0):
            self.dead = True
            
        if (self.x_move_count >=30):
            self.x_move_count = 0
            self.set_x_velocity()
   
###############################################################################    
class Bullet(pyglet.sprite.Sprite):

	def __init__(self, image_data, parent_ship, screen_top, **kwargs):
          self.dead=False
          self.velocity = 5
          self.screen_top = screen_top
          self.parent_ship = parent_ship
          pyglet.sprite.Sprite.__init__(self, image_data, **kwargs)

	def update(self):
		self.y += self.velocity
		if (self.y > self.screen_top):
			self.dead = True

	def on_kill(self):
		self.parent_ship.on_kill()    # when hitting an alien, call on_kill to update spaceship counter
   
###############################################################################
  
if __name__ == "__main__":
	win = SpaceGame(caption="Space Invaders !!", height=800, width=800)
	pyglet.app.run()


