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

		#----- Play Music -----
		self.backgroundMusic = base.loader.loadSfx("backgroundMusic.wav")
		self.backgroundMusic.play()
		self.failSound = base.loader.loadSfx("fail.wav")

		#------ State Variables -----
		self.isLit = False

		#----- Setup Visible World -----
		self.platforms = []
		self.berries = []
		self.coins = []

		self.ocean = Ocean(self.render, self.world, self.loader, self.hopper)
		self.setupPlatforms()		
		self.setupCoins()
		self.setupBerries()
		self.endToken = Coin(self.render, self.world, self.hopper, 0, 0.6, 0.6, Vec3(0, 0, 1))
		self.endToken.coinNP.reparentTo(self.platforms[-1].platformBulletNode)
		
		#----- Setup Camera -----
		base.camera.reparentTo(self.hopper.hopperModel)
		base.camera.setPos(0, 60, 50)#150.0)
		base.camera.setH(180)
		base.camera.lookAt(self.hopper.hopperModel)
	
	#----- Tasks -----
	def update(self, task):
		self.hopper.processInput()
		dt = globalClock.getDt()
		self.world.doPhysics(dt, 10, 1/180.0)
		return task.cont
	
	def simulateWater(self, task):
		if self.hopper.hopperNP.getZ() < 0:
			self.hopper.freeze = True
			return task.done
		else:
			return task.cont

	#----- Setup Item Functions -----	
	def setupPlatforms(self):
		x = -2; y = 3; z = 0
		
		heading = 0
		for i in range(2):
			platform = Platform(self.render, self.world, heading, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			self.platforms.append(platform)
			x -= 12; z += 2
		
		heading = 45
		for i in range(3):
			platform = Platform(self.render, self.world, heading, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			x -= 8; y -= 8; z += 2
			self.platforms.append(platform)
		
		heading = -45
		for i in range(3):
			platform = Platform(self.render, self.world, heading, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			x -= 8; y += 8; z -= 2
			self.platforms.append(platform)
	
	def setupCoins(self):
		coin = Coin(self.render, self.world, self.hopper, 10, 0.35, 0.35, Vec3(3, 10, 3))
		self.coins.append(coin)

	def resetCoins(self):
		for coin in self.coins:
			coin.removeCoin()
		self.setupCoins()

	def setupBerries(self):
		berry10 = Berry(self.render, self.world, self.hopper, 10, 0.35, 0.35, Vec3(5, 10, 3)) 
		self.berries.append(berry10)
	
	def resetBerries(self):
		for berry in self.berries:
			berry.removeBerry()
		self.setupBerries()
	
	#----- Light Functions -----
	def addLight(self):
		self.dlight = DirectionalLight('dlight')
		self.dlight.setColor(VBase4(0.9, 0.9, 0.8, 1))
		self.dlnp = self.render.attachNewNode(self.dlight)
		self.dlnp.setHpr(90, -30, 0)
		self.render.setLight(self.dlnp)
		
		self.slight = Spotlight('slight')
		slens = PerspectiveLens()
		self.slight.setLens(slens)
		self.slight.setColor(Vec4(1, 1, 1, 1))
		self.slnp = self.render.attachNewNode(self.slight)
		self.slnp.reparentTo(self.hopper.hopperNP)
		self.slnp.setPos(0, 40, 50)
		self.slnp.lookAt(self.hopper.hopperNP)
		self.render.setLight(self.slnp)
		
		self.alight = AmbientLight('alight')
		self.alight.setColor(VBase4(0.2, 0.4, 1, 1))
		self.alnp = self.render.attachNewNode(self.alight)
		
		self.render.setLight(self.alnp)
		
		self.render.setShaderAuto()
		self.slight.setShadowCaster(True)

	def destroyLight(self):
		self.render.clearLight(self.dlnp)
		self.render.clearLight(self.alnp)
		self.render.clearLight(self.slnp)















