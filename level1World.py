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
*  Description: This class runs the complete     *
*               game of Hopper!                  *
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

#import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from hopper import Hopper
from oceanWorld import Ocean
from platform import Platform
from coin import Coin
from berry import Berry

class Level1World(object):
	
	def __init__(self, render, loader, theBase, world, hopper):
		self.render = render
		self.loader = loader
		base = theBase
		self.world = world
		self.hopper = hopper

		base.disableMouse()
	

		inputState.watchWithModifiers('accelerate', 'arrow_up') #----- ITF: move to hopper class -----
		inputState.watchWithModifiers('turnLeft', 'arrow_left')
		inputState.watchWithModifiers('turnRight', 'arrow_right')
		#inputState.watchWithModifiers('toggleLight', 'l')

		#----- Play Music -----
		self.backgroundMusic = base.loader.loadSfx("backgroundMusic.wav")
		self.backgroundMusic.play()
		self.failSound = base.loader.loadSfx("fail.wav")

		self.isLit = False
		self.freeze = False
		#----- Setup Visible World -----
		ocean = Ocean(self.render, self.world, self.loader, self.hopper)
		
		x = -2; y = 3; z = 0
		platform = Platform(self.render, self.world, Vec3(9, 7, 0.5), Point3(x, y, z)) 
		for i in range(2):
			platform = Platform(self.render, self.world, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			x -= 12
			z += 2

		self.coin = Coin(self.render, self.world, self.hopper, 10, 0.35, 0.35, Vec3(3, 10, 3)) #ITF: broaden Coin class
		self.berry10 = Berry(self.render, self.world, self.hopper, 10, 0.35, 0.35, Vec3(5, 10, 3)) 
		self.endToken = Coin(self.render, self.world, self.hopper, 0, 0.6, 0.6, Vec3(0, 0, 1))
		self.endToken.coinNP.reparentTo(platform.platformBulletNode)
		
		#myFog = Fog("Fog Name")
		#myFog.setColor(0.5, 0.5, 0.5)
		#myFog.setExpDensity(0.003)
		#self.render.setFog(myFog)

		#----- Setup Camera -----
		base.camera.reparentTo(self.hopper.hopperModel)
		
		base.camera.setPos(0, 60, 50)#150.0)
		base.camera.setH(180)
		base.camera.lookAt(self.hopper.hopperModel)
		
	def update(self, task):
		self.processInput()
		dt = globalClock.getDt()
		self.world.doPhysics(dt, 10, 1/180.0)
		return task.cont
	
	def processInput(self):
		#if inputState.isSet('toggleLight'): self.toggleLight()

		speed = Vec3(0, 0, 0)
		omega = 0
		
		if self.freeze == False:
			if inputState.isSet('turnLeft'):   omega = 100
			if inputState.isSet('turnRight'):  omega = -100
			if inputState.isSet('accelerate'): speed.setY(0.6)
			#temporarily disabled!!! do not forget to undo! This includes the speed above!
			#else: speed.setY(0.5)
		else:
			self.hopper.stand()
		
		speed *= 10
		self.hopper.hopperBulletNode.setAngularMovement (omega)
		self.hopper.hopperBulletNode.setLinearMovement(speed, True)

	def unfreeze(self):
		self.freeze = False
		self.hopper.loopWalking()

	#----- Add more comments for blocks of code (e.g. these are for tasks, etc.) -----
	#----- Broken (ITF: Fix) -----
	def simulateWater(self, task):
		#self.hopper.hopperBulletNode.applyForce(Vec3(0, 0, 10))
		if self.hopper.hopperNP.getZ() < 0:
		#	self.hopper.hopperBulletNode.setLinearMovement(speed, True)	
			self.freeze = True
			return task.done
		else:
			return task.cont
	
	#----- DO NOT USE!!! ------	
	def toggleLight(self):
		if self.isLit == False:
			self.addLight()
			self.isLit = True
		else:
			self.destroyLight()
			self.isLit = False

	def addLight(self):
		self.dlight = DirectionalLight('dlight')
		self.dlight.setColor(VBase4(0.9, 0.9, 0.8, 1))
		self.dlnp = self.render.attachNewNode(self.dlight)
		self.dlnp.setHpr(90, -30, 0)
		self.render.setLight(self.dlnp)
		
		slight = Spotlight('slight')
		slens = PerspectiveLens()
		slight.setLens(slens)
		slight.setColor(Vec4(1, 1, 1, 1))
		self.slnp = self.render.attachNewNode(slight)
		self.slnp.reparentTo(self.hopper.hopperNP)
		self.slnp.setPos(0, 40, 50)
		self.slnp.lookAt(self.hopper.hopperNP)
		self.render.setLight(self.slnp)

		self.render.setShaderAuto()
		slight.setShadowCaster(True)

		alight = AmbientLight('alight')
		alight.setColor(VBase4(0.5, 0.5, 0.7, 1))
		self.alnp = self.render.attachNewNode(alight)
		self.render.setLight(self.alnp)

	def destroyLight(self):
		self.render.clearLight(self.dlnp)
		self.render.clearLight(self.alnp)
		self.render.clearLight(self.slnp)















