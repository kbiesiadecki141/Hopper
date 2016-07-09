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
		backgroundMusic = base.loader.loadSfx("backgroundMusic.wav")
		#backgroundMusic.play()

		#----- Setup Bullet World -----
		self.debugNode = BulletDebugNode("Debug")
		self.debugNode.showWireframe(True)
		self.debugNP = self.render.attachNewNode(self.debugNode)
		#self.debugNP.show()

		self.world = BulletWorld()
		self.world.setGravity(Vec3(0, 0, -9.81))
		self.world.setDebugNode(self.debugNP.node())

		#----- Setup/Manipulate Hopper -----
		self.hopper = Hopper(self.render, self.world, base)
		inputState.watchWithModifiers('accelerate', 'arrow_up')
		inputState.watchWithModifiers('turnLeft', 'arrow_left')
		inputState.watchWithModifiers('turnRight', 'arrow_right')
		self.accept('space', self.hopper.doJump)
		self.accept('arrow_up', self.hopper.loopRunning)
		self.accept('arrow_up-up', self.hopper.loopWalking)
		self.accept('arrow_right', self.hopper.loopWalking)
		self.accept('arrow_left', self.hopper.loopWalking)
		
		#----- Setup Visible World -----
		ocean = Ocean(self.render, self.world, self.loader)
		
		x = -2; y = 3; z = 0
		for i in range(10):
			Platform(self.render, self.world, Vec3(9, 7, 0.5), Point3(x, y, z)) 
			x -= 12
			z += 2

		self.coin = Coin(self.render, self.world, self.hopper) #ITF: broaden Coin class
		
		#----- Setup Camera -----
		base.camera.reparentTo(self.hopper.hopperModel)
		base.camera.setPos(0, 50, 50.0)
		base.camera.setH(180)
		base.camera.lookAt(self.hopper.hopperModel)
		
		#----- Update -----
		taskMgr.add(self.update, "update")
		taskMgr.add(self.coin.detectCollisionForGhosts, "detectCoinCollision", uponDeath = self.collectCoin)
		
	def update(self, task):
		self.processInput()
		dt = globalClock.getDt()
		self.world.doPhysics(dt, 10, 1/180.0)
		return task.cont

	def processInput(self):
		speed = Vec3(0, 0, 0)
		omega = 0

		if inputState.isSet('turnLeft'):   omega = 100
		if inputState.isSet('turnRight'):  omega = -100
		if inputState.isSet('accelerate'): speed.setY(0.6)
		#temporarily disabled!!! do not forget to undo! This includes the speed above!
		#else: speed.setY(0.5)

		speed *= 10
		self.hopper.hopperBulletNode.setAngularMovement (omega)
		self.hopper.hopperBulletNode.setLinearMovement(speed, True)
	
	def collectCoin(self, task):
		chaChing = base.loader.loadSfx("coinCollect.wav")
		chaChing.setVolume(1)
		chaChing.play()
		self.coin.removeCoin()

game = PlayHopper()
game.run()

















