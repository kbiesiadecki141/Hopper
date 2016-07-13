"""
**************************************************
*                                                *
*  Katelyn Biesiadecki                           *
*  CS454 Game Programming (Kang, Ijaz)           *
*                                                *
*  Start Date: July 6, 2016                      *
*  Midway Due Date: July 13, 2016                *
*  Final Due Date: July 23, 2016                 *
*                                                *
*  Project Name: Hopper                          *
*  Description: This class creates the "coin"    *
*               for pickup/powerup during the    *
*               game.                            *
*                                                *
**************************************************
"""

import random, sys, os, math
from math import sin, cos

from direct.actor.Actor import Actor
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.showbase.InputStateGlobal import inputState
from direct.interval.IntervalGlobal import *

from panda3d.core import *
from panda3d.bullet import *

from direct.gui.OnscreenText import OnscreenText

class Berry(object):
	
	def __init__(self, render, world, hopper, berryValue, radius, height, posMap):
		self.render = render
		self.world = world
		self.hopper = hopper
		self.berryValue = berryValue #if berryVal > 0, call boost; else, call lowerHealth
		self.radius = radius
		self.height = height
		self.volume = 1

		self.berryShape = BulletCylinderShape(radius, height, ZUp)
		self.ghostNode = BulletGhostNode("Berry")
		self.ghostNode.addShape(self.berryShape)
		self.berryNP = self.render.attachNewNode(self.ghostNode)
		self.berryNP.setCollideMask(BitMask32.allOff())
		self.berryNP.setPos(posMap) 
		self.berryNP.setR(90)
		self.world.attachGhost(self.ghostNode)
		
		self.berryModel = loader.loadModel("models/art/cat-shapes/alice-shapes--icosahedron/icosahedron.egg") 
		berryTexture = loader.loadTexture("models/emTex.jpg")
		self.berryModel.setTexture(berryTexture, 1)
		self.berryModel.reparentTo(self.berryNP)
		self.berryModel.setScale(0.4*radius)
		self.berryModel.setPos(0, 0, 0)
	
	def setVolume(self, volume):
		self.volume = volume

	def collectBerry(self, task):
		pUp = base.loader.loadSfx("powerUp.mp3")
		pUp.setVolume(self.volume)
		pUp.play()
		self.removeBerry()
	
	def removeBerry(self):
		self.berryNP.detach_node()
		
	def spinBerry(self, task):
		theta = task.time*20.0
		self.berryNP.setH(theta)
		return task.cont











		




