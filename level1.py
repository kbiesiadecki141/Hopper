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

class PlayHopper(ShowBase):
	
	def __init__(self):
		ShowBase.__init__(self)
		base.disableMouse()
		
		#----- Play Music -----
		self.backgroundMusic = base.loader.loadSfx("backgroundMusic.wav")
		self.backgroundMusic.play()
		self.failSound = base.loader.loadSfx("fail.wav")

		#----- Setup Bullet World -----
		self.debugNode = BulletDebugNode("Debug")
		self.debugNode.showWireframe(True)
		self.debugNP = self.render.attachNewNode(self.debugNode)
		self.debugNP.show()

		self.world = BulletWorld()
		self.world.setGravity(Vec3(0, 0, -9.81))
		self.world.setDebugNode(self.debugNP.node())

		#----- Setup/Manipulate Hopper -----
		self.hopper = Hopper(self.render, self.world, base)
		self.freeze = False
		inputState.watchWithModifiers('accelerate', 'arrow_up')
		inputState.watchWithModifiers('turnLeft', 'arrow_left')
		inputState.watchWithModifiers('turnRight', 'arrow_right')
		self.accept('space', self.hopper.doJump)
		self.accept('arrow_up', self.hopper.loopRunning)
		self.accept('arrow_up-up', self.hopper.loopWalking)
		self.accept('arrow_right', self.hopper.loopWalking)
		self.accept('arrow_left', self.hopper.loopWalking)
		
		#----- Setup Visible World -----
		ocean = Ocean(self.render, self.world, self.loader, self.hopper)
		
		x = -2; y = 3; z = 0
		for i in range(10):
			Platform(self.render, self.world, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			x -= 12
			z += 2

		self.coin = Coin(self.render, self.world, self.hopper, 10, 0.35, 0.35, Vec3(3, 10, 3)) #ITF: broaden Coin class
		#self.endToken = Coin(self.render, self.world, self.hopper, 0.6, 0.6, Vec3(3, 20, 5))

		#-----  Misc. -----
		self.amount = 0

		#----- Setup Camera -----
		base.camera.reparentTo(self.hopper.hopperModel)
		
		base.camera.setPos(0, 50, 50)#150.0)
		base.camera.setH(180)
		base.camera.lookAt(self.hopper.hopperModel)
		
		#----- Update -----
		taskMgr.add(self.update, "update")
		taskMgr.add(self.simulateWater, "simulateWater", uponDeath = self.fail)
		taskMgr.add(self.detectCollisionForGhosts, "detectCoinCollision", extraArgs = [self.coin], appendTask = True, uponDeath = self.coin.collectCoin)
		#taskMgr.add(self.detectCollisionForGhosts, "detectEndCoinCollision", uponDeath = self.coin.collectCoin)
		
	def update(self, task):
		self.processInput()
		self.displayWallet()
		dt = globalClock.getDt()
		self.world.doPhysics(dt, 10, 1/180.0)
		return task.cont

	def processInput(self):
		speed = Vec3(0, 0, 0)
		omega = 0
		
		if self.freeze == False:
			if inputState.isSet('turnLeft'):   omega = 100
			if inputState.isSet('turnRight'):  omega = -100
			if inputState.isSet('accelerate'): speed.setY(0.6)
			#temporarily disabled!!! do not forget to undo! This includes the speed above!
			else: speed.setY(0.5)
		
		speed *= 10
		self.hopper.hopperBulletNode.setAngularMovement (omega)
		self.hopper.hopperBulletNode.setLinearMovement(speed, True)

	def displayWallet(self):
		self.wallet = OnscreenText(text = "Wallet: "+str(self.amount), pos = (-1.1, -0.9), bg = (1, 1, 1, 1), align = TextNode.ALeft)

	def detectCollisionForGhosts(self, coin, task):
		# contactTestPair returns a BulletContactResult object
		contactResult = self.world.contactTestPair(self.hopper.getNode(), coin.ghostNode) 
		if len(contactResult.getContacts()) > 0:
			print "Hopper is in contact with: ", coin.ghostNode.getName()
			self.amount += coin.coinValue
			self.wallet.destroy()
			return task.done
		else:
			return task.cont
	
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

	def reset(self):
		self.b.destroy()
		self.hopper.hopperNP.setPos(10, 10, 1)
		self.hopper.hopperNP.setH(90)
		self.coin.coinNP = self.render.attachNewNode(self.coin.ghostNode)
		self.backgroundMusic.play()
		self.failSound.stop()
		self.freeze = False
		taskMgr.add(self.simulateWater, "simulateWater", uponDeath = self.fail)
		taskMgr.add(self.coin.detectCollisionForGhosts, "detectCoinCollision", uponDeath = self.coin.collectCoin)

	def fail(self, task):
		self.backgroundMusic.stop()
		self.failSound.play()
		self.b = DirectButton(text = ("Restart Level", "Restart Level", "Restart Level", "disabled"), scale = .05, command = self.reset)
		self.b.resetFrameSize()


game = PlayHopper()
game.run()

















