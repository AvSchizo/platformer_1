import pygame
import random
from sys import exit, argv
from copy import deepcopy
from math import atan, sin, cos, pi, sqrt


pygame.init()
pygame.display.set_caption("PLATFORMER")

refScreenSize = [800, 450]
screen = pygame.display.set_mode(refScreenSize)
resolutionScaling = screen.get_height()/refScreenSize[1]
resolutionScaling_alt = screen.get_width()/refScreenSize[0]


clock = pygame.time.Clock()


# draws line according to scale
def drawLine(color, pointA, pointB, scaling, lineWidth=1, inscrn=None, incam=None):
	if inscrn == None:
		scrn = screen
	else:
		scrn = inscrn
	
	if incam == None:
		cam = camera
	else:
		cam = incam
	
	pygame.draw.line(scrn, color, (scrn.get_width()/2+(pointA[0]-cam.pos[0])*scaling, scrn.get_height()/2-(pointA[1]-cam.pos[1])*scaling), (scrn.get_width()/2+(pointB[0]-cam.pos[0])*scaling, scrn.get_height()/2-(pointB[1]-cam.pos[1])*scaling), lineWidth)



TAS = False
TASedit = 0
levelEdit = False


def getTASInputs(file):
	with open (file, "r") as f:
		tfl = f.read().splitlines()
	
	toReturn = []
	for l in tfl:

		if l == "empty" or l == "":
			toReturn.append([0, 0, 0, 0, 0, 0, 0, 0])

		# left side
		elif l == "left":
			toReturn.append([0, 0, 1, 0, 0, 0, 0, 0])

		elif l == "lump":
			toReturn.append([0, 0, 1, 0, 0, 1, 0, 0])

		elif l == "run left":
			toReturn.append([0, 0, 1, 0, 1, 0, 0, 0])

		elif l == "run lump":
			toReturn.append([0, 0, 1, 0, 1, 1, 0, 0])

		elif l == "full left":
			toReturn.append([0, 0, 1, 0, 1, 0, 1, 0])

		# right side
		elif l == "right":
			toReturn.append([0, 0, 0, 1, 0, 0, 0, 0])

		elif l == "rump":
			toReturn.append([0, 0, 0, 1, 0, 1, 0, 0])

		elif l == "run right":
			toReturn.append([0, 0, 0, 1, 1, 0, 0, 0])

		elif l == "run rump":
			toReturn.append([0, 0, 0, 1, 1, 1, 0, 0])

		elif l == "full right":
			toReturn.append([0, 0, 0, 1, 1, 0, 1, 0])
		
		# neutral
		elif l == "jump":
			toReturn.append([0, 0, 0, 0, 0, 1, 0, 0])


		else:
			tempList1 = []
			for n in l.split():
				tempList1.append(int(n))
			toReturn.append(tempList1)
	
	return toReturn

if TAS:
	tasInputs = getTASInputs("TAS_file")
else:
	tasInputs = []




def frameHappenings():
	player.dash.update()
	player.dealWithInputs()
	player.updatePhysics()
	player.checkpointCollision(checkpointList)
	player.checkDeathPlanes(mapHazardList)




# DEBUG
# 1 is to print gamestate, 2 is to display it on screen
debug = 1
def debug_print(seperated=True):
	if seperated:
		print("_________")
	print(player.totalInputList[currentFrame-1])
	print(f"current frame: {currentFrame}")
	print(f"Xpos: {player.pos[0]}")
	print(f"Ypos: {player.pos[1]}")
	print(f"Xvel: {player.velocity[0]}")
	print(f"Yvel: {player.velocity[1]}")





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
	def initiate(self, direction, player, dashSpeed=10, length=10):
		if direction[0] == direction[1] and direction[0] == 0 or direction[1] == -1 and player.airTime == 0 or self.dashes == 0:
			return
		if direction[1] >= 0 and direction[0] == 0:
			return

		if player.airTime > 0:
			self.dashes -= 1

		player.dashInitiated()
		
		for i in range(len(self.velocity)):
			if i == 1:
				if direction[1] >= 0:
					pass
				else:
					self.velocity[i] = dashSpeed*(-2)
			else:
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
			speedDecrease = 2
			for i in range(len(self.velocity)):
				if abs(self.velocity[i]) <= speedDecrease:
					self.velocity[i] = 0
				else:
					if self.velocity[i] > 0:
						self.velocity[i] -= speedDecrease
					if self.velocity[i] < 0:
						self.velocity[i] += speedDecrease

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

	def __init__(self, eep=[0, 0], inList=[], tason=False, color="yellow"):

		self.z = 0
		self.size = [25, 25]

		self.color = color


		if tason:
			self.totalInputList = inList
		else:
			self.totalInputList = []

		self.checkpointIndex = 0
		self.lastCheckpoint = eep
		self.respawn()



	def reset(self):

		self.velocity = [0, 0]
		self.airTime = 0
		self.extraJumpForce = 0
		self.dash = dashClass()



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
		if self.inputValues[5] == 1 and self.airTime < 3:
			self.jump(jumpForce)
		# if self.jumpHigher == 1 and self.airTime > 0:
		# 	self.velocity[1] += .5

		acceleration = 1
		deceleration = .5
		walkSpeed = 5
		wsiv = walkSpeed*(self.inputValues[4]+1)
		# left
		if self.inputValues[2] == 1 and self.velocity[0] > -1*wsiv:
			self.velocity[0] -= acceleration*(self.inputValues[4]+1)
			if self.velocity[0] < -1*wsiv:
				self.velocity[0] = -1*wsiv
			if self.velocity[0] > 0:
				self.velocity[0] -= acceleration*(self.inputValues[4]+1)
		# right
		if self.inputValues[3] == 1 and self.velocity[0] < wsiv:
			self.velocity[0] += acceleration*(self.inputValues[4]+1)
			if self.velocity[0] > wsiv:
				self.velocity[0] = wsiv
			if self.velocity[0] < 0:
				self.velocity[0] += acceleration*(self.inputValues[4]+1)

		if self.inputValues[2] + self.inputValues[3] == 0:
			if abs(self.velocity[0]) <= 1:
				self.velocity[0] = 0
			else:
				self.velocity[0] *= deceleration

		if self.velocity[0] <= -1*walkSpeed*(self.inputValues[4]+1)-1:
			self.velocity[0] += .5
		if self.velocity[0] >= walkSpeed*(self.inputValues[4]+1)+1:
			self.velocity[0] -= .5
	


	def jump(self, force=10):
		self.extraJumpForce = 4
		self.velocity[1] = force
	


	def updatePhysics(self, opgeo=None):

		if opgeo == None:
			geo = mapGeo_loaded
		else:
			geo = opgeo


		defaultGravity = 1
		gravity = defaultGravity

		if self.airTime > 6 or self.jumpHigher == 0:
			self.extraJumpForce = 0
		
		if self.dash.timer == 0:
			if self.velocity[1] > 0 and self.jumpHigher == 0:
				self.velocity[1] -= gravity*3
			else:
				self.velocity[1] -= gravity
		else:
			self.velocity[1] = 0


		# horizontal movement + collision
		inVel = self.velocity[0] + self.dash.velocity[0]
		self.collisionNormal(0, geo, inVel)

		# vertical movement + collision
		inVel = self.velocity[1] + self.dash.velocity[1] + self.extraJumpForce
		self.collisionNormal(1, geo, inVel)

		while True:
			collided = 0
			for line in geo:
				if self.amTouchingGeo(line):
					collided = 1
			if collided == 0:
				break
			self.pos[1] += 1



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
				if self.amTouchingGeo(line):
					collided = 1

	
			if collided == 1:
				self.pos[dir] = lastPos

				if dir == 1 and velocity < 0:
					self.dash.dashes = 1

					if self.airTime > 0:
						if abs(self.velocity[0]) < abs(self.dash.velocity[0]) and self.dash.cooldown == 0:
							self.velocity[0] += self.dash.velocity[0]*1.5
						if self.dash.velocity[1] < 0:
							self.dash.reset()
							self.dash.startCooldown(10)
						else:
							self.dash.reset()

					self.airTime = 0

				if dir == 0:
					if self.dash.cooldown > 0:
						self.dash.velocity[0] = 0

				self.velocity[dir] = 0



	def amTouchingGeo(self, line):
		pointA = line.points[0]
		pointB = line.points[1]

		# if both on one side
		if abs(pointA[0]-self.pos[0]) > self.size[0]/2 and abs(pointB[0]-self.pos[0]) > self.size[0]/2 and (pointA[0]-self.pos[0])*(pointB[0]-self.pos[0]) >= 0:
			return False
		elif abs(pointA[1]-self.pos[1]) > self.size[1]/2 and abs(pointB[1]-self.pos[1]) > self.size[1]/2 and (pointA[1]-self.pos[1])*(pointB[1]-self.pos[1]) >= 0:
			return False
		else:
			return True



	def checkpointCollision(self, list):
		for i in range(len(list)):

			if i < self.checkpointIndex:
				continue

			c = list[i]

			left = self.pos[0]-self.size[0]/2
			right = self.pos[0]+self.size[0]/2
			bottom = self.pos[1]-self.size[1]/2
			top = self.pos[1]+self.size[1]/2

			cleft = c.area[0][0]
			cright = c.area[1][0]
			cbottom = c.area[1][1]
			ctop = c.area[0][1]

			if (left < cright and right > cleft) and (bottom < ctop and top > cbottom):
				self.checkpointIndex = i
				self.lastCheckpoint = c.respawn



	def checkDeathPlanes(self, hazards):
		dead = 0


		for i in range(len(hazards)):

			c = hazards[i]

			left = self.pos[0]-self.size[0]/2
			right = self.pos[0]+self.size[0]/2
			bottom = self.pos[1]-self.size[1]/2
			top = self.pos[1]+self.size[1]/2

			cleft = c.area[0][0]
			cright = c.area[1][0]
			cbottom = c.area[1][1]
			ctop = c.area[0][1]

			if (left < cright and right > cleft) and (bottom < ctop and top > cbottom):
				dead = 1
		

		if dead > 0:
			self.respawn()



	def respawn(self):

		self.pos = deepcopy(self.lastCheckpoint)
		self.reset()


	
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
		image.fill(self.color)

		# calculates position on screen
		rect = image.get_rect(center=(scrn.get_width()/2+(self.pos[0]-cam.pos[0])*scaling, scrn.get_height()/2-(self.pos[1]-cam.pos[1])*scaling))

		scrn.blit(image, rect)

player = playerClass(eep=[0, 0], inList=tasInputs, tason=TAS)




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

		self.left = self.pos[0] - (self.size[0]/2 * (1/camScaling))
		self.right = self.pos[0] + (self.size[0]/2 * (1/camScaling))

		self.bottom = self.pos[1] - (self.size[1]/2 * (1/camScaling))
		self.top = self.pos[1] + (self.size[1]/2 * (1/camScaling))

		self.width = self.size[0]*(1/camScaling)
		self.height = self.size[1]*(1/camScaling)
	


	def follow(self, object):
		self.pos[0] = object.pos[0]
		self.pos[1] = object.pos[1]




# mglc: mapGeoLineClass
class mglc():

	def __init__(self, points, direction=None, color=(255, 255, 255)):

		self.points = points

		self.direction = direction

		self.color = color
	


	def draw(self, opscrn=None, opcam=None):

		if opscrn == None:
			scrn = screen
		else:
			scrn = opscrn

		if opcam == None:
			cam = camera
		else:
			cam = opcam


		pointA = self.points[0]
		pointB = self.points[1]

		scaling = cam.getScaling()*resolutionScaling
		drawLine(self.color, pointA, pointB, scaling, inscrn=scrn, incam=cam)




### CHECKPOINTS ###
# checkpointClass
class cpc():

	def __init__(self, area, point):
		self.respawn = point
		# area goes: [topleft, bottomright]
		self.area = area




# dac: directionArrowClass
class dac():

	def __init__(self, inpoints, scale=.2, useSpecSides=[False, False], specSides=[(0, 0), (0, 0)], color=(0, 255, 0)):

		## finding direction
		self.points = inpoints

		# setup
		A = inpoints[0]
		B = inpoints[1]

		w = B[0]-A[0]
		h = B[1]-A[1]
		if w == 0 and h == 0:
			w = 1
			h = 0
		
		v = sqrt(h**2 + w**2) * scale

		# direction
		if w == 0:
			d = (h/abs(h)) * (pi/2)
		elif h == 0:
			d = (pi/2) - (w/abs(w))*(pi/2)
		else:
			d = atan(h/w)
			
			if w < 0:
				d += pi
		
		# other points
		for i in range(2):
			# subtracted angle on second 
			e = i*-2 + 1

			toAppend = [
				B[0] + cos(d + e*(3*pi/4))*v,
				B[1] + sin(d + e*(3*pi/4))*v
			]

			self.points.append(toAppend)

		# specific sides
		for i in range(2):
			if useSpecSides[i]:
				self.points[i] = specSides[i]


		# other shit
		self.color = color
	


	def draw(self, opscrn=None, opcam=None):

		if opscrn == None:
			scrn = screen
		else:
			scrn = opscrn

		if opcam == None:
			cam = camera
		else:
			cam = opcam

		scaling = cam.getScaling()*resolutionScaling

		pointA = self.points[0]
		pointB = self.points[1]
		pointC = self.points[2]
		pointD = self.points[3]

		drawLine(self.color, pointA, pointB, scaling, inscrn=scrn, incam=cam)
		drawLine(self.color, pointC, pointB, scaling, inscrn=scrn, incam=cam)
		drawLine(self.color, pointD, pointB, scaling, inscrn=scrn, incam=cam)




# mhc: mapHazardClass
class mhc():

	def __init__(self, inarea, inmode=1, incolor="red"):
		
		self.color = incolor

		self.area = inarea

		self.mode = inmode
	


	def draw(self, opscrn=None, opcam=None, mode=1):

		if opscrn == None:
			scrn = screen
		else:
			scrn = opscrn

		if opcam == None:
			cam = camera
		else:
			cam = opcam

		scaling = cam.getScaling()*resolutionScaling

		r = self.area[0]
		t = self.area[1]

		w = t[0]-r[0]
		h = r[1]-t[1]

		pos = [
			r[0]+w/2,
			r[1]+h/2
		]


		# option 1
		if mode == 1:
			drawLine(self.color, r, (t[0], r[1]), scaling, inscrn=scrn, incam=cam)
			drawLine(self.color, (t[0], r[1]), t, scaling, inscrn=scrn, incam=cam)
			drawLine(self.color, t, (r[0], t[1]), scaling, inscrn=scrn, incam=cam)
			drawLine(self.color, (r[0], t[1]), r, scaling, inscrn=scrn, incam=cam)

		# option 2
		if mode == 2:
			surf = pygame.Surface([ (w)*scaling, (h)*scaling ])
			surf.fill(self.color)

			rect = surf.get_rect(center=(scrn.get_width()/2+(pos[0]-cam.pos[0])*scaling, scrn.get_height()/2-(pos[1]-cam.pos[1])*scaling))

			scrn.blit(surf, rect)






##############################################
#                                            #
#                TEST LEVEL                  #
#                                            #
##############################################

mapGeo_loaded = [
	mglc([(-200, -100), (200, -100)]),
	mglc([(100, -100), (100, 0)]),
	mglc([(100, 0), (200, 0)]),
	mglc([(200, -100), (200, 0)]),
	mglc([(150, 100), (150, 30)]),
	mglc([(-200, 225), (-100, 225)]),
	mglc([(0, 350), (150, 350)]),
	mglc([(250, 325), (250, 475)]),
	mglc([(300, 275), (500, 275)]),
	mglc([(600, 400), (650, 400)]),
	mglc([(1100, 250), (1250, 250)], color=(50, 50, 255)),
]

checkpointList = [
	cpc([(1100, 500), (1250, 250)], [1150, 350])
]

mapDecList = [
	dac([(-100, 100), (-125, 200)]),
	dac([(350, 310), (375, 310)]),
	dac([(800, 300), (1000, 275)]),
]

mapHazardList = [
	mhc([(-1000000, -600), (1000000, -1000000)]),
	mhc([(500, 205), (1100, 190)]),
]


if levelEdit:
	camStartPos = [700, 320, 30]
else:
	camStartPos = [0, 0, 0]
camera = cameraClass(size=[screen.get_width()-50, screen.get_height()-50], pos=camStartPos)















# INPUTS

# toFind is value, function returns index of key in list of keys
def findIndex_dict(toFind, dict):
	keys = list(dict.keys())
	for i in range(len(keys)):
		
		if dict[keys[i]] == toFind:
			return i
	
	print("debug (findIndex_dict): findIndex_dict returns nothing")



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

toRepeat = 0
if TASedit == 1 or TAS:
	try:
		toRepeat = int(argv[1])
	except:
		toRepeat = 0
if TASedit == 2:
	toRepeat = int(input())-1

if levelEdit:
	toRepeat = 20

for i in range(toRepeat):
	currentFrame += 1
	frameHappenings()

while True:

	


	frameEvents = pygame.event.get()
	for event in frameEvents:
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
			exit()

		if TASedit == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			currentFrame += 1
			frameHappenings()
			print(currentFrame)



	if TASedit != 1:
		currentFrame += 1
		frameHappenings()



	### CAMERA ###
	if not levelEdit:
			
		if player.pos[0] < camera.left:
			camera.pos[0] -= camera.width
		if player.pos[0] > camera.right:
			camera.pos[0] += camera.width
		
		if player.pos[1] < camera.bottom:
			camera.pos[1] -= camera.height
		if player.pos[1] > camera.top:
			camera.pos[1] += camera.height

	if TASedit > 0:
		cameraFollowPlayer = True
	else:
		cameraFollowPlayer = False
	if cameraFollowPlayer and currentFrame % 1 == 0:
		camera.follow(player)

	camera.update()






	##### RENDERING #####



	screen.fill((0, 0, 10))

	player.draw()


	for line in mapGeo_loaded:
		line.draw(opscrn=screen)
	
	for line in mapDecList:
		line.draw(opscrn=screen)
	
	for haz in mapHazardList:
		haz.draw(opscrn=screen, mode=haz.mode)






	pygame.display.update()
	if debug == 1 and TASedit > 0:
		debug_print()
	if TASedit == 2:
		input()
	clock.tick(FPS)
