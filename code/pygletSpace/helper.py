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
# along with PyGletSpace.  If not, see <http://www.gnu.org/licenses/>.

import os
from pyglet import image

def get_image_dir():
	"""Get the directory used to store the images
	@returns string - the directory
	"""
	directory = os.path.abspath(os.path.dirname(__file__))
	directory = os.path.join(directory, 'data')
	return directory

def load_image(image_file_name):

	full_path = os.path.join(get_image_dir(), image_file_name)
	return image.load(full_path)
