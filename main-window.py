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

	def __init__(self, size=[800, 450], scalingReference=[1/2, 10], pos=[0, 0, 0]):

		self.size = size

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
	


	def follow(self, object):
		self.pos[0] = object.pos[0]
		self.pos[1] = object.pos[1]

# special camera for codehs, get rid of size=[400, 450] at home
camera = cameraClass(size=[400, 450])




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
	mglc([(-800, -100), (5000, -100)]),
	mglc([(100, -100), (100, 0)]),
	mglc([(100, 0), (200, 0)]),
	mglc([(200, -100), (200, 0)]),
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
	


	# dash function
	def initiate(self, direction, player, dashSpeed=10, length=5):
		if direction[0] == direction[1] and direction[0] == 0 or direction[1] == -1 and player.airTime == 0 or self.dashes == 0:
			return

		if player.airTime > 0:
			self.dashes -= 1

		player.dashInitiated()
		
		for i in range(len(self.velocity)):
			self.velocity[i] = direction[i]*dashSpeed

		self.timer = length
	


	def startCooldown(self, time=20):
		self.cooldown = time
	


	def update(self):
		
		if self.timer > 0:
			self.timer -= 1
			if self.timer == 0:
				self.startCooldown()
		if self.timer < 0:
			self.timer = 0
		
		if self.timer == 0:
			timerDecrease = 1
			for i in range(len(self.velocity)):
				if abs(self.velocity[i]) <= timerDecrease:
					self.velocity[i] = 0
				else:
					if self.velocity[i] > 0:
						self.velocity[i] -= timerDecrease
					if self.velocity[i] < 0:
						self.velocity[i] += timerDecrease

		if self.cooldown > 0:
			self.cooldown -= 1
		if self.cooldown < 0:
			self.cooldown = 0



	def updateSpec(self, data, decrease=1):
		if data > 0:
			data -= decrease
		if data < 0:
			data = 0




class playerClass():

	def __init__(self, pos=[0, 0], inList=[]):

		self.dash = dashClass()

		self.pos = pos
		self.z = 0
		self.size = [25, 25]

		self.velocity = [0, 0]
		self.airTime = 0
		self.extraJumpForce = 0

		self.totalInputList = inList



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
				self.totalInputList.append(tempList1)

		if indi1:
			self.inputValues = self.totalInputList[currentFrame-1]
		else:
			return tempList1



	def dealWithInputs(self):
		self.getInputValues(tas=TAS)

		if self.inputValues[6] == 1 and self.dash.timer == 0 and self.dash.cooldown == 0:
			self.dash.initiate([self.inputValues[3]-self.inputValues[2], self.inputValues[0]-self.inputValues[1]], self)

		maxJumpHigher = 10
		if self.airTime > 0 and self.inputValues[5] == 0 or self.airTime > maxJumpHigher:
			self.jumpHigher = 0
		else:
			self.jumpHigher = 1
		jumpForce = 15
		if self.inputValues[5] == 1 and self.airTime == 0:
			self.jump(jumpForce)
		if self.jumpHigher == 1 and self.airTime > 0:
			self.velocity[1] += .5

		acceleration = 1
		deceleration = .8
		walkSpeed = 5
		if self.inputValues[2] == 1 and self.velocity[0] > -1*walkSpeed*(self.inputValues[4]+1):
			self.velocity[0] -= acceleration
			if self.velocity[0] > 0:
				self.velocity[0] -= acceleration
		if self.inputValues[3] == 1 and self.velocity[0] < walkSpeed*(self.inputValues[4]+1):
			self.velocity[0] += acceleration
			if self.velocity[0] < 0:
				self.velocity[0] += acceleration

		if self.inputValues[2] + self.inputValues[3] == 0:
			if abs(self.velocity[0]) <= 1:
				self.velocity[0] = 0
			else:
				self.velocity[0] *= deceleration

		if self.velocity[0] <= -1*walkSpeed*(self.inputValues[4]+1)-1:
			self.velocity[0] += 1
		if self.velocity[0] >= walkSpeed*(self.inputValues[4]+1)+1:
			self.velocity[0] -= 1
	


	def jump(self, force=10):
		self.extraJumpForce = 8
		self.velocity[1] = force
	


	def updatePhysics(self, opgeo=None):

		if opgeo == None:
			geo = mapGeo_loaded
		else:
			geo = opgeo


		defaultGravity = 1.5
		gravity = defaultGravity

		if self.airTime > 2 or self.jumpHigher == 0:
			self.extraJumpForce = 0
		
		if self.dash.timer == 0:
			if self.velocity[1] > 0 and self.jumpHigher == 0:
				self.velocity[1] -= gravity*3
			else:
				self.velocity[1] -= gravity


		# horizontal movement + collision
		inVel = self.velocity[0] + self.dash.velocity[0]
		self.collisionNormal(0, geo, inVel)

		# vertical movement + collision
		inVel = self.velocity[1] + self.dash.velocity[1] + self.extraJumpForce
		self.collisionNormal(1, geo, inVel)



	def dashInitiated(self):
		self.velocity[1] = 0
	


	def collisionNormal(self, dir, geo, vel):
		velocity = int(vel)
		velDist = abs(velocity)
		if dir == 1 and (velDist > 0 or self.airTime > 0):
			self.airTime += 1
		for i in range(velDist):
			lastPos = self.pos[dir]
			self.pos[dir] += velocity/velDist
			collided = 0
			for line in geo:
				pointA = line.points[0]
				pointB = line.points[1]

				# if both on one side
				if abs(pointA[0]-self.pos[0]) > self.size[0]/2 and abs(pointB[0]-self.pos[0]) > self.size[0]/2 and (pointA[0]-self.pos[0])*(pointB[0]-self.pos[0]) >= 0:
					pass
				elif abs(pointA[1]-self.pos[1]) > self.size[1]/2 and abs(pointB[1]-self.pos[1]) > self.size[1]/2 and (pointA[1]-self.pos[1])*(pointB[1]-self.pos[1]) >= 0:
					pass
				else:
					collided = 1

	
			if collided == 1:
				self.pos[dir] = lastPos

				if dir == 1 and velocity < 0:
					self.airTime = 0
					self.dash.dashes = 1

				self.velocity[dir] = 0

				if self.airTime > 0 and dir == 1:
					self.velocity[0] += self.dash.velocity[0]
					self.dash.reset()
					self.dash.startCooldown(10)


	
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










FPS = 30

currentFrame = 0

while True:

	currentFrame += 1


	frameEvents = pygame.event.get()
	for event in frameEvents:
		if event.type == pygame.QUIT:
			exit()




	player.dash.update()
	player.dealWithInputs()

	player.updatePhysics()


	if player.pos[0] < camera.left:
		camera.pos[0] = player.pos[0] - camera.width/2
	if player.pos[0] > camera.right:
		camera.pos[0] = player.pos[0] + camera.width/2
	camera.update()


	screen.fill((0, 0, 10))

	player.draw()


	for line in mapGeo_loaded:
		line.draw(opscrn=screen)


	pygame.display.update()
	clock.tick(FPS)
