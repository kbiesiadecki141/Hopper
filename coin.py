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
	
	def __init__(self, render, world, hopper):#, coinValue):
		self.render = render
		self.world = world
		self.hopper = hopper
		radius = 0.35
		height = 0.35
		self.coinShape = BulletCylinderShape(radius, height, ZUp)
		self.ghostNode = BulletGhostNode("Coin")
		self.ghostNode.addShape(self.coinShape)
		self.coinNP = self.render.attachNewNode(self.ghostNode)
		self.coinNP.setCollideMask(BitMask32.allOff())
		self.coinNP.setPos(3, 10, 3) #ITF: add to args
		self.coinNP.setR(90)
		self.world.attachGhost(self.ghostNode)
		
		self.coinModel = loader.loadModel("models/mint/Mint.egg") 
		self.coinModel.reparentTo(self.coinNP)
		self.coinModel.setScale(5)
		self.coinModel.setPos(0, 0, 0)
	
	def detectCollisionForGhosts(self, task):
		# contactTestPair returns a BulletContactResult object
		contactResult = self.world.contactTestPair(self.hopper.getNode(), self.ghostNode) 
		if len(contactResult.getContacts()) > 0:
			print "Hopper is in contact with: ", self.ghostNode.getName()
			return task.done
		else:
			return task.cont
	
	def removeCoin(self):
		self.coinNP.detach_node()
		












		




