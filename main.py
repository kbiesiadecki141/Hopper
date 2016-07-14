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
*  Description: This class runs the complete     *
*               game of Hopper!                  *
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

import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from hopper import Hopper
from oceanWorld import Ocean
from platform import Platform
from coin import Coin

from level1 import PlayHopper

def level1():
	game = PlayHopper()
	pass
b = DirectButton(text = ("Play Level 1", "Play Level 1", "Play Level 1", "disabled"), scale = .05, command = level1)
b.resetFrameSize()

run()














