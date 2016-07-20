"""
**************************************************
*								*
*  Katelyn Biesiadecki				   *
*  CS454 Game Programming (Kang, Ijaz)           *
*								*
*  Start Date: July 6, 2016		          *
*  Midway Due Date: July 13, 2016		    *
*  Final Due Date: July 23, 2016		     *
*								*
*  Project Name: Hopper				  *
*  Description: This class runs the complete     *
*		   game of Hopper!		      *
*								*
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
from pandac.PandaModules import CollisionHandlerEvent, CollisionNode, CollisionSphere, CollisionTraverser, BitMask32, CollisionRay

from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from hopper import Hopper
from enemy import Enemy
from wizardLair import WizardLair
from platform import Platform
from coin import Coin
from berry import Berry
from spinner import Spinner

class Level2World(object):
	
	def __init__(self, render, loader, theBase, world, hopper):
		self.render = render
		self.loader = loader
		base = theBase
		self.world = world
		self.hopper = hopper

		base.disableMouse()

		#----- Play Music -----
		self.backgroundMusic = base.loader.loadSfx("sounds/backgroundMusic.wav")
		self.backgroundMusic.play()
		self.failSound = base.loader.loadSfx("sounds/fail.wav")

		#------ State Variables -----
		self.isLit = False

		#----- Setup Visible World -----
		self.platforms = []
		self.spinners = []
		self.berries = []
		self.coins = []
		self.enemies = []

		self.setupPlatforms()		
		self.setupCoins()
		self.setupBerries()
		self.setupEnemies()

		self.endToken = Coin(self.render, self.world, self.hopper, 0, 0.6, 0.6, Vec3(0, 0, 1))
		self.endToken.coinNP.reparentTo(self.platforms[-1].platformBulletNode)
		
		self.wizardLair = WizardLair(self.render, self.world, self.loader, self.hopper)
		self.wizardLair.wizardGate.reparentTo(self.platforms[1].platformBulletNode)	
		#----- Setup Light -----
		self.directionalLight2 = DirectionalLight( "directionalLight" )
		self.directionalLight2.setColor( Vec4( 1, 1, 1, 1 ) )
		self.directionalLight2.setDirection(Vec3(0, 0, -1))
		self.directionalLightNP = self.render.attachNewNode(self.directionalLight2)
		
		#----- Collision Handling -----
		base.cTrav = CollisionTraverser()
		self.collisionHandler = CollisionHandlerEvent()

		self.pickerNode = CollisionNode('mouseRayCollisionNode')
		self.pickerNP = base.camera.attachNewNode(self.pickerNode)
		self.pickerRay = CollisionRay()
		self.pickerNode.addSolid(self.pickerRay)
		base.cTrav.addCollider(self.pickerNP, self.collisionHandler)
		self.collisionHandler.addInPattern("mouseRayIntoEnemy")
		self.collisionHandler.addOutPattern("mouseRayOutEnemy")
		
		self.pickingEnabledObject = None

	#----- Tasks -----
	def update(self, task):
		self.hopper.processInput()
		for enemy in self.enemies:
			if enemy.getHealth() != 0:
				enemy.pace()
		dt = globalClock.getDt()
		self.world.doPhysics(dt, 10, 1/180.0)
		return task.cont
	
	def simulateWater(self, task):
		if self.hopper.hopperNP.getZ() < 0:
			self.hopper.freeze = True
			return task.done
		else:
			return task.cont
	
	def rayUpdate(self, task):
		if base.mouseWatcherNode.hasMouse():
			mPos = base.mouseWatcherNode.getMouse()
			self.pickerRay.setFromLens(base.camNode, mPos.getX(), mPos.getY())
		return task.cont

	#----- Setup Enemy Functions -----
	def setupEnemies(self):
		enemy1 = Enemy(self.render, self.world, base, Point3(0, 0, 1), self.hopper, 1)
		enemy1.enemyNP.reparentTo(self.platforms[3].platformBulletNode)
		enemy2 = Enemy(self.render, self.world, base, Point3(0, 0, 1), self.hopper, 2)
		enemy2.enemyNP.reparentTo(self.platforms[4].platformBulletNode)
		self.enemies.append(enemy1)
		self.enemies.append(enemy2)
     	
	def resetEnemies(self):
		for enemy in self.enemies:
			enemy.enemyNP.remove_node()
		self.enemies = []
		self.setupEnemies()

	def collideEventIn(self, entry):
		print "Wahoo!"
		np_from = entry.getFromNodePath()
		np_into = entry.getIntoNodePath()
		print "'%s' goes INTO '%s'!\nYou may now click the LMB" % (np_from.getName(), np_into.getName())
		np_into.getParent().setColor(.6, 0.5, 1.0, 1)
		self.pickingEnabledObject = np_into

	def collideEventOut(self, entry):
		print "Outwhoo!"
		self.pickingEnabledObject = None
		print "you LEFT enemy alone"
		np_into = entry.getIntoNodePath()
		np_into.getParent().setColor(1.0, 1.0, 1.0, 1)

	def mousePick(self, status):
		print "Inside mouse pick"
		if self.pickingEnabledObject:
			if status == 'down':
				idNum = self.pickingEnabledObject.getTag("id")
				self.enemies[int(idNum)-1].lowerHealth()
			if status == 'up':
				pass

	#----- Setup Item Functions -----	
	def setupPlatforms(self):
		path = "images/wizardFloor.jpg"
		platform = Platform(self.render, self.world, 0, Vec3(10, 7, 0.5), Point3(-2, 3, -1), tex = path) 
		self.platforms.append(platform)
		platform = Platform(self.render, self.world, 0, Vec3(10, 7, 0.5), Point3(-13, 3, -1), tex = path) 
		self.platforms.append(platform)
		platform = Platform(self.render, self.world, 0, Vec3(10, 7, 0.5), Point3(-24, 3, 0), roll = 20, tex = path) 
		self.platforms.append(platform)
		platform = Platform(self.render, self.world, 0, Vec3(10, 7, 0.5), Point3(-34, 3, 3), tex = path)
		self.platforms.append(platform)
		platform = Platform(self.render, self.world, 0, Vec3(10, 7, 0.5), Point3(-46, 3, 4), tex = path)
		self.platforms.append(platform)
		platform = Platform(self.render, self.world, 0, Vec3(10, 7, 0.5), Point3(-58, 3, 5), tex = path)
		self.platforms.append(platform)
	 	
		"""
		x = -2; y = 3; z = -1
		
		heading = 0
		for i in range(6):
			platform = Platform(self.render, self.world, heading, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			self.platforms.append(platform)
			
			if i == 3 or i == 5:
				spinner = Spinner(self.render, self.world, 90, 14, Vec3(2.2, 0.3, 1), Point3(x+9, y+7, z+2))
				self.spinners.append(spinner)	
			
			x -= 12; z += 1.8
		"""
	 	"""
		spinDex = 4 #ehh?? get it??!! spinDex = spin index?!! X-D
		for i in range(3):
			self.spinner = Spinner(self.render, self.world, 90, 14, Vec3(2.2, 0.3, 1), Point3(0, 0, 0))
			self.spinner.spinnerBulletNode.reparentTo(self.platforms[spinDex].platformBulletNode)
			spinDex += 3
		"""

	#def setup

	def setupCoins(self):
		"""
		index = 0
		for i in range(4):
			coin = Coin(self.render, self.world, self.hopper, 10, 0.35, 0.35, Point3(1, 0, 2))
			coin.coinNP.reparentTo(self.platforms[index].platformBulletNode)
			self.coins.append(coin)
			index += 5
		"""
	def resetCoins(self):
		print "Inside coins; NOT removing a coin but initializing list to 0"
		self.coins = []
		self.setupCoins()

	def setupBerries(self):
		"""
		index = 1
		mult = 1
		for i in range(5):
			berry1 = Berry(self.render, self.world, self.hopper, 10*mult, 0.35, 0.35, Point3(0, 0, 2))
			berry1.berryNP.reparentTo(self.platforms[index].platformBulletNode)
			self.berries.append(berry1)
			index += 3
			mult *= -1

			if mult > 0:
				mult *= 2
			else:
				mult /= 2
		"""
	
	def resetBerries(self):
		self.berries = []
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

		for platform in self.platforms:
			platform.removeNormal()

	def destroyLight(self):
		self.render.clearLight(self.dlnp)
		self.render.clearLight(self.alnp)
		self.render.clearLight(self.slnp)
		
		for platform in self.platforms:
			platform.addNormal()

	def destroyWorld(self):
		for platform in self.platforms:
			self.world.removeRigidBody(platform.platformBulletNode.node())
			platform.platformBulletNode.remove_node()
		for spinner in self.spinners:
			self.world.removeRigidBody(spinner.spinnerBulletNode.node())
			spinner.spinnerBulletNode.remove_node()
		for coin in self.coins:
			self.world.removeGhost(coin.ghostNode)
			coin.removeCoin()
		for enemy in self.enemies:
			enemy.enemyNP.remove_node()
		












