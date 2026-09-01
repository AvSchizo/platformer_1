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

		self.size = [800, 450]

		self.pos = [0, 0, 0]
		
		self.scalingFactor = scalingReference[0]**(1/scalingReference[1])

		self.update()
	

	def getScaling(self, distance=0):
		# gets called by other objects when they're determining their size and position when drawing themselves
		return self.scalingFactor**(self.pos[2]-distance)
	

	def update(self):
		camScaling = self.getScaling()

		self.left = self.pos[0] - (self.size[0]/2 * camScaling)
		self.right = self.pos[0] + (self.size[0]/2 * camScaling)

		self.bottom = self.pos[1] - (self.size[1]/2 * camScaling)
		self.top = self.pos[1] + (self.size[1]/2 * camScaling)




# mglc: mapGeoLineClass
class mglc():

	def __init__(self, points, direction=None):

		self.points = points

		self.direction = direction


### TEST LEVEL ###
mapGeo_loaded = [
	mglc([(-800, 0), (800, 0)]),
]




class playerClass(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface(())
	

	def update()


player = pygame.sprite.GroupSingle()







FPS = 60
seconds = 2

for i in range(seconds*FPS):
	clock.tick(60)
