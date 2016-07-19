
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
*  Description: This class creates the ocean     *
*               layout as a foundation for the   *
*               game.                            *
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

class Platform(object):
	
	def __init__(self, render, world, heading, sizeMap, originMap, roll = 0, tex = "models/165.jpg"):
		self.render = render
		self.world = world

		self.origin = originMap
		self.size = sizeMap
		self.heading = heading
		self.roll = roll

		shape = BulletBoxShape(self.size*0.55)
		self.platformBulletNode = self.render.attachNewNode(BulletRigidBodyNode("Platform"))
		self.platformBulletNode.node().addShape(shape)
		self.platformBulletNode.setPos(self.origin + self.size)
		self.platformBulletNode.setH(self.heading)
		self.platformBulletNode.setR(self.roll)
		self.platformBulletNode.setCollideMask(BitMask32.allOn())
		
		"""
		self.directionalLight = DirectionalLight( "directionalLight" )
		self.directionalLight.setColor( Vec4( 1, 1, 1, 1 ) )
		self.directionalLight.setDirection(Vec3(0, -0.6, -1))
		self.directionalLightNP = render.attachNewNode(self.directionalLight)
		"""

		#----- Platform Model ------
		self.platformModel = loader.loadModel("models/ModelCollection/EnvBuildingBlocks/stone-cube/stone.egg")
		self.platformModel.reparentTo(self.platformBulletNode)
		self.platformModel.setPos(0, 0, 0)
		self.platformModel.setScale(self.size.x * 1.1, self.size.y * 1.1, self.size.z * 0.625)
		
		#self.platformModel.setLight(self.directionalLightNP)   
		
		self.volcTex = loader.loadTexture(tex)
		self.platformModel.setTexture(self.volcTex, 1)
		
		self.volcNormal = loader.loadTexture("models/165_norm.jpg")
		self.vt = TextureStage('vt')
		self.vt.setMode(TextureStage.MNormal)

		self.platformModel.setTexture(self.volcTex, 1)
		
		self.platformModel.setTexture(self.volcTex, 1)
		
		self.world.attachRigidBody(self.platformBulletNode.node())

	def removeNormal(self):
		#self.platformModel.clearLight(self.directionalLightNP)
		self.platformModel.setTexture(self.volcTex, 1)
		
		pass
	def addNormal(self):
		self.platformModel.setTexture(self.vt, self.volcNormal)















		




