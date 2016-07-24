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
from pandac.PandaModules import CollisionHandlerEvent, CollisionNode, CollisionSphere, CollisionTraverser, BitMask32, CollisionRay

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText

class Enemy(object):
	
	def __init__(self, render, world, base, originMap, hopper, idNum, strength = 1, size = 1.2):
		self.render = render
		self.world = world
		self.base = base
		self.originMap = originMap
		self.hopper = hopper
		self.idNum = idNum
		self.strength = strength 
		self.size = size
	
		self.volume = 1
		self.turned = False
		self.isAttacking = False
		self.mult = 1

		self.attackSound = self.base.loader.loadSfx("sounds/bloodSquirt.mp3")
		self.attackSound.setVolume(1) 
		self.damageSound = self.base.loader.loadSfx("sounds/swordSlash.mp3")
		self.damageSound.setVolume(0.5) 

		self.freeze = False

		#----- Setup Enemy -----
		h = 2.75
		w = self.size + 0.2
		
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
		self.enemyModel.setScale(0.42 * self.size)
		self.enemyModel.setH(180)
		self.enemyModel.setPos(0, 0, 1)
		self.enemyModel.loop("idle")
		#self.setupPoison()

		self.enemyCollider = self.enemyModel.attachNewNode(CollisionNode('enemyNode'))
		self.enemyCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
		self.enemyCollider.setTag("id", str(self.idNum))
	
	def setupPoison(self):
		shape = BulletSphereShape(2)
		node = BulletRigidBodyNode('Poison')
		node.setMass(10.0)
		node.addShape(shape)
		self.sphere = self.render.attachNewNode(node)
		self.sphere.setPos(0, 0, 50)
		self.world.attachRigidBody(node)

		smileyFace = self.loader.loadModel("models/smiley")
		smileyFace.reparentTo(self.sphere)
		smileyFace.setScale(2)
		
		self.poison = loader.loadModel("smiley")
		self.poison.reparentTo(self.enemyModel)
		self.poison.setColor(1, 1, 1)
		self.poison.setPos(2.2, 2.5, -1.7)
		self.poison.setScale(0.3)

	def pace(self):
		speed = Vec3(1.1*self.mult, 0, 0)
		omega = 0
		
		if self.enemyNP.getY() > 1 and self.turned == False:
			self.mult *= -1
			self.turned = True
		
		if self.enemyNP.getY() < -1 and self.turned:
			self.mult *= -1
			self.turned = False

		self.enemyBulletNode.setAngularMovement (omega)
		self.enemyBulletNode.setLinearMovement(speed, True)

		self.enemyModel.lookAt(self.hopper.hopperModel)
	
	def square(self):
		speed = Vec3(1.1*self.mult, 0, 0)
		omega = 0
		
		if self.enemyNP.getY() > 1 and self.turnedLeft == False:
			self.mult *= -1
			self.turnedLeft = True
		
		if self.enemyNP.getY() < -1 and self.turnedLeft:
			self.mult *= -1
			#self.turnedLeft = dwendw setheading to getHeading + 90

		self.enemyBulletNode.setAngularMovement (omega)
		self.enemyBulletNode.setLinearMovement(speed, True)

		self.enemyModel.lookAt(self.hopper.hopperModel)

	def lowerHealth(self):
		if self.strength == 0:
			self.enemyNP.remove_node()
		else:
			self.strength -= 1
		self.playAttack()
		self.damageSound.play()
	
	def setVolume(self, volume):
		self.volume = volume

	def attack(self):
		if self.isAttacking == False:
			self.attackSound.play()
			self.loopAttack()
			self.isAttacking = True
	
	def shootPoison(self, posMap):
		self.trajectory = ProjectileInterval(self.poison, startPos = Point3(0, 0, 0),
								endPos = posMap,
								duration = 1)
		self.trajectory.play()
		self.hopper.lowerHealth(-5)
		

	def getHealth(self):
		return self.strength

	def playAttack(self):
		self.enemyModel.setPlayRate(2.0, "attackLR")
		self.enemyModel.play("attackLR")
	
	def loopAttack(self):
		self.enemyModel.setPlayRate(2.0, "attackLR")
		self.enemyModel.loop("attackLR")

	def stand(self):
		self.enemyModel.loop("idle")
	
	def getNode(self):
		return self.enemyNP.node()
	
	def stopSound(self):
		self.attackSound.stop()

