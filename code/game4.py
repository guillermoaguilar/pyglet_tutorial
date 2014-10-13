#!/usr/bin/env python

import random, math
import pyglet
from pyglet import window
from pyglet import clock
from pyglet import font
from pyglet.window import key 

   
###############################################################################
class SpaceGame(window.Window):
    
    def __init__(self, *args, **kwargs):

        #Let all of the arguments pass through
        self.win = window.Window.__init__(self, *args, **kwargs)
        
        clock.schedule_interval(self.update, 1.0/30) # update at 30 Hz
        clock.schedule_interval(self.create_alien, 1.0/5) # update at 5 Hz
        
        
        # setting text objects
        ft = font.load('Tahoma', 20)         #Create a font for our FPS clock
        self.fpstext = font.Text(ft, y=10)   # object to display the FPS

        # loading image
        self.spaceship_image = pyglet.image.load('images/ship3.png')
        self.spaceship = Spaceship(self.spaceship_image, x=200, y=50)
        
        self.alien_image = pyglet.image.load('images/invader.png')
        self.aliens = []
        
        
        
    def create_alien(self, dt):
        self.aliens.append(Alien(self.alien_image, 
                            x=random.randint(0, self.width), y=self.height))
        
    def update(self, dt):
        
        for alien in self.aliens:
            alien.update()
            if alien.dead:
                self.aliens.remove(alien)


    def on_draw(self):
        self.clear() # clearing buffer
        clock.tick() # ticking the clock
        
        # showing FPS
        self.fpstext.text = "fps: %d" % clock.get_fps()
        self.fpstext.draw()
        
        self.spaceship.draw()
        for alien in self.aliens:
            alien.draw()
        
        # flipping
        self.flip()
    
    
    ## Event handlers
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')  
            
    def on_mouse_motion(self, x, y, dx, dy):
        self.spaceship.x = x
        #self.spaceship.y = y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
        
    def on_mouse_press(self, x, y, button, modifiers):
        pass


####################################################################
class Spaceship(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)
     
        
####################################################################
class Alien(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)   
        self.x_velocity= random.randint(-3,3)
        self.y_velocity= 5
        self.dead = False
        
    def update(self):
        self.x -= self.x_velocity
        self.y -= self.y_velocity
        
        if self.y < 0:
            self.dead=True 
 
        
###################################################################
  
if __name__ == "__main__":
    win = SpaceGame(caption="Aliens!! Invaders from Space!!", height=600, width=800)
    pyglet.app.run()


