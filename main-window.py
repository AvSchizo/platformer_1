import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
pygame.display.set_caption("PLATFORMER")




class cameraClass():
	def __init__(self, scalingReference=[1/2, 10]):

		self.pos = [0, 0, 0]
		
		self.scalingFactor = 1/scalingReference[0]**(0-scalingReference[1])
	

	def getScaling(self, distance=0):
		# gets called by other objects when they're determining their size and position when drawing themselves
		return scalingFactor**(self.pos[2]-distance)
