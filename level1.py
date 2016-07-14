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

		self.bulletWorld = BulletWorld()
		self.bulletWorld.setGravity(Vec3(0, 0, -9.81))
		self.bulletWorld.setDebugNode(self.debugNP.node())
	
		#----- Setup Buttons ------
		self.buttonMap = []

		#----- State Variables -----
		self.isHelping = False
		self.isDebugging = False
		self.isLit = False
		self.amount = 0
		self.isFatiguing = True
	
		#----- Setup/Manipulate Hopper -----
		self.hopper = Hopper(self.render, self.bulletWorld, base)
		self.accept('space', self.hopper.doJump)
		self.accept('arrow_up', self.hopper.loopRunning)
		self.accept('arrow_up-up', self.hopper.loopWalking)
		self.accept('arrow_right', self.hopper.loopWalking)
		self.accept('arrow_left', self.hopper.loopWalking)
		self.accept('h', self.toggleHelp)
		self.accept('l', self.toggleLight)
		self.accept('b', self.toggleDebug)

		#----- Setup World -----
		self.world = Level1World(self.render, self.loader, base, self.bulletWorld, self.hopper) 
		
		#----- Tasks -----
		taskMgr.add(self.world.update, "update")
		taskMgr.doMethodLater(2.5, self.fatigue, "fatigue", uponDeath = self.fail)
		taskMgr.add(self.world.simulateWater, "simulateWater", uponDeath = self.fail)
		
		for spinner in self.world.spinners:
			taskMgr.add(spinner.spin, "spinnerTask")
		
		taskMgr.add(self.detectCollisionForGhosts, "detectEndCoinCollision", extraArgs = [self.world.endToken], appendTask = True, uponDeath = self.levelClear)
		for berry in self.world.berries:
			taskMgr.add(berry.spinBerry, "spinBerry")
			taskMgr.add(self.detectCollisionForGhosts, "detectBerryCollision", extraArgs = [berry], appendTask = True, uponDeath = berry.collectBerry)
		
		for coin in self.world.coins:
			taskMgr.add(self.detectCollisionForGhosts, "detectCoinCollision", extraArgs = [coin], appendTask = True, uponDeath = coin.collectCoin)
			
	#----- Hopper Functions -----
	def fatigue(self, task):
		if self.hopper.getHealth() > 0:
			self.hopper.lowerHealth(-8)
		
		if self.hopper.getHealth() == 0:
			self.isFatiguing = False
			return task.done
		else:
			print self.hopper.getHealth()
			self.isFatiguing = True
			return task.again

	def displayWallet(self):
		#---ITF: beautify this ----
		self.wallet = OnscreenText(text = "Wallet: "+str(self.amount), pos = (-1.1, -0.9), bg = (1, 1, 1, 1), align = TextNode.ACenter, mayChange = True)

	#----- Item Functions -----
	def detectCollisionForGhosts(self, item, task):
		# contactTestPair returns a BulletContactResult object
		contactResult = self.bulletWorld.contactTestPair(self.hopper.getNode(), item.ghostNode) 
		if len(contactResult.getContacts()) > 0:
			print "Hopper is in contact with: ", item.ghostNode.getName()
			if task.name == "detectCoinCollision":
				item.setVolume(1)
				self.amount += item.coinValue
				self.displayWallet()
			elif task.name == "detectBerryCollision":
				item.setVolume(1)
				if item.berryValue > 0:
					self.hopper.boostHealth(item.berryValue)
				else:
					self.hopper.lowerHealth(item.berryValue)
			return task.done
		else:
			return task.cont

	#----- Replay Functions -----	
	def reset(self):
		print "Resetting Level 1"

		for button in self.buttonMap:
			button.destroy()
		
		self.hopper.hopperNP.setPos(8, 10, 1)
		self.hopper.hopperNP.setH(90)
		if self.isFatiguing == False: 
			taskMgr.doMethodLater(3, self.fatigue, "fatigue", uponDeath = self.fail)
		self.hopper.resetHealth()
		self.hopper.loopWalking()
		
		self.world.backgroundMusic.play()
		self.world.failSound.stop()
		self.hopper.freeze = False
		
		"""
		self.world.resetCoins()
		self.world.resetBerries()
		for coin in self.world.coins:
			coin.setVolume(0)
			taskMgr.remove("detectCoinCollision")
			taskMgr.add(self.detectCollisionForGhosts, "detectCoinCollision", extraArgs = [coin], appendTask = True, uponDeath = coin.collectCoin)
	
		for berry in self.world.berries:
			berry.setVolume(0)
			taskMgr.add(berry.spinBerry, "spinBerry")
			taskMgr.remove("detectBerryCollision")
			taskMgr.add(self.detectCollisionForGhosts, "detectBerryCollision", extraArgs = [berry], appendTask = True, uponDeath = berry.collectBerry)
		
		"""
		taskMgr.add(self.detectCollisionForGhosts, "detectEndCoinCollision", extraArgs = [self.world.endToken], appendTask = True, uponDeath = self.levelClear)
		
		taskMgr.add(self.world.simulateWater, "simulateWater", uponDeath = self.fail)
		
		#self.amount = 0
		self.displayWallet()
	
	def levelClear(self, task):
		#Hooray! Level 2 unlocked
		#Menu options:
		# - Main Menu
		# - Quit
		# - Play Again
		# - Next Level
		self.world.backgroundMusic.stop()
		winSound = base.loader.loadSfx("sounds/jennyWin.m4a")
		winSound.play()

		self.hopper.freeze = True	
		self.hopper.setHealth(-1)
		self.q = DirectButton(text = ("Quit", "Quit", "Quit", "disabled"), scale = .08, pos = (0, 0, -0.2), command = self.quit)
		self.q.resetFrameSize()
	 	self.b = DirectButton(text = ("Restart Level", "Restart Level", "Restart Level", "disabled"), scale = .08, pos = (0, 0, -0.3) , command = self.reset)
		self.b.resetFrameSize()

		self.buttonMap.append(self.q)
		self.buttonMap.append(self.b)

	def fail(self, task):
		self.hopper.freeze = True
		self.hopper.setHealth(-1)
		print "Inside fail; hopper health:"+str(self.hopper.getHealth())
		self.world.backgroundMusic.stop()
		self.world.failSound.play()
		self.c = DirectButton(text = ("Restart Level", "Restart Level", "Restart Level", "disabled"), scale = .08, pos = (0, 0, 0) , command = self.reset)
		self.c.resetFrameSize()

		self.buttonMap.append(self.c)
	
	def quit(self):
		sys.exit()	
	
	#----- User Input Functions -----
	def getHelp(self):
		self.blackFrame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-3,3,-3,1),pos=(-1,1,1))
		self.walk = self.addInstructions(0.3, "[W]: Forward")
		self.turnLeft = self.addInstructions(0.2, "[A]: Turn Left")
		self.turnRight = self.addInstructions(0.1, "[D]: Turn Right")
		self.jump = self.addInstructions(0.0, "[Space]: Jump") 
		self.theHelp = self.addInstructions(-0.1, "[H]: Help") 
		self.lighting = self.addInstructions(-0.2, "[L]: Toggle Lighting") 
		self.debugging = self.addInstructions(-0.3, "[B]: Toggle Debugging") 
	
	def destroyHelp(self):
		self.blackFrame.destroy()
		self.walk.destroy()
		self.turnLeft.destroy()
		self.turnRight.destroy()
		self.jump.destroy()
		self.theHelp.destroy()
		self.lighting.destroy()
		self.debugging.destroy()

	def addInstructions(self, pos, msg):
		return OnscreenText(text = msg, style = 1, fg = (1, 1, 1, 1), pos = (0, pos), align= TextNode.ACenter, scale = .1)

	def toggleHelp(self):
		if self.isHelping == False:
			self.getHelp()
			self.isHelping = True
		else:
			self.destroyHelp()
			self.isHelping = False
	
	def toggleDebug(self):
		if self.isDebugging == False:
			self.debugNP.show()
			self.isDebugging = True
		else:
			self.debugNP.hide()
			self.isDebugging = False

	def toggleLight(self):
		if self.isLit == False:
			self.hopper.freeze = True
			self.world.addLight()
			self.isLit = True
			unfreezeSeq = Sequence(Wait(2.0), Func(self.hopper.unfreeze))
			unfreezeSeq.start()
		else:
			self.world.destroyLight()
			self.isLit = False

game = PlayHopper()
game.run()

















