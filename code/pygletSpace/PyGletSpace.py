#!/usr/bin/env python

# PyGletSpace - An Example game using PyGlet
# Copyright (C) 2007 Mark Mruss <selsine@gmail.com>
# http://www.learningpython.com
#
# This file is part of PyGletSpace.
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyGletSpace.  If not, see <http://www.gnu.org/licenses/>

__author__ = "Mark Mruss <selsine@gmail.com>"
__version__ = "0.1"
__date__ = "Date: 2007/10/13"
__copyright__ = "Copyright (c) 2007 Mark Mruss"
__license__ = "GPL"

from pyglet import window
from pyglet import clock
from pyglet import font
import random

import helper

class SpaceGameWindow(window.Window):

	def __init__(self, *args, **kwargs):
		self.max_monsters = 30
		#Let all of the standard stuff pass through
		window.Window.__init__(self, *args, **kwargs)
		self.set_mouse_visible(False)
		self.init_sprites()

	def init_sprites(self):
		self.bullets = []
		self.monsters = []
		self.ship = SpaceShip(self.width - 150, 10, x=100,y=100)
		self.bullet_image = helper.load_image("bullet.png")
		self.monster_image = helper.load_image("monster.png")

	def main_loop(self):

		#Create a font for our FPS clock
		ft = font.load('Arial', 28)
		#The pyglet.font.Text object to display the FPS
		fps_text = font.Text(ft, y=10)

		#Schedule the Monster creation
		clock.schedule_interval(self.create_monster, 0.3)
		clock.set_fps_limit(30)

		while not self.has_exit:
			self.dispatch_events()
			self.clear()

			self.update()
			self.draw()

			#Tick the clock
			clock.tick()
			#Gets fps and draw it
			fps_text.text = ("fps: %d") % (clock.get_fps())
			fps_text.draw()
			self.flip()

	def update(self):

		to_remove = []
		for sprite in self.monsters:
			sprite.update()
			#Is it dead?
			if (sprite.dead):
				to_remove.append(sprite)
		#Remove dead sprites
		for sprite in to_remove:
			self.monsters.remove(sprite)

		#Bullet update and collision
		to_remove = []
		for sprite in self.bullets:
			sprite.update()
			if (not sprite.dead):
				monster_hit = sprite.collide_once(self.monsters)
				if (monster_hit is not None):
					sprite.on_kill()
					self.monsters.remove(monster_hit)
					to_remove.append(sprite)
			else:
				to_remove.append(sprite)
		#Remove bullets that hit monsters
		for sprite in to_remove:
			self.bullets.remove(sprite)

		self.ship.update()
		#Is it dead?
		monster_hit = self.ship.collide_once(self.monsters)
		if (monster_hit is not None):
			self.ship.dead = True
			self.has_exit = True

	def draw(self):

		for sprite in self.bullets:
			sprite.draw()
		for sprite in self.monsters:
			sprite.draw()
		self.ship.draw()

	def create_monster(self, interval):
		if (len(self.monsters) < self.max_monsters):
			self.monsters.append(Monster(self.monster_image
				, x=random.randint(0, self.width) , y=self.height))

	"""******************************************
	Event Handlers
	*********************************************"""
	def on_mouse_motion(self, x, y, dx, dy):
		self.ship.x = x
		self.ship.y = y

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.ship.x = x
		self.ship.y = y

	def on_mouse_press(self, x, y, button, modifiers):

		if (button == 1):
			self.bullets.append(Bullet(self.ship
					, self.bullet_image
					, self.height
					, x=x + (self.ship.image.width / 2) - (self.bullet_image.width / 2)
					, y=y))

class Sprite(object):

	def __get_left(self):
		return self.x
	left = property(__get_left)

	def __get_right(self):
		return self.x + self.image.width
	right = property(__get_right)

	def __get_top(self):
		return self.y + self.image.height
	top = property(__get_top)

	def __get_bottom(self):
		return self.y
	bottom = property(__get_bottom)

	def __init__(self, image_file, image_data=None, **kwargs):

		#init standard variables
		self.image_file = image_file
		if (image_data is None):
			self.image = helper.load_image(image_file)
		else:
			self.image = image_data
		self.x = 0
		self.y = 0
		self.dead = False
		#Update the dict if they sent in any keywords
		self.__dict__.update(kwargs)

	def draw(self):
		self.image.blit(self.x, self.y)

	def update(self):
		pass

	def intersect(self, sprite):
		"""Do the two sprites intersect?
		@param sprite - Sprite - The Sprite to test
		"""
		return not ((self.left > sprite.right)
			or (self.right < sprite.left)
			or (self.top < sprite.bottom)
			or (self.bottom > sprite.top))

	def collide(self, sprite_list):
		"""Determing ther are collisions with this
		sprite and the list of sprites
		@param sprite_list - A list of sprites
		@returns list - List of collisions"""

		lst_return = []
		for sprite in sprite_list:
			if (self.intersect(sprite)):
				lst_return.append(sprite)
		return lst_return

	def collide_once(self, sprite_list):
		"""Determine if there is at least one
		collision between this sprite and the list
		@param sprite_list - A list of sprites
		@returns - None - No Collision, or the first
		sprite to collide
		"""
		for sprite in sprite_list:
			if (self.intersect(sprite)):
				return sprite
		return None

class SpaceShip(Sprite):

	def __init__(self, text_x, text_y, **kwargs):

		self.kills = 0
		Sprite.__init__(self, "ship.png", **kwargs)

		#Create a font for our kill message
		self.font = font.load('Arial', 28)
		#The pyglet.font.Text object to display the FPS
		self.kill_text = font.Text(self.font, y=text_y, x=text_x)

	def draw(self):
		Sprite.draw(self)
		self.kill_text.text = ("Kills: %d") % (self.kills)
		self.kill_text.draw()

	def on_kill(self):
		self.kills += 1


class Bullet(Sprite):

	def __init__(self, parent_ship, image_data, top, **kwargs):
		self.velocity = 5
		self.screen_top = top
		self.parent_ship = parent_ship
		Sprite.__init__(self,"", image_data, **kwargs)

	def update(self):
		self.y += self.velocity
		#Have we gone off the screen?
		if (self.bottom > self.screen_top):
			self.dead = True

	def on_kill(self):
		"""We have hit a monster let the parent know"""
		self.parent_ship.on_kill()

class Monster(Sprite):

	def __init__(self, image_data, **kwargs):
		self.y_velocity = 5
		self.set_x_velocity()
		self.x_move_count = 0
		self.x_velocity
		Sprite.__init__(self, "", image_data, **kwargs)

	def update(self):
		self.y -= self.y_velocity
		self.x += self.x_velocity#random.randint(-3,3)
		self.x_move_count += 1
		#Have we gone beneath the botton of the screen?
		if (self.y < 0):
			self.dead = True

		if (self.x_move_count >=30):
			self.x_move_count = 0
			self.set_x_velocity()

	def set_x_velocity(self):
		self.x_velocity = random.randint(-3,3)

if __name__ == "__main__":
	# Someone is launching this directly
	space = SpaceGameWindow()
	space.main_loop()

