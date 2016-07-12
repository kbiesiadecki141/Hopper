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

class Hopper(object):
	
	def __init__(self, render, world, base):
		self.render = render
		self.world = world
		self.base = base

		self.jumpEffect = self.base.loader.loadSfx("jump.wav")
		self.jumpEffect.setVolume(0.5) 

		#-- Health --
		#frame = DirectFrame(frameSize = (-1,2.5,-0.2,1),frameColor = (0, 0, 0, 0.5), pos = (-1, 1, 1))
		self.health = DirectWaitBar(text = "", value = 100, range = 100, pos = (-0.85, 0.93, 0.93), scale = 0.4)
		healthText = OnscreenText(text = "Health", parent = self.health, pos = (-0.77, -0.23, -0.23), bg = (0,0,0,1), fg = (1,1,1,1), scale = 0.15)
		#--ITF: add black frame around wait bar---
		
		h = 1.75
		w = 0.4
		hopperShape = BulletCapsuleShape(w, h - 2 * w, ZUp)

		self.hopperBulletNode = BulletCharacterControllerNode(hopperShape, 0.4, "Hopper")
		self.hopperNP = self.render.attachNewNode(self.hopperBulletNode)
		self.hopperNP.setPos(10, 10, 1)
		self.hopperNP.setH(90)
		self.hopperNP.setCollideMask(BitMask32.allOn())
		self.world.attachCharacter(self.hopperBulletNode)

		self.hopperModel = Actor("models/ralph/ralph.egg", {
				 'run' : 'models/ralph/ralph-run.egg',
				 'walk' : 'models/ralph/ralph-walk.egg',
				 'jump' : 'models/ralph/ralph-jump.egg'})

		self.hopperModel.reparentTo(self.hopperNP)
		self.hopperModel.setScale(0.3048)
		self.hopperModel.setH(180)
		self.hopperModel.setPos(0, 0, -1)
		self.hopperModel.loop("walk")

	def doJump(self):
		self.hopperBulletNode.setMaxJumpHeight(1.0)
		self.hopperBulletNode.setJumpSpeed(6.0)
		self.hopperBulletNode.doJump()
		self.jumpEffect.play()
		animationSequence = Sequence(Func(self.playJump), Wait(0.6), Func(self.loopWalking))
		animationSequence.start()

	def loopWalking(self):
		self.hopperModel.loop("walk")
	
	def playJump(self):
		self.hopperModel.play("jump")

	def loopRunning(self):
		self.hopperModel.loop("run")

	def getNode(self):
		return self.hopperNP.node()

	def boostHealth(self, boostVal):
		if (self.health['value'] + boostVal) <= 100:
			self.health['value'] += boostVal
		else:
			self.health['value'] = 100

	def lowerHealth(self, damage):
		if (self.health['value'] + damage) >= 0:
			self.health['value'] -= damage
		else:
			self.health['value'] = 0

	def resetHealth(self):
		self.health['value'] = 100






