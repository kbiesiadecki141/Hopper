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
*  Description: This class has Hopper functions  *
*               within itself, rather than       *
*               imported from hopper.            *
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
class PlayHopper(ShowBase):
	
	def __init__(self):
		ShowBase.__init__(self)
		base.disableMouse()
		
		#----- Play Music -----
		backgroundMusic = base.loader.loadSfx("backgroundMusic.wav")
		backgroundMusic.play()

		# ITF: Create a setup world class!
		
		#----- Setup Bullet World -----
		self.debugNode = BulletDebugNode("Debug")
		self.debugNode.showWireframe(True)
		self.debugNP = self.render.attachNewNode(self.debugNode)
		self.debugNP.show()

		self.world = BulletWorld()
		self.world.setGravity(Vec3(0, 0, -9.81))
		self.world.setDebugNode(self.debugNP.node())

		#----- Setup Visible World -----
		self.setupWorld()

		#----- Setup Hopper -----
		#self.setupHopper()
		self.hopper = Hopper(self.render, self.world)
		self.hopperWalking = False
		inputState.watchWithModifiers('accelerate', 'arrow_up')
		inputState.watchWithModifiers('turnLeft', 'arrow_left')
		inputState.watchWithModifiers('turnRight', 'arrow_right')
		#self.accept('space', self.doJump)
		self.accept('space', self.hopper.doJump)
		
		#----- Setup Camera -----
		#base.camera.reparentTo(self.hopperModel)
		base.camera.reparentTo(self.hopper.hopperModel)
		base.camera.setPos(0, 50, 70.0)
		base.camera.setH(180)
		#base.camera.lookAt(self.hopperModel)
		base.camera.lookAt(self.hopper.hopperModel)
		
		#----- Update -----
		taskMgr.add(self.update, "update")
	
	def update(self, task):
		self.processInput()
		dt = globalClock.getDt()
		self.world.doPhysics(dt, 10, 1/180.0)
		return task.cont

	def doJump(self):
		self.hopperBulletNode.setMaxJumpHeight(1.0)
		self.hopperBulletNode.setJumpSpeed(7.0)
		self.hopperBulletNode.doJump()

	def processInput(self):
		speed = Vec3(0, 0, 0)
		omega = 0

		if inputState.isSet('turnLeft'):omega = 100; self.hopperWalking = True
		if inputState.isSet('turnRight'):omega = -100; self.hopperWalking = True
		if inputState.isSet('accelerate'): speed.setY(1.5); self.hopperWalking = True
		else: speed.setY(1.0)

		speed *= 10
		#self.hopperBulletNode.setAngularMovement (omega)
		#self.hopperBulletNode.setLinearMovement(speed, True)
		self.hopper.hopperBulletNode.setAngularMovement (omega)
		self.hopper.hopperBulletNode.setLinearMovement(speed, True)

	def setupWorld(self):
		oceanShape = BulletPlaneShape(Vec3(0, 0, 1), 0)
		oceanBulletNode = BulletRigidBodyNode("Ocean")
		oceanBulletNode.addShape(oceanShape)
		oceanNP = self.render.attachNewNode(oceanBulletNode)
		oceanNP.setPos(0, 0, 0)
		self.world.attachRigidBody(oceanBulletNode)
		oceanModel = self.loader.loadModel("models/square")
		oceanModel.setScale(1000, 1000, 1)
		oceanModel.setPos(0, 0, 0)
		seaTexture = loader.loadTexture("models/Sargasso-sea.png")
		#seaTexture = loader.loadTexture("models/smallWavesMovie.avi")
		#seaTexture.setWrapU(Texture.WM_repeat)
		#seaTexture.setWrapV(Texture.WM_repeat)
		oceanModel.setTexture(seaTexture, 1)
		oceanModel.setTexScale(TextureStage.getDefault(), 50, 50)
		oceanModel.reparentTo(oceanNP)  #error?
	
	def setupHopper(self):
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

game = PlayHopper()
game.run()

















