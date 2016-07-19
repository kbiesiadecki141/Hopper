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
*  Description: This class creates the wizard    *
*               lair for the challenge level of  *
*               the game.                        *
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

class WizardLair(object):
	
	def __init__(self, render, world, theLoader, hopper):
		self.render = render
		self.world = world
		self.loader = theLoader
		self.hopper = hopper
		"""	
		wizardLairShape = BulletPlaneShape(Vec3(0, 0, 1), 0)
		wizardLairBulletNode = BulletRigidBodyNode("WizardFloor")
		wizardLairBulletNode.addShape(wizardLairShape)
		wizardLairNP = self.render.attachNewNode(wizardLairBulletNode)
		wizardLairNP.setPos(0, 0, -10)
		self.world.attachRigidBody(wizardLairBulletNode)
		"""
		#fix
		"""
		self.environ = loader.loadModel("models/square")	  
		self.environ.reparentTo(render)
		self.environ.setPos(0,0,-10)
		self.environ.setScale(100,100,1)
		self.floorTex = self.loader.loadTexture('models/wizardLair.jpg')
		self.environ.setTexture(self.floorTex, 1)
		self.floorTex.setWrapU(Texture.WMRepeat)
		"""

		base.setBackgroundColor(0, 0, 0)
		




