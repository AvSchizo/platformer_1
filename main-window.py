import pygame
import random


pygame.init()
pygame.display.set_caption("PLATFORMER")

refScreenSize = [1600, 900]
screen = pygame.display.set_mode(refScreenSize)
resolutionScaling = screen.get_height()/refScreenSize[1]
resolutionScaling_alt = screen.get_width()/refScreenSize[0]


clock = pygame.time.Clock()





class cameraClass():
	def __init__(self, scalingReference=[1/2, 10]):

		self.pos = [0, 0, 0]
		
		self.scalingFactor = scalingReference[0]**(1/scalingReference[1])
	

	def getScaling(self, distance=0):
		# gets called by other objects when they're determining their size and position when drawing themselves
		camScaling = self.scalingFactor**(self.pos[2]-distance)
		return camScaling
