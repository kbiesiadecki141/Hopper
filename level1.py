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

#import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from hopper import Hopper
from oceanWorld import Ocean
from platform import Platform
from coin import Coin
from level1World import Level1World
class PlayHopper(ShowBase):
	
	def __init__(self):
		ShowBase.__init__(self)
		#----- Setup Bullet World -----
		self.debugNode = BulletDebugNode("Debug")
		self.debugNode.showWireframe(True)
		self.debugNP = self.render.attachNewNode(self.debugNode)
		#self.debugNP.show()

		self.bulletWorld = BulletWorld()
		self.bulletWorld.setGravity(Vec3(0, 0, -9.81))
		self.bulletWorld.setDebugNode(self.debugNP.node())
		
		#----- State Variables -----
		self.isHelping = False
		self.amount = 0
		self.isLit = False
		#----- Setup/Manipulate Hopper -----

		self.hopper = Hopper(self.render, self.bulletWorld, base)
		self.world = Level1World(self.render, self.loader, base, self.bulletWorld, self.hopper) 
		#self.freeze = False
		self.accept('space', self.hopper.doJump)
		self.accept('arrow_up', self.hopper.loopRunning)
		self.accept('arrow_up-up', self.hopper.loopWalking)
		self.accept('arrow_right', self.hopper.loopWalking)
		self.accept('arrow_left', self.hopper.loopWalking)
		self.accept('h', self.toggleHelp)
		self.accept('l', self.toggleLight)
		
		self.isFatiguing = True
		
		#----- Update -----
		taskMgr.add(self.world.update, "update")
		taskMgr.doMethodLater(3, self.fatigue, "fatigue", uponDeath = self.die)
		taskMgr.add(self.world.simulateWater, "simulateWater", uponDeath = self.fail)
		taskMgr.add(self.detectCollisionForGhosts, "detectCoinCollision", extraArgs = [self.world.coin], appendTask = True, uponDeath = self.world.coin.collectCoin)
		taskMgr.add(self.detectCollisionForGhosts, "detectEndCoinCollision", extraArgs = [self.world.endToken], appendTask = True, uponDeath = self.levelClear)
		
	def fatigue(self, task):
		self.hopper.lowerHealth(2)
		if self.hopper.getHealth() == 0:
			self.isFatiguing = False
			return task.done
		else:
			self.isFatiguing = True
			return task.again

	def displayWallet(self):
		#---ITF: beautify this ----
		self.wallet = OnscreenText(text = "Wallet: "+str(self.amount), pos = (-1.1, -0.9), bg = (1, 1, 1, 1), align = TextNode.ACenter, mayChange = True)

	def detectCollisionForGhosts(self, coin, task):
		# contactTestPair returns a BulletContactResult object
		contactResult = self.bulletWorld.contactTestPair(self.hopper.getNode(), coin.ghostNode) 
		if len(contactResult.getContacts()) > 0:
			print "Hopper is in contact with: ", coin.ghostNode.getName()
			self.amount += coin.coinValue
			self.displayWallet()
			return task.done
		else:
			return task.cont
	
	def reset(self):
		self.c.destroy()
		self.hopper.hopperNP.setPos(10, 10, 1)
		self.hopper.hopperNP.setH(90)
		self.hopper.resetHealth()
		self.hopper.loopWalking()
		self.world.coin.coinNP = self.render.attachNewNode(self.world.coin.ghostNode)
		self.world.backgroundMusic.play()
		self.world.failSound.stop()
		self.world.freeze = False
		self.amount = 0
		self.displayWallet()
		taskMgr.add(self.world.simulateWater, "simulateWater", uponDeath = self.fail)
		taskMgr.add(self.detectCollisionForGhosts, "detectCoinCollision", extraArgs = [self.world.coin], appendTask = True, uponDeath = self.world.coin.collectCoin)
		taskMgr.add(self.detectCollisionForGhosts, "detectEndCoinCollision", extraArgs = [self.world.endToken], appendTask = True, uponDeath = self.levelClear)
	
	def replay(self):
		self.q.destroy()
		self.b.destroy()
		self.hopper.hopperNP.setPos(10, 10, 1)
		self.hopper.hopperNP.setH(90)
		self.hopper.resetHealth()
		self.hopper.loopWalking()
		self.world.coin.coinNP = self.render.attachNewNode(self.world.coin.ghostNode)
		self.world.backgroundMusic.play()
		self.world.failSound.stop()
		self.world.freeze = False
		self.amount = 0
		self.displayWallet()
		taskMgr.add(self.world.simulateWater, "simulateWater", uponDeath = self.fail)
		taskMgr.add(self.detectCollisionForGhosts, "detectCoinCollision", extraArgs = [self.world.coin], appendTask = True, uponDeath = self.world.coin.collectCoin)
		taskMgr.add(self.detectCollisionForGhosts, "detectEndCoinCollision", extraArgs = [self.world.endToken], appendTask = True, uponDeath = self.levelClear)
	
	def levelClear(self, task):
		#Hooray! Level 2 unlocked
		#Menu options:
		# - Main Menu
		# - Quit
		# - Play Again
		# - Next Level
		self.world.freeze = True	
		self.q = DirectButton(text = ("Quit", "Quit", "Quit", "disabled"), scale = .08, pos = (0, 0, -0.2), command = self.quit)
		self.q.resetFrameSize()
	 	self.b = DirectButton(text = ("Restart Level", "Restart Level", "Restart Level", "disabled"), scale = .08, pos = (0, 0, -0.3) , command = self.replay)
		self.b.resetFrameSize()

	def quit(self):
		sys.exit()	
	
	def fail(self, task):
		self.world.freeze = True
		self.world.backgroundMusic.stop()
		self.world.failSound.play()
		self.c = DirectButton(text = ("Restart Level", "Restart Level", "Restart Level", "disabled"), scale = .08, pos = (0, 0, 0) , command = self.reset)
		self.c.resetFrameSize()
	
	def die(self, task):
		self.world.freeze = True
		self.world.backgroundMusic.stop()
		self.world.failSound.play()
		taskMgr.doMethodLater(0.5, self.fatigue, "fatigue", uponDeath = self.fail)
		self.c = DirectButton(text = ("Restart Level", "Restart Level", "Restart Level", "disabled"), scale = .08, pos = (0, 0, 0) , command = self.reset)
		self.c.resetFrameSize()
	
	def getHelp(self):
		self.walk = self.addInstructions(0.7, "[Up Arrow]: ")
	
	def destroyHelp(self):
		self.walk.destroy()

	def addInstructions(self, pos, msg):
		return OnscreenText(text = msg, style = 1, fg = (1, 1, 1, 1), pos = (0, pos), align= TextNode.ACenter, scale = .05)

	def toggleHelp(self):
		if self.isHelping == False:
			self.getHelp()
			self.isHelping = True
		else:
			self.destroyHelp()
			self.isHelping = False
			
	def toggleLight(self):
		if self.isLit == False:
			self.world.freeze = True
			self.world.addLight()
			self.isLit = True
			unfreezeSeq = Sequence(Wait(2.0), Func(self.world.unfreeze))
			unfreezeSeq.start()
		else:
			self.world.destroyLight()
			self.isLit = False
game = PlayHopper()
game.run()

















