
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
	
	def __init__(self, render, world, sizeMap, originMap):
		self.render = render
		self.world = world

		self.origin = originMap
		self.size = sizeMap
		
		shape = BulletBoxShape(self.size*0.55) #ITF: Change size*0.55
		platformBulletNode = self.render.attachNewNode(BulletRigidBodyNode("Platform"))
		platformBulletNode.node().addShape(shape)
		platformBulletNode.setPos(self.origin + self.size)
		platformBulletNode.setCollideMask(BitMask32.allOn())

		platformModel = loader.loadModel("models/ModelCollection/EnvBuildingBlocks/stone-cube/stone.egg")
		platformModel.reparentTo(platformBulletNode)
		platformModel.setPos(0, 0, 0)
		platformModel.setScale(self.size.x * 1.1, self.size.y * 1.1, self.size.z * 0.625)
		self.world.attachRigidBody(platformBulletNode.node())

















		




