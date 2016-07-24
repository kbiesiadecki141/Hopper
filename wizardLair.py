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

		self.wizardGate = loader.loadModel("models/gate/gate.egg")
		self.wizardGate.setPos(0, 0, 1) #Note: Wizard Gate (and other models) MUST be reparented to a platform for proper placement
		self.wizardGate.setScale(0.007, 0.007, 0.004)
		self.wizardGate.setH(90)

		self.fire = loader.loadModel("models/fire/fire.egg")
		self.fire.reparentTo(self.wizardGate)
		self.fire.setPos(-600, -300, 0)
		self.fire.setScale(3)
		
		self.fire = loader.loadModel("models/fire/fire.egg")
		self.fire.reparentTo(self.wizardGate)
		self.fire.setPos(600, -300, 0)
		self.fire.setScale(3)
		
		self.castle = loader.loadModel("models/art/alice-amusement-park--hauntedhouse/hauntedhouse.egg")
		self.castle.setPos(0, 0, 0)
		self.castle.setScale(0.15, 0.15, 0.3)
		self.castle.setH(180)
		
		castleShape = BulletBoxShape(Vec3(9, 6, 7))
		self.castleBulletNode = BulletRigidBodyNode("WizardCastle")
		self.castleBulletNode.addShape(castleShape)
		self.castleNP = self.render.attachNewNode(self.castleBulletNode)
		self.castleNP.setPos(-38, 33, 13)
		
		self.world.attachRigidBody(self.castleBulletNode)
		
		lairShape = BulletBoxShape(Vec3(4, 8.5, 7))
		self.lairBulletNode = BulletRigidBodyNode("WizardLair")
		self.lairBulletNode.addShape(lairShape)
		self.lairNP = self.render.attachNewNode(self.lairBulletNode)
		self.lairNP.setPos(-110, 15, 20)

		self.world.attachRigidBody(self.lairBulletNode)
		
		self.lair = loader.loadModel("models/Church/Church.egg")
		self.lair.setPos(0, 0, 1) #Note: Wizard Lair (and other models) MUST be reparented to a platform for proper placement
		self.lair.setScale(0.3, 0.3, 0.2)
		self.lair.setH(90)

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
		




