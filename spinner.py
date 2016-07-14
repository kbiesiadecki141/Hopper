
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

class Spinner(object):
	
	def __init__(self, render, world, heading, speed, sizeMap, originMap):
		self.render = render
		self.world = world

		self.origin = originMap
		self.size = sizeMap
		self.heading = heading
		self.speed = speed

		shape = BulletBoxShape(self.size)
		self.spinnerBulletNode = self.render.attachNewNode(BulletRigidBodyNode("Spinner"))
		self.spinnerBulletNode.node().addShape(shape)
		self.spinnerBulletNode.setPos(self.origin.x, self.origin.y, self.origin.z)
		self.spinnerBulletNode.setH(self.heading)
		self.spinnerBulletNode.setCollideMask(BitMask32.allOn())
		self.spinnerBulletNode.reparentTo(self.render)

		self.spinnerModel = loader.loadModel("models/ModelCollection/EnvBuildingBlocks/spinner/spinner.egg")
		self.spinnerModel.reparentTo(self.spinnerBulletNode)
		self.spinnerModel.setPos(0, 0, -1)
		self.spinnerModel.setScale(0.2, 0.5, 0.05)
		self.spinnerModel.setColorScale(0, 0.5, 1, 1)
		self.world.attachRigidBody(self.spinnerBulletNode.node())

	def spin(self, task):
		theta = task.time * self.speed
		self.spinnerBulletNode.setH(theta)
		return task.cont















		




