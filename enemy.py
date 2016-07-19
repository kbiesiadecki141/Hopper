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
*  Description: ~fill me in~                     *
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
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText

class Enemy(object):
	
	def __init__(self, render, world, base, originMap):
		self.render = render
		self.world = world
		self.base = base
		self.originMap = originMap

		self.jumpEffect = self.base.loader.loadSfx("sounds/jump.wav")
		self.jumpEffect.setVolume(0.5) 

		self.freeze = False
		
		h = 1.75
		w = 0.4
		
		enemyShape = BulletCapsuleShape(w, h - 2 * w, ZUp)

		self.enemyBulletNode = BulletCharacterControllerNode(enemyShape, 0.4, "Enemy")
		self.enemyNP = self.render.attachNewNode(self.enemyBulletNode)
		self.enemyNP.setPos(originMap)
		self.enemyNP.setH(90)
		self.enemyNP.setCollideMask(BitMask32.allOn())
		self.world.attachCharacter(self.enemyBulletNode)

		self.enemyModel = Actor("models/art/monster/bvw-f2004--monster/monster1.egg", {
				 'idle' : 'models/art/monster/bvw-f2004--monster/monster1-idle.egg',
				 'explode' : 'models/art/monster/bvw-f2004--monster/monster1-explode.egg',
				 'attackL' : 'models/art/monster/bvw-f2004--monster/monster1-pincer-attack-left.egg',
				 'attackR' : 'models/art/monster/bvw-f2004--monster/monster1-pincer-attack-right.egg',
				 'attackT' : 'models/art/monster/bvw-f2004--monster/monster1-tentacle-attack.egg',
				 'attackLR' : 'models/art/monster/bvw-f2004--monster/monster1-pincer-attack-both.egg'})

		self.enemyModel.reparentTo(self.enemyNP)
		self.enemyModel.setScale(0.3048)
		self.enemyModel.setH(180)
		self.enemyModel.setPos(0, 0, 1)
		self.enemyModel.loop("idle")

	def processInput(self):
		speed = Vec3(0, 0, 0)
		omega = 0
		
		if self.freeze == False:
			if inputState.isSet('turnLeft'):   omega = 100
			if inputState.isSet('turnRight'):  omega = -100
			if inputState.isSet('accelerate'): speed.setY(0.85)
			#temporarily disabled!!! do not forget to undo! This includes the speed above!
			#else: speed.setY(0.6)
		else:
			self.stand()
		
		speed *= 10
		self.enemyBulletNode.setAngularMovement (omega)
		self.enemyBulletNode.setLinearMovement(speed, True)

	def doJump(self):
		self.enemyBulletNode.setMaxJumpHeight(1.0)
		self.enemyBulletNode.setJumpSpeed(6.0)
		self.enemyBulletNode.doJump()
		self.jumpEffect.play()
		animationSequence = Sequence(Func(self.playJump), Wait(0.6), Func(self.loopWalking))
		animationSequence.start()

	def loopWalking(self):
		self.enemyModel.loop("walk")
	
	def playJump(self):
		self.enemyModel.play("jump")

	def loopRunning(self):
		self.enemyModel.loop("run")
	
	def stand(self):
		self.enemyModel.pose("walk", 6)
	
	def unfreeze(self):
		self.freeze = False
		self.loopWalking()

	def getNode(self):
		return self.enemyNP.node()

	#----- Implement later -----
	"""
	def boostHealth(self, boostVal):
		if (self.health['value'] + boostVal) <= 100:
			self.health['value'] += boostVal
		else:
			self.health['value'] = 100

	def lowerHealth(self, damage):
		if (self.health['value'] + damage) >= 0:
			self.health['value'] += damage
		else:
			self.health['value'] = 0

	def resetHealth(self):
		self.health['value'] = 100

	def getHealth(self):
		return self.health['value']
	
	def setHealth(self, val):
		self.health['value'] = val
	"""




