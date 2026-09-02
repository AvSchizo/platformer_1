import pygame
import random


pygame.init()
pygame.display.set_caption("PLATFORMER")

refScreenSize = [800, 450]
screen = pygame.display.set_mode(refScreenSize)
resolutionScaling = screen.get_height()/refScreenSize[1]
resolutionScaling_alt = screen.get_width()/refScreenSize[0]


clock = pygame.time.Clock()







class cameraClass():

	def __init__(self, scalingReference=[1/2, 10], pos=[0, 0, 0]):

		self.size = [800, 450]

		self.pos = pos
		
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

		self.width = self.size[0]*camScaling
		self.height = self.size[1]*camScaling

camera = cameraClass()




# mglc: mapGeoLineClass
class mglc():

	def __init__(self, points, direction=None):

		self.points = points

		self.direction = direction
	


	def draw(self, scrn=screen):
		# screen.get_width()/2-(self.pos[0]-cam.pos[0])*scaling
		pygame.draw.line(screen, (255, 255, 255), (100, 50), self.points[1], 10)


### TEST LEVEL ###
mapGeo_loaded = [
	mglc([(-800, -100), (800, -100)]),
]




class playerClass():

	def __init__(self, pos=[0, 0]):

		self.pos = pos
		self.z = 0
		self.size = [25, 25]

		self.velocity = [0, 0]
	


	def updatePhysics(self, geo=mapGeo_loaded):

		defaultGravity = .5
		gravity = defaultGravity
		
		self.velocity[1] = -1


		# horizontal movement + collision
		self.collisionNormal(0, geo)

		# vertical movement + collision
		self.collisionNormal(1, geo)
	


	def collisionNormal(self, dir, geo):
		velDist = int(abs(self.velocity[dir]))
		for i in range(velDist):
			lastPos = self.pos[dir]
			self.pos[dir] += self.velocity[dir]/velDist
			for line in geo:
				pointA = line.points[0]
				pointB = line.points[1]

				# if both on one side
				collided = 0
				if abs(pointA[0]-self.pos[0]) > self.size[0]/2 and abs(pointB[0]-self.pos[0]) > self.size[0]/2 and (pointA[0]-self.pos[0])*(pointB[0]-self.pos[0]) >= 0:
					pass
				elif abs(pointA[1]-self.pos[1]) > self.size[1]/2 and abs(pointB[1]-self.pos[1]) > self.size[1]/2 and (pointA[1]-self.pos[1])*(pointB[1]-self.pos[1]) >= 0:
					pass
				else:
					self.pos[dir] = lastPos
					self.velocity[dir] = 0
					#to stop checking other lines for collision
					return
				print(self.pos[dir])


	
	def draw(self, scrn=screen, cam=camera):

		scaling = cam.getScaling(self.z) * resolutionScaling

		image = pygame.Surface([25*scaling]*2)
		image.fill("red")

		# calculates position on screen
		rect = image.get_rect(center=(screen.get_width()/2-(self.pos[0]-cam.pos[0])*scaling, screen.get_height()/2-(self.pos[1]-cam.pos[1])*scaling))

		screen.blit(image, rect)

player = playerClass(pos=[0, 0])










FPS = 30

currentFrame = 0

while True:

	currentFrame += 1



	screen.fill((0, 0, 0))

	player.updatePhysics()
	player.draw()
	for line in mapGeo_loaded:
		line.draw(scrn=screen)
	# pygame.draw.line(screen, (255, 255, 255), (-100, 0), (100, 0), 1)




	if currentFrame > FPS*5:
		break


	pygame.display.update()
	clock.tick(60)
