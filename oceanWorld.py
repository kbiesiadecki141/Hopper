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

class Ocean(object):
	
	def __init__(self, render, world, theLoader, hopper):
		self.render = render
		self.world = world
		self.loader = theLoader
		self.hopper = hopper
		
		self.waterMap = []

		self.worldsize = 50
		self.seaTex = self.loader.loadTexture('models/water.png')

		x = 0
		self.setupOcean(False, -50, 5)
		self.setupOcean(False, 50, 5)
		self.setupOcean(True, -50, 5)
		self.setupOcean(True, 50, 5)
		oceanShape = BulletPlaneShape(Vec3(0, 0, 1), 0)
		oceanBulletNode = BulletRigidBodyNode("Ocean")
		oceanBulletNode.addShape(oceanShape)
		
		oceanNP = self.render.attachNewNode(oceanBulletNode)
		oceanNP.setPos(0, 0, -10)
		self.world.attachRigidBody(oceanBulletNode)

	def setupOcean(self, isDiag, val, repeat):
		x = 0
		y = 0
		z = 0
		for j in range(repeat):
			for i in range(repeat):
				self.water = self.loader.loadModel('models/square.egg')
				self.water.setSx(self.worldsize*2)
				self.water.setSy(self.worldsize*2)
				self.water.setPos(x,y,z)
				self.water.setTransparency(TransparencyAttrib.MAlpha)
				self.water.setAlphaScale(1)
				newTS = TextureStage('1')
				self.water.setTexture(newTS, self.seaTex)
				self.water.setTexScale(newTS,4)
				self.water.setColorScale(0, 1, 1, 1)
				self.water.reparentTo(self.render)
				LerpTexOffsetInterval(self.water,200,(20,0),(0,0), textureStage=newTS).loop()
				if isDiag:
					x -= val
				else:
					x += val

				self.waterMap.append(self.water)
			x = 0
			y += val
		"""	
		alight = AmbientLight('alight')
		alight.setColor(VBase4(0.5, 0.5, 1.0, 1.0))
		alnp  = self.render.attachNewNode(alight)
		self.water.setLight(alnp)
		"""






		




