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

class Hopper(object):
	
	def __init__(self, render, world):
		self.render = render
		self.world = world
		h = 1.75
		w = 0.4
		hopperShape = BulletCapsuleShape(w, h - 2 * w, ZUp)

		self.hopperBulletNode = BulletCharacterControllerNode(hopperShape, 0.4, "Hopper")
		self.hopperNP = self.render.attachNewNode(self.hopperBulletNode)
		self.hopperNP.setPos(10, 10, 1)
		self.hopperNP.setH(45)
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
		self.hopperBulletNode.setJumpSpeed(4.0)
		self.hopperBulletNode.doJump()
		animationSequence = Sequence(Func(self.playJump), Wait(0.6), Func(self.loopWalking))
		animationSequence.start()

	def loopWalking(self):
		self.hopperModel.loop("walk")
	
	def playJump(self):
		self.hopperModel.play("jump")

	def loopRunning(self):
		self.hopperModel.loop("run")
