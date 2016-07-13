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
from spinner import Spinner

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
		self.spinners = []
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
		for i in range(6):
			platform = Platform(self.render, self.world, heading, Vec3(7, 6, 0.5), Point3(x, y, z)) 
			self.platforms.append(platform)
			
			if i == 3 or i == 5:
				spinner = Spinner(self.render, self.world, 90, 14, Vec3(2.2, 0.3, 1), Point3(x+7, y+6, z+2))
				self.spinners.append(spinner)	
			
			x -= 12; z += 2
		
		heading = 45
		for i in range(7):
			platform = Platform(self.render, self.world, heading, Vec3(7, 6, 0.5), Point3(x, y, z)) 
			self.platforms.append(platform)
			
			if i == 5 or i == 7:
				spinner = Spinner(self.render, self.world, 90, 14, Vec3(2.2, 0.3, 1), Point3(x+7, y+6, z+2))
				self.spinners.append(spinner)	
			
			x -= 8; y -= 8; z += 2
		
		heading = -45
		for i in range(5):
			platform = Platform(self.render, self.world, heading, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			self.platforms.append(platform)
			
			if i == 0 or i == 4:
				spinner = Spinner(self.render, self.world, 90, 14, Vec3(2.2, 0.3, 1), Point3(x+7, y+6, z+2))
				self.spinners.append(spinner)	
			
			x -= 8; y += 8; z -= 2
		
		heading = 90
		for i in range(7):
			platform = Platform(self.render, self.world, heading, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			self.platforms.append(platform)
			
			if i == 3 or i == 5:
				spinner = Spinner(self.render, self.world, 90, 14, Vec3(2.2, 0.3, 1), Point3(x+7, y+6, z+2))
				self.spinners.append(spinner)	
			
			y += 8; z += 2
	 
	 	"""
		spinDex = 4 #ehh?? get it??!! spinDex = spin index?!! X-D
		for i in range(3):
			self.spinner = Spinner(self.render, self.world, 90, 14, Vec3(2.2, 0.3, 1), Point3(0, 0, 0))
			self.spinner.spinnerBulletNode.reparentTo(self.platforms[spinDex].platformBulletNode)
			spinDex += 3
		"""

	#def setup

	def setupCoins(self):
		index = 0
		for i in range(4):
			coin = Coin(self.render, self.world, self.hopper, 10, 0.35, 0.35, Point3(1, 0, 2))
			coin.coinNP.reparentTo(self.platforms[index].platformBulletNode)
			self.coins.append(coin)
			index += 5

	def resetCoins(self):
		for coin in self.coins:
			coin.removeCoin()
		self.setupCoins()

	def setupBerries(self):
		index = 1
		mult = 1
		for i in range(5):
			berry1 = Berry(self.render, self.world, self.hopper, 10*mult, 0.35, 0.35, Point3(0, 0, 2))
			berry1.berryNP.reparentTo(self.platforms[index].platformBulletNode)
			self.berries.append(berry1)
			index += 3
			mult *= -1
	
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
		self.alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
		self.alnp = self.render.attachNewNode(self.alight)
		
		self.render.setLight(self.alnp)
		
		self.render.setShaderAuto()
		self.slight.setShadowCaster(True)

	def destroyLight(self):
		self.render.clearLight(self.dlnp)
		self.render.clearLight(self.alnp)
		self.render.clearLight(self.slnp)















