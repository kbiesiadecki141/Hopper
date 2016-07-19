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
*  Description: This class sets up the onscreen  *
*               interface of Hopper!             *
*                                                *
**************************************************
"""

from panda3d.core import *
from panda3d.bullet import *

from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

class OnscreenInterface():
	def __init__(self):
		pass

	def createStartScreen(self):
		self.startScreen = OnscreenImage(image = "images/HopperStartScreen.png", pos = (0, 0, 0), scale = (1.35, 1, 1))

	def destroyStartScreen(self):
		self.startScreen.destroy()
	
	def startButton(self):
		#maps = loader.loadModel('maps/button_maps')
		return DirectButton(text = ("Start", "Start", "Start", "disabled"), scale = .18, pos = (0, 0, -0.3))#, geom = (maps.find('**/button_ready'), maps.find('**/button_click'), maps.find('**/button_rollover'), maps.find('**/button_disabled')))

	def createLevelSelectScreen(self):
		self.levelSelectScreen = OnscreenImage(image = "images/levelSelect.png", pos = (0, 0, 0), scale = (1.35, 1, 1))

	def destroyLevelSelectScreen(self):
		self.levelSelectScreen.destroy()
		
	def levelSelectButton(self, level, pos):
	 	return DirectButton(text = ("Level "+str(level), "Level "+str(level), "Level "+str(level), "disabled"), scale = .09, pos = (pos, 0, -0.6))
			
