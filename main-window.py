import pygame
import random
from sys import exit


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
	


	def draw(self, opscrn=None, opcam=None):

		if opscrn == None:
			opscrn = screen
		else:
			scrn = opscrn

		if opcam == None:
			cam = camera
		else:
			cam = opcam


		pointA = self.points[0]
		pointB = self.points[1]

		scaling = cam.getScaling()*resolutionScaling
		pygame.draw.line(scrn, (255, 255, 255), (scrn.get_width()/2+(pointA[0]-cam.pos[0])*scaling, scrn.get_height()/2-(pointA[1]-cam.pos[1])*scaling), (scrn.get_width()/2+(pointB[0]-cam.pos[0])*scaling, scrn.get_height()/2-(pointB[1]-cam.pos[1])*scaling), 1)


### TEST LEVEL ###
mapGeo_loaded = [
	mglc([(-800, -100), (800, -100)]),
]




### PLAYER STUFF ###
class dashClass():
	
	def __init__(self):
		self.reset()
	


	def reset(self):

		self.velocity = [0, 0]

		self.timer = 0
		self.cooldown = 0

		self.dashes = 1
	


	def initiate(self, direction, dashSpeed=10):
		if direction[0] == direction[1] and direction[0] == 0:
			return
		
		for i in range(len(self.velocity)):
			self.velocity[i] == direction[i]*dashSpeed
	


	def startCooldown(self, time=10):
		self.cooldown = time
	


	def update(self):
		
		if self.timer > 0:
			self.timer -= 1
			if self.timer == 0:
				self.startCooldown()
		if self.timer < 0:
			self.timer = 0
		
		if self.timer == 0:
			for v in self.velocity:
				self.updateSpec(v)

		self.updateSpec(cooldown)



	def updateSpec(self, data):
		if self.data > 0:
			self.data -= 1
		if self.data < 0:
			self.data = 0




class playerClass():

	def __init__(self, pos=[0, 0]):

		self.dash = dashClass()

		self.pos = pos
		self.z = 0
		self.size = [25, 25]

		self.velocity = [0, 0]
		self.airTime = 0

		self.totalInputList = []



	def getInputValues(self, tas=False, indi1=True, indi2=True):

		# inputValues setup
		if tas and currentFrame <= len(self.totalInputList):
			pass
	
		# turn player inputs into input values
		else:
	
			tempList1 = []
			keysDown = pygame.key.get_pressed()
			for key in list(playerInputs.values()):
				if keysDown[key]:
					tempList1.append(1)
				else:
					tempList1.append(0)

			if indi2:
				totalInputList.append(tempList1)

		if indi1:
			self.inputValues = tempList1
		else:
			return tempList1
	


	def updatePhysics(self, opgeo=None):

		if opgeo == None:
			geo = mapGeo_loaded
		else:
			geo = opgeo


		defaultGravity = .5
		gravity = defaultGravity
		
		if self.dash.timer > 0:
			self.velocity[1] = self.dash.velocity[1]
		else:
			self.velocity[1] -= gravity


		# horizontal movement + collision
		inVel = self.velocity[0]
		self.collisionNormal(0, geo, inVel)

		# vertical movement + collision
		inVel = self.velocity[1]
		self.collisionNormal(1, geo, inVel)
	


	def collisionNormal(self, dir, geo, vel):
		velocity = int(vel)
		velDist = abs(velocity)
		for i in range(velDist):
			lastPos = self.pos[dir]
			self.pos[dir] += velocity/velDist
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

					self.airTime = 0

					self.velocity[dir] = 0
					#to stop checking other lines for collision
					return
		self.airTime += 1


	
	def draw(self, opscrn=None, opcam=None):

		if opscrn == None:
			scrn = screen
		else:
			scrn = opscrn

		if opcam == None:
			cam = camera
		else:
			cam = opcam


		scaling = cam.getScaling(self.z) * resolutionScaling

		image = pygame.Surface([25*scaling]*2)
		image.fill("red")

		# calculates position on screen
		rect = image.get_rect(center=(scrn.get_width()/2+(self.pos[0]-cam.pos[0])*scaling, scrn.get_height()/2-(self.pos[1]-cam.pos[1])*scaling))

		scrn.blit(image, rect)

player = playerClass(pos=[0, 0])




# INPUTS

# toFind is value, function returns index of key in list of keys
def findIndex_dict(toFind, dict):
	keys = list(dict.keys())
	for i in range(len(keys)):
		
		if dict[keys[i]] == toFind:
			return i
	
	print("debug (findIndex_dict): findIndex_dict returns nothing")


TAS = False
totalInputList = []

playerInputs = {
	"up": pygame.K_UP,
	"down": pygame.K_DOWN,
	"left": pygame.K_LEFT,
	"right": pygame.K_RIGHT,
	"z": pygame.K_z,
	"x": pygame.K_x,
	"c": pygame.K_c,
	"escape": pygame.K_ESCAPE,
}
player.getInputValues()










FPS = 30

currentFrame = 0

while True:

	currentFrame += 1


	frameEvents = pygame.event.get()
	for event in frameEvents:
		if event.type == pygame.QUIT:
			exit()



	screen.fill((0, 0, 0))

	player.updatePhysics()
	player.draw()
	for line in mapGeo_loaded:
		line.draw(opscrn=screen)
	# pygame.draw.line(screen, (255, 255, 255), (-100, 0), (100, 0), 1)




	# if currentFrame > FPS*5:
	# 	break


	pygame.display.update()
	clock.tick(FPS)
