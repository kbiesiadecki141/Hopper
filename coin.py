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

class Coin(object):
	
	def __init__(self, render, world, hopper, coinValue, radius, height, posMap):
		self.render = render
		self.world = world
		self.hopper = hopper
		self.coinValue = coinValue
		self.radius = radius
		self.height = height
		self.volume = 1
		self.chaChing = base.loader.loadSfx("sounds/coinCollect.wav")

		self.coinShape = BulletCylinderShape(radius, height, ZUp)
		self.ghostNode = BulletGhostNode("Coin")
		self.ghostNode.addShape(self.coinShape)
		self.coinNP = self.render.attachNewNode(self.ghostNode)
		self.coinNP.setCollideMask(BitMask32.allOff())
		self.coinNP.setPos(posMap) #ITF: add to args
		self.coinNP.setR(90)
		self.world.attachGhost(self.ghostNode)
		
		material = Material()
		material.setShininess(10.0)
		material.setAmbient((1, 1, 0, 1))
	
		self.coinModel = loader.loadModel("models/mint/Mint.egg") 
		coinTexture = loader.loadTexture("models/mint/goldCoin.jpg") 
		self.coinModel.setTexture(coinTexture, 1)
		self.coinModel.reparentTo(self.coinNP)
		self.coinModel.setScale(14.286*radius)
		self.coinModel.setPos(0, 0, 0)
		#self.coinModel.setMaterial(material)
	
	def setVolume(self, volume):
		self.volume = volume

	def collectCoin(self, task):
		self.chaChing.setVolume(self.volume)
		self.chaChing.play()
		self.removeCoin()
	
	def removeCoin(self):
		self.coinNP.remove_node()

		print "Inside remove coin; removing a coin"

	def stopSound(self):
		self.chaChing.stop()











		




