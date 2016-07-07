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
	
	def __init__(self, render, world, theLoader):
		self.render = render
		self.world = world
		self.loader = theLoader
		
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






