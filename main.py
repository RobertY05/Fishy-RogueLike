#Robert Yan
#2023 01 24
#Pygame Culminating Assignment: Maze Game

#import necessary libraries
import pygame
import random
import math
import random
import copy
from collections import deque

#start pygame, declare screen size as constant variables, and intialize / create important variables
pygame.init()
WIDTH, HEIGHT = 640, 480
pygame.display.set_caption("PY GAMING")
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
mousePos = (-1, -1)
m1, m2, m3 = False, False, False
pm1, pm2, pm3 = False, False, False
clock = pygame.time.Clock()

#---other constants---
WALKSQUISH = 2
SHOOTSTRETCH = 4
ANIMDELAY = 5
GRIDWIDTH = WIDTH // 40
GRIDHEIGHT = HEIGHT // 40
MAPSIZE = 7
BIGFONT = pygame.font.Font("tf2build.ttf", 32)
LITTLEFONT = pygame.font.Font("tf2build.ttf", 16)

#---load all images here---:
AnglerFlopper = pygame.image.load("AnglerFlopper.png")
BlobFlopper = pygame.image.load("BlobFlopper.png")
BlueFlopper = pygame.image.load("BlueFlopper.png")
BombFlopper = pygame.image.load("BombFlopper.png")
BubbleEnemy = pygame.image.load("BubbleEnemy.png")
BubbleFriendly = pygame.image.load("BubbleFriendly.png")
BubblePop = pygame.image.load("BubblePop.png")
Dirt = [pygame.image.load("Dirt0.png"), pygame.image.load("Dirt1.png"), pygame.image.load("Dirt2.png")]
GoldFlopper = pygame.image.load("GoldFlopper.png")
GreenFlopper = pygame.image.load("GreenFlopper.png")
IceFlopper = pygame.image.load("IceFlopper.png")
LongFlopper = pygame.image.load("LongFlopper.png")
OrangeFlopper = pygame.image.load("OrangeFlopper.png")
PercItem = pygame.image.load("PercItem.png")
BalloonItem = pygame.image.load("BalloonItem.png")
RoidsItem = pygame.image.load("RoidsItem.png")
ChairItem = pygame.image.load("ChairItem.png")
AirburstItem = pygame.image.load("AirburstItem.png")
BuckyItem = pygame.image.load("BuckyItem.png")
BoomerangItem = pygame.image.load("BoomerangItem.png")
JacketItem = pygame.image.load("JacketItem.png")
WheelItem = pygame.image.load("WheelItem.png")
ArthritisItem = pygame.image.load("ArthritisItem.png")
Door = [pygame.image.load("Door.png")]
Rock = [pygame.image.load("Rock0.png"), pygame.image.load("Rock1.png"), pygame.image.load("Rock2.png")]
Sand = [pygame.image.load("Sand0.png"), pygame.image.load("Sand1.png"), pygame.image.load("Sand2.png")]
SquareFlopper = pygame.image.load("SquareFlopper.png")
Water = [pygame.image.load("Water0.png"), pygame.image.load("Water1.png"), pygame.image.load("Water2.png"), pygame.image.load("Water3.png"), pygame.image.load("Water4.png")]
Heart = pygame.image.load("Heart.png")
Whirlpool = pygame.image.load("Whirlpool.png")

#---function tools---:

#function to return a manipulated image, returns the manipulated image based on arguments
def newImage(base, xStretch, yStretch, facingRight, facingUp, rotation):

  #define the return variable
  ret = base

  #apply stretch / squish on x / y axis if needed
  if xStretch != 0 or yStretch != 0:
    ret = pygame.transform.scale(base, (base.get_width()+xStretch, base.get_width()+yStretch))

  #apply flip on x / y axis if needed
  if (facingRight or facingUp):
    ret = pygame.transform.flip(ret, facingRight, facingUp)

  #rotate if needed
  if (rotation != 0):
    ret = pygame.transform.rotate(ret, rotation)

  #return the transformed image
  return ret

#returns a distance using pythagorean theorem
def distance(x1, y1, x2, y2):
  dx = x2 - x1
  dy = y2 - y1
  return math.sqrt(dx * dx + dy * dy)

#returns true if the two circles given are colliding, otherwise false
def circleCircle(x1, y1, r1, x2, y2, r2):
  if (distance(x1, y1, x2, y2) < r1 + r2):
    return True
  return False

#returns true if the circle and square given are colliding, otherwise false
def circleSquare(x1, y1, r1, x2, y2, s2):
  testX = -1
  testY = -1

  #find the closest sides of the rectangle
  if x1 < x2:
    testX = x2-s2/2
  else:
    testX = x2+s2/2
  if y1 < y2:
    testY = y2-s2/2
  else:
    testY = y2+s2/2

  #check the distances from the circle to the sides
  if (abs(testX - x1) < r1 and y2-s2/2-r1 < y1 < y2+s2/2+r1) or (abs(testY - y1) < r1 and x2-s2/2-r1 < x1 < x2+s2/2+r1):
    return True

  return False

#function that handles wall collision, returns the closest x value and y value to the wall
def tileCollision(xTargetIn, yTargetIn, xPrevIn, yPrevIn, radius):

  #define some helper variables
  xGrid = round((xPrevIn-20)/40)
  yGrid = round((yPrevIn-20)/40)
  checks = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
  validX = xTargetIn
  validY = yTargetIn
  flag = False

  #check up down left right first
  for i in checks:

    #the spot that will be checked
    checkX = xGrid+i[0]
    checkY = yGrid+i[1]

    #check if there is a collision
    if 0 <= checkX <= GRIDWIDTH-1 and 0 <= checkY <= GRIDHEIGHT-1 and curRoom.blocked[checkX][checkY] and circleSquare(validX, validY, radius, checkX*40+20, checkY*40+20, 40):

      #set return variables
      flag = True
      newX = -1
      newY = -1

      #check which side and set x / y accordingly
      if xPrevIn < checkX*40+20:
        newX = checkX*40-radius
      else:
        newX = checkX*40+40+radius
      if yPrevIn < checkY*40+20:
        newY = checkY*40-radius
      else:
        newY = checkY*40+40+radius

      #use the side that is closer to the item being collided with
      if distance(newX, validY, xPrevIn, yPrevIn) < distance(validX, newY, xPrevIn, yPrevIn):
        validX = newX
      else:
        validY = newY

  return (validX, validY, flag)

#function that returns an angle in radians given two cordinates
def angle(origX, origY, destX, destY):
  opp = abs(origY-destY)
  adj = abs(origX-destX)
  above = False
  right = False
  if origX < destX:
    right = True
  if origY > destY:
    above = True

  if adj == 0:
    adj = 0.1

  angle = math.atan(opp/adj)

  if above and right:
    return angle + math.pi/2
  elif above and not right:
    return math.pi * 3 / 2 - angle
  elif not above and not right:
    return math.pi * 3 / 2 + angle
  else:
    return math.pi/2 - angle

#function that loads the current room
def loadRoom(room):
  allSprites.clear()
  for i in room.tiles:
    for j in i:
      allSprites.append(j, 0)
  if not room.cleared:
    for i in room.enemies:
      i.kill = False
      allSprites.append(i, 1)
      enemies.append(i)
  allSprites.append(playerInstance, 1)
  allSprites.append(floorMap, 2)
  allSprites.append(healthBar, 2)

  if room.curItem != -1:
    allSprites.append(room.curItem, 1)
  if room.special == 2 and room.cleared:
    allSprites.append(hole(WIDTH/2, HEIGHT/2), 1)

def bfs(xIn, yIn, room, melee):
  path = [[-1 for y in range(GRIDHEIGHT)] for x in range(GRIDWIDTH)]
  if (0 <= xIn <= GRIDWIDTH-1 and 0 <= yIn <= GRIDHEIGHT-1) == False:
    return path
  queue = deque()
  queue.append((xIn, yIn, 0))
  path[xIn][yIn] = 0
  dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  while (len(queue) > 0):
    x, y, step = queue.popleft()
    for i in dir:
      newX = x+i[0]
      newY = y+i[1]
      if 0 <= newX <= GRIDWIDTH-1 and 0 <= newY <= GRIDHEIGHT-1 and path[newX][newY] == -1 and not room.blocked[newX][newY]:
        queue.append((newX, newY, step+1))
        path[newX][newY] = step+1
  if melee:
    for i in enemies:
      if i.standRange == 0:
        tmpX, tmpY = round((i.x-20)/40), round((i.y-20)/40)
        path[tmpX][tmpY] += 4

  return path

def generateFloor(tileSet, enemySet):
  curFloor = [[False for i in range(MAPSIZE)] for j in range(MAPSIZE)]
  x = MAPSIZE//2
  y = MAPSIZE//2
  curX = x
  curY = y
  roomCount = (MAPSIZE*MAPSIZE) // 3 + (random.randint(0, 4))
  tmp = 0
  dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  while tmp < roomCount:
    if curFloor[x][y] == False:
      tmp += 1
      curFloor[x][y] = True
    while True:
      idx = random.randint(0, 3)
      newX = x + dir[idx][0]
      newY = y + dir[idx][1]
      if 0 <= newX <= MAPSIZE-1 and 0 <= newY <= MAPSIZE-1:
        x = newX
        y = newY
        break

  x = MAPSIZE//2
  y = MAPSIZE//2
  ret = [[-1 for i in range(MAPSIZE)] for j in range(MAPSIZE)]
  ret[x][y] = room(enemySet, 0, tileSet, curFloor[x][y-1], curFloor[x-1][y], curFloor[x][y+1], curFloor[x+1][y])
  ret[x][y].clear()
  q = deque()
  needTreasure = True
  q.append((x, y, 0))
  while len(q) > 0:
    x, y, step = q.popleft()
    up, left, down, right = False, False, False, False
    if 0 <= y-1 <= MAPSIZE-1:
      up = curFloor[x][y-1]
    if 0 <= x-1 <= MAPSIZE-1:
      left = curFloor[x-1][y]
    if 0 <= y+1 <= MAPSIZE-1:
      down = curFloor[x][y+1]
    if 0 <= x+1 <= MAPSIZE-1:
      right = curFloor[x+1][y]

    if ret[x][y] == 0:
      if step > 2 and needTreasure:
        ret[x][y] = room(enemySet, 1, tileSet, up, left, down, right)
        ret[x][y].clear()
        needTreasure = False
      else:
        ret[x][y] = room(enemySet, -1, tileSet, up, left, down, right)

    if up and ret[x][y-1] == -1:
      ret[x][y-1] = 0
      q.append((x, y-1, step+1))
    if left and ret[x-1][y] == -1:
      ret[x-1][y] = 0
      q.append((x-1, y, step+1))
    if down and ret[x][y+1] == -1:
      ret[x][y+1] = 0
      q.append((x, y+1, step+1))
    if right and ret[x+1][y] == -1:
      ret[x+1][y] = 0
      q.append((x+1, y, step+1))

  ret[x][y] = room(enemySet, 2, tileSet, up, left, down, right)
  return ret

#---classes---:
class spriteGroup():

  #constructor: make two lists to manage the sprites, set the time it takes to clear
  def __init__(self, layers):
    self.layers = layers
    self.allSprites = [[] for i in range(self.layers)]
    self.clearRate = 20
 
  #add something to the sprite list
  def append(self, sprite, order):
    self.allSprites[order].append(sprite)

  #empty the list
  def clear(self):
    for i in self.allSprites:
      i.clear()

  #code to update the sprites:
  def update(self):

    #delete marked sprites every so often
    if counter % self.clearRate == 0:

      #reset counter make temporary list
      tmp = [[] for i in range(self.layers)]

      #append only unmarked sprites
      for i in range(len(self.allSprites)):
        for j in self.allSprites[i]:
          if not j.kill:
            tmp[i].append(j)

      #update the list that actually gets used
      self.allSprites = tmp
    
    #update all the sprites
    for i in self.allSprites:
      for j in i:
        if not j.kill:
          j.update()

  #function to draw all the sprites
  def draw(self):
    for i in self.allSprites:
      for j in i:
        if not j.kill:
          j.draw()

class player():
  def __init__(self):
    self.kill = False

    #stats:
    self.bulletProperties = []
    self.bulletSpeed = 7
    self.bulletSize = 15
    self.bulletKB = 1
    self.damage = 1
    self.shootCD = 30
    self.speed = 5
    self.maxHealth = 3
    self.blastResistance = False

    #changing game variables:
    self.curHealth = 3
    self.x = WIDTH / 2
    self.y = HEIGHT / 2
    self.timeToShoot = 0

    # W A S D
    self.moving = [False, False, False, False]
    self.shooting = [False, False, False, False]

    #animation variables:
    self.radius = 18
    self.shootState = 0
    self.shootMax = 4
    self.iFrames = 60
    self.iFrameVisible = True
    self.iFrameBlink = 10
    self.iFrameCounter = 0
    self.walkRight = True
    self.walkState = 0
    self.walkMax = 5
    self.walkAnimDir = 1
    self.animTimer = ANIMDELAY
    self.deathFrame = 0
    self.deathMax = 5

  def update(self):
    if self.curHealth == 0:
      self.animTimer = max(0, self.animTimer - 1)
      if self.animTimer == 0:
        self.animTimer = ANIMDELAY
        self.deathFrame += 1
      if self.deathFrame > self.deathMax:
        allSprites.append(messageEffect("You Died!!!", "press R to restart"), 2)
        allSprites.append(explosionEffect(self.x, self.y, 120, 20, 3, 999), 1)
        self.kill = True
        global needRestart
        needRestart = True

      return

    directions = self.moving[0] + self.moving[1] + self.moving[2] + self.moving[3]
    diagonal = 1
    if directions != 0:
        diagonal = math.sqrt(2)

    newX = self.x
    newY = self.y
    
    if self.moving[0]:
      newY -= self.speed/diagonal
    if self.moving[1]:
      newX -= self.speed/diagonal
    if self.moving[2]:
      newY += self.speed/diagonal
    if self.moving[3]:
      newX += self.speed/diagonal

    self.x, self.y, flag = tileCollision(newX, newY, self.x, self.y, self.radius)
    
    if self.moving[1] and not self.moving[3]:
      self.walkRight = False
    elif self.moving[3] and not self.moving[1]:
      self.walkRight = True

    if self.timeToShoot == 0 and (self.shooting[0] or self.shooting[1] or self.shooting[2] or self.shooting[3]):
      self.timeToShoot = self.shootCD
      self.shootState = self.shootMax
      self.walkState = 0
      self.walkAnimDir = 1
      self.animTimer = ANIMDELAY
      if self.shooting[0]:
        allSprites.append(bullet(True, self.bulletSize, self.x, self.y, 0, -self.bulletSpeed, self.damage, self.bulletProperties, 1), 1)
      elif self.shooting[1]:
        allSprites.append(bullet(True, self.bulletSize, self.x, self.y, -self.bulletSpeed, 0, self.damage, self.bulletProperties, 1), 1)
      elif self.shooting[2]:
        allSprites.append(bullet(True, self.bulletSize, self.x, self.y, 0, self.bulletSpeed, self.damage, self.bulletProperties, 1), 1)
      else:
        allSprites.append(bullet(True, self.bulletSize, self.x, self.y, self.bulletSpeed, 0, self.damage, self.bulletProperties, 1), 1)
    self.timeToShoot = max(0, self.timeToShoot-1)

    self.iFrameCounter = max(0, self.iFrameCounter - 1)
    if self.iFrameCounter % self.iFrameBlink == 0:
      self.iFrameVisible = not self.iFrameVisible
    if self.iFrameCounter == 0:
      self.iFrameVisible = True
    
    if self.shootState != 0:
      self.animTimer -= 1
      if self.animTimer == 0:
        self.animTimer = ANIMDELAY
        self.shootState -= 1
    elif self.moving[0] or self.moving[1] or self.moving[2] or self.moving[3]:
      self.animTimer -= 1
      if self.animTimer == 0:
        self.animTimer = ANIMDELAY
        self.walkState += self.walkAnimDir
        if self.walkState > self.walkMax:
          self.walkAnimDir *= -1
          self.walkState += 2*self.walkAnimDir
        if self.walkState < 0:
          self.walkAnimDir *= -1
          self.walkState += 2*self.walkAnimDir
    else:
      self.animTimer = ANIMDELAY
      self.walkState = 0
      
  def draw(self):
    displayImage = -1
    if self.deathFrame != 0:
      displayImage = newImage(OrangeFlopper, self.deathFrame * SHOOTSTRETCH, self.deathFrame * SHOOTSTRETCH, self.walkRight, False, 0)
      displayRect = displayImage.get_rect()
      displayRect.center = (self.x, self.y)
      screen.blit(displayImage, displayRect)
    elif self.iFrameVisible:
      if self.shootState != 0:
        if self.shooting[1]:
          displayImage = newImage(OrangeFlopper, -self.shootState*SHOOTSTRETCH, self.shootState*SHOOTSTRETCH, False, False, 0)
        elif self.shooting[3]:
          displayImage = newImage(OrangeFlopper, -self.shootState*SHOOTSTRETCH, self.shootState*SHOOTSTRETCH, True, False, 0)
        else:
          displayImage = newImage(OrangeFlopper, -self.shootState*SHOOTSTRETCH, self.shootState*SHOOTSTRETCH, self.walkRight, False, 0)
      else:
        displayImage = newImage(OrangeFlopper, self.walkState*WALKSQUISH, -self.walkState*WALKSQUISH, self.walkRight, False, 0)

      displayRect = displayImage.get_rect()
      displayRect.center = (self.x, self.y)
      screen.blit(displayImage, displayRect)

  def hurt(self):
    if self.iFrameCounter == 0:
      self.iFrameCounter = self.iFrames
      self.curHealth -= 1

  def pickup(self, itemType):
    tmp = itemType()
    if itemType.bulletProperties:
      self.bulletProperties.append(itemType())
    self.bulletSpeed = max(4, min(self.bulletSpeed + itemType.bulletSpeed, 15))
    self.bulletSize = min(max(self.bulletSize + itemType.bulletSize, 5), playerInstance.radius)
    self.bulletKB = min(3, self.bulletKB + itemType.bulletKB)
    self.damage = max(self.damage + itemType.damage, 1)
    self.shootCD = min(self.shootCD // itemType.shootCD, 60)
    self.speed = min(max(1, self.speed + itemType.speed), 10)
    self.maxHealth = max(1, self.maxHealth + itemType.maxHealth)
    self.curHealth = self.maxHealth
    allSprites.append(messageEffect(itemType.name, itemType.message), 2)
    curRoom.curItem = -1

class bullet():
  def __init__(self, friendly, size, startX, startY, xVelocity, yVelocity, damage, properties, kb):
    self.kill = False
    self.friendly = friendly
    self.x = startX
    self.y = startY
    self.xVelocity = xVelocity
    self.yVelocity = yVelocity
    self.radius = size
    self.properties = copy.deepcopy(properties)
    self.damage = damage
    self.kb = kb
  
  def update(self):
    self.x, self.y, flag = tileCollision(self.x+self.xVelocity, self.y+self.yVelocity, self.x, self.y, self.radius)
    if flag or self.x < -self.radius or self.x > self.radius + WIDTH or self.y < -self.radius or self.y > self.radius + HEIGHT:
      self.kill = True
    if self.friendly:
      for i in enemies:
        if circleCircle(self.x, self.y, self.radius, i.x, i.y, i.radius):
          i.hurt(self.damage, self.xVelocity * self.kb, self.yVelocity * self.kb)
          self.kill = True
          break
    else:
      if circleCircle(self.x, self.y, self.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
        self.kill = True

    for i in self.properties:
      i.modify(self)

    if self.kill:
      allSprites.append(popEffect(self.x, self.y, self.radius*3), 1)

  def draw(self):
    if self.friendly:
      displayImage = newImage(BubbleFriendly, -(40-self.radius), -(40-self.radius), False, False, 0)
      displayRect = displayImage.get_rect()
      displayRect.center = (self.x, self.y)
      screen.blit(displayImage, displayRect)
    else:
      displayImage = newImage(BubbleEnemy, -(40 - self.radius), -(40 - self.radius), False, False, 0)
      displayRect = displayImage.get_rect()
      displayRect.center = (self.x, self.y)
      screen.blit(displayImage, displayRect)

class wall():
  def __init__(self, tileSet, idx, x, y):
    self.tileSet = tileSet
    self.idx = idx
    self.x = x
    self.y = y
    self.size = 20
    self.displayRect = tileSet[idx].get_rect()
    self.displayRect.center = (x, y)
    self.kill = False
    
  def update(self):
    pass

  def draw(self):
    screen.blit(self.tileSet[self.idx], self.displayRect)

class room():
  def __init__(self, enemies, special, tileSet, up, left, down, right):
    self.up = up
    self.left = left
    self.down = down
    self.right = right
    self.enemies = []
    self.tiles = [[-1 for y in range(GRIDHEIGHT)] for x in range(GRIDWIDTH)]
    self.blocked = [[False for y in range(GRIDHEIGHT)] for x in range(GRIDWIDTH)]
    self.cleared = False
    self.special = special
    self.aiGrid = [[-1 for y in range(GRIDHEIGHT)] for x in range(GRIDWIDTH)]
    self.aiGridMelee = [[-1 for y in range(GRIDHEIGHT)] for x in range(GRIDWIDTH)]
    self.curItem = -1

    for i in range(GRIDWIDTH):
      self.blocked[i][0] = True
      self.blocked[i][GRIDHEIGHT-1] = True

    for i in range(GRIDHEIGHT):
      self.blocked[0][i] = True
      self.blocked[GRIDWIDTH-1][i] = True
    
    if special == 0:
      pass
    elif special == 1:
      if len(allItems) > 0:
        tmp = allItems[random.randint(0, len(allItems) - 1)]
        allItems.remove(tmp)
        self.curItem = item(WIDTH / 2, HEIGHT / 2, tmp, tmp.image)
    elif special == 2:
      pass
    else:
      obstacleCount = random.randint(0, 10)
      obstacles = [16, 146, 341, 56, 325, 471, 273, 84, 295, 457, 216, 511]
      for i in range(obstacleCount):
        x = random.randint(1, GRIDWIDTH-4)
        y = random.randint(1, GRIDHEIGHT-4)
        obstacleType = random.randint(1, 511)
        
        if random.randint(0, 1) == 1:
          obstacleType = obstacles[random.randint(0, len(obstacles)-1)]
          
        for i in range(3):
          for j in range(3):
            if ((obstacleType & (1 << (i * 3 + j))) != 0):
              self.blocked[x+i][y+j] = True

    for i in range(1, GRIDWIDTH-1):
      self.blocked[i][GRIDHEIGHT//2] = False
      self.blocked[i][GRIDHEIGHT//2-1] = False

    for i in range(1, GRIDHEIGHT-1):
      self.blocked[GRIDWIDTH//2][i] = False
      self.blocked[GRIDWIDTH//2-1][i] = False
    
    for i in range(GRIDWIDTH):
      for j in range(GRIDHEIGHT):
        if self.blocked[i][j]:
          self.tiles[i][j] = wall(tileSet, random.randint(0, len(tileSet)-1), i*40+20, j*40+20)
        else:
          self.tiles[i][j] = wall(Water, random.randint(0, len(Water)-1), i*40+20, j*40+20)

    if self.up:
      self.tiles[GRIDWIDTH//2][0] = wall(Door, 0, (GRIDWIDTH//2)*40+20, 20)
      self.tiles[GRIDWIDTH//2-1][0] = wall(Door, 0, (GRIDWIDTH//2-1)*40+20, 20)
    if self.left:
      self.tiles[0][GRIDHEIGHT//2] = wall(Door, 0, 20, (GRIDHEIGHT//2)*40+20)
      self.tiles[0][GRIDHEIGHT//2-1] = wall(Door, 0, 20, (GRIDHEIGHT//2-1)*40+20)
    if self.down:
      self.tiles[GRIDWIDTH//2][GRIDHEIGHT-1] = wall(Door, 0, (GRIDWIDTH//2)*40+20, (GRIDHEIGHT-1)*40+20)
      self.tiles[GRIDWIDTH//2-1][GRIDHEIGHT-1] = wall(Door, 0, (GRIDWIDTH//2-1)*40+20, (GRIDHEIGHT-1)*40+20)
    if self.right:
      self.tiles[GRIDWIDTH-1][GRIDHEIGHT//2] = wall(Door, 0, (GRIDWIDTH-1)*40+20, (GRIDHEIGHT//2)*40+20)
      self.tiles[GRIDWIDTH-1][GRIDHEIGHT//2-1] = wall(Door, 0, (GRIDWIDTH-1)*40+20, (GRIDHEIGHT//2-1)*40+20)

    self.aiGrid = bfs(GRIDWIDTH // 2, GRIDHEIGHT // 2, self, False)
    enemyCount = 0
    if self.special == -1:
      enemyCount = random.randint(4, 6)
    elif self.special == 2:
      enemyCount = random.randint(7, 10)
    notAllowed = [(WIDTH/2, 0), (WIDTH/2, HEIGHT), (0, HEIGHT/2), (WIDTH, HEIGHT/2)]
    for i in range(enemyCount):
      while True:
        spawnX, spawnY = random.randint(1, GRIDWIDTH-2), random.randint(1, GRIDHEIGHT-2)
        if self.blocked[spawnX][spawnY] == False and self.aiGrid[spawnX][spawnY] != -1:
          flag = True
          for j in self.enemies:
            if circleCircle(spawnX * 40 + 20, spawnY * 40 + 20, playerInstance.radius, j.x, j.y, j.radius):
              flag = False
              break
          for j in notAllowed:
            if circleCircle(j[0], j[1], 100, spawnX * 40 + 20, spawnY * 40 + 20, playerInstance.radius):
              flag = False
              break
          if flag:
            enemyType = floors[floorIdx][1][random.randint(0, 2)]
            self.enemies.append(enemy(spawnX * 40 + 20, spawnY * 40 + 20, enemyType.image, enemyType(), enemyType.stand, enemyType.kb, enemyType.shootCD, enemyType.speed, enemyType.hp))
            break

  def clear(self):
    self.cleared = True
    playerInstance.curHealth = playerInstance.maxHealth
    if self.up:
      self.tiles[GRIDWIDTH//2][0].kill = True
      self.tiles[GRIDWIDTH//2-1][0].kill = True
      self.tiles[GRIDWIDTH//2][0] = wall(Water, random.randint(0, len(Water)-1), (GRIDWIDTH//2)*40+20, 20)
      self.tiles[GRIDWIDTH//2-1][0] = wall(Water, random.randint(0, len(Water)-1), (GRIDWIDTH//2-1)*40+20, 20)
      allSprites.append(self.tiles[GRIDWIDTH//2][0], 0)
      allSprites.append(self.tiles[GRIDWIDTH//2-1][0], 0)
      self.blocked[GRIDWIDTH//2][0] = False
      self.blocked[GRIDWIDTH//2-1][0] = False
    if self.left:
      self.tiles[0][GRIDHEIGHT//2].kill = True
      self.tiles[0][GRIDHEIGHT//2-1].kill = True
      self.tiles[0][GRIDHEIGHT//2] = wall(Water, random.randint(0, len(Water)-1), 20, (GRIDHEIGHT//2)*40+20)
      self.tiles[0][GRIDHEIGHT//2-1] = wall(Water, random.randint(0, len(Water)-1), 20, (GRIDHEIGHT//2-1)*40+20)
      allSprites.append(self.tiles[0][GRIDHEIGHT//2], 0)
      allSprites.append(self.tiles[0][GRIDHEIGHT//2-1], 0)
      self.blocked[0][GRIDHEIGHT//2] = False
      self.blocked[0][GRIDHEIGHT//2-1] = False
    if self.down:
      self.tiles[GRIDWIDTH//2][GRIDHEIGHT-1].kill = True
      self.tiles[GRIDWIDTH//2-1][GRIDHEIGHT-1].kill = True
      self.tiles[GRIDWIDTH//2][GRIDHEIGHT-1] = wall(Water, random.randint(0, len(Water)-1), (GRIDWIDTH//2)*40+20, (GRIDHEIGHT-1)*40+20)
      self.tiles[GRIDWIDTH//2-1][GRIDHEIGHT-1] = wall(Water, random.randint(0, len(Water)-1), (GRIDWIDTH//2-1)*40+20, (GRIDHEIGHT-1)*40+20)
      allSprites.append(self.tiles[GRIDWIDTH//2][GRIDHEIGHT-1], 0)
      allSprites.append(self.tiles[GRIDWIDTH//2-1][GRIDHEIGHT-1], 0)
      self.blocked[GRIDWIDTH//2][GRIDHEIGHT-1] = False
      self.blocked[GRIDWIDTH//2-1][GRIDHEIGHT-1] = False
    if self.right:
      self.tiles[GRIDWIDTH-1][GRIDHEIGHT//2].kill = True
      self.tiles[GRIDWIDTH-1][GRIDHEIGHT//2-1].kill = True
      self.tiles[GRIDWIDTH-1][GRIDHEIGHT//2] = wall(Water, random.randint(0, len(Water)-1), (GRIDWIDTH-1)*40+20, (GRIDHEIGHT//2)*40+20)
      self.tiles[GRIDWIDTH-1][GRIDHEIGHT//2-1] = wall(Water, random.randint(0, len(Water)-1), (GRIDWIDTH-1)*40+20, (GRIDHEIGHT//2-1)*40+20)
      allSprites.append(self.tiles[GRIDWIDTH-1][GRIDHEIGHT//2], 0)
      allSprites.append(self.tiles[GRIDWIDTH-1][GRIDHEIGHT//2-1], 0)
      self.blocked[GRIDWIDTH-1][GRIDHEIGHT//2] = False
      self.blocked[GRIDWIDTH-1][GRIDHEIGHT//2-1] = False

    if self.special == 2:
      allSprites.append(hole(WIDTH/2, HEIGHT/2), 1)
      if len(allItems) != 0:
        tmp = allItems[random.randint(0, len(allItems)-1)]
        allItems.remove(tmp)
        self.curItem = item(WIDTH/2, HEIGHT/2+80, tmp, tmp.image)
        allSprites.append(self.curItem, 1)
        allSprites.append(explosionEffect(WIDTH/2, HEIGHT/2, playerInstance.radius*2, 3, 3, 0), 1)

  def updateGrid(self):
    self.aiGrid = bfs(round((playerInstance.x - 20) / 40), round((playerInstance.y - 20) / 40), curRoom, False)
    self.aiGridMelee = bfs(round((playerInstance.x - 20) / 40), round((playerInstance.y - 20) / 40), curRoom, True)

class hudMap():
  def __init__(self):
    self.kill = False
    self.open = False
    self.gap = 5
    self.size = 30
    self.roomRect = pygame.Rect(0, 0, self.size, self.size)

  def update(self):
    pass

  def draw(self):
    dir = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
    if self.open:
      for x in range(MAPSIZE):
        for y in range(MAPSIZE):
          if curFloor[x][y] != -1 and curFloor[x][y].cleared:
            for i in dir:
              nextX, nextY = x + i[0], y + i[1]
              if 0 <= nextX <= MAPSIZE-1 and 0 <= nextY <= MAPSIZE-1 and curFloor[nextX][nextY] != -1:
                self.roomRect.center = (WIDTH - (MAPSIZE * self.size + MAPSIZE * self.gap + self.gap + self.size / 2) + (nextX * self.size + nextX * self.gap + self.gap + self.size / 2), nextY * self.size + nextY * self.gap + self.gap + self.size / 2)
                if curFloor[nextX][nextY].cleared == False and curFloor[nextX][nextY].special == -1:
                  pygame.draw.rect(screen, (39,39,39), self.roomRect)
                elif curFloor[nextX][nextY].special == 1:
                  pygame.draw.rect(screen, (212, 175, 55), self.roomRect)
                elif curFloor[nextX][nextY].special == 2:
                  pygame.draw.rect(screen, (138, 3, 3), self.roomRect)
                else:
                  pygame.draw.rect(screen, (182, 182, 182), self.roomRect)

      pygame.draw.circle(screen, (255, 69, 0), (WIDTH - (MAPSIZE * self.size + MAPSIZE * self.gap + self.gap + self.size / 2) + (curX * self.size + curX * self.gap + self.gap + self.size / 2), curY * self.size + curY * self.gap + self.gap + self.size / 2), self.size/3)


class hudHealth():
  def __init__(self):
    self.kill = False
    self.lastHealth = playerInstance.curHealth
    self.gap = 5
    self.animTimer = 0
    self.displayHealth = self.lastHealth

  def update(self):
    if self.displayHealth > playerInstance.curHealth:
      for i in range(self.lastHealth):
        if i > playerInstance.curHealth - 1:
          allSprites.append(explosionEffect((i % 7) * 20 + 10 + self.gap * ((i % 7) +1), ((i // 7) * 20) + self.gap * ((i // 7) + 1) + 10, 20, 2, 2, 0), 2)
      self.displayHealth = self.lastHealth
    elif self.displayHealth < playerInstance.curHealth:
      self.animTimer = max(0, self.animTimer - 1)
      if self.animTimer == 0:
        self.animTimer = ANIMDELAY
        self.displayHealth += 1
    self.lastHealth = playerInstance.curHealth

  def draw(self):
    if playerInstance.kill == False:
      for i in range(self.displayHealth):
        displayRect = Heart.get_rect()
        displayRect.center = ((i % 7) * 20 + 10 + self.gap * ((i % 7) +1), ((i // 7) * 20) + self.gap * ((i // 7) + 1) + 10)
        screen.blit(Heart, displayRect)

class enemy():
  def __init__(self, posX, posY, image, attack, standing, kb, shootCD, speed, hp):
    self.kill = False
    self.radius = playerInstance.radius

    self.image = image
    self.attack = attack

    self.x = posX
    self.y = posY

    self.deathFrame = 0
    self.deathMax = 3
    self.deathBubbles = 5

    self.timeToShoot = random.randint(60, 120)
    self.shootCD = shootCD

    self.speed = speed
    self.hp = hp
    self.standRange = standing
    self.kbMulti = kb

    self.nextX = round((self.x-20)/40)
    self.nextY = round((self.y-20)/40)
    self.halt = 40

    self.shootState = 0
    self.shootMax = 4
    self.shootFaceLock = True

    self.walkRight = True
    self.walkState = 0
    self.walkMax = 5
    self.walkAnimDir = 1

    self.animTimer = ANIMDELAY

  def update(self):
    self.animTimer = max(0, self.animTimer - 1)
    self.halt = max(0, self.halt - 1)

    if (round((self.x-20)/40) <= 0 or round((self.x-20)/40) >= GRIDWIDTH-1 or round((self.y-20)/40) <= 0 or round((self.y-20)/40) >= GRIDHEIGHT-1) and self.deathFrame == 0:
      self.deathFrame = 1

    if self.timeToShoot == -1:
      self.shootState = self.shootMax
      self.timeToShoot = self.shootCD + random.randint(-20, 20)
      self.walkState = 0
      self.walkAnimDir = 1
      if playerInstance.x > self.x:
        self.shootFaceLock = True

    self.timeToShoot = max(0, self.timeToShoot - 1)

    if self.hp <= 0 and self.deathFrame == 0:
      self.deathFrame = 1

    if self.deathFrame == 3:
      if self in enemies:
        enemies.remove(self)

    if self.deathFrame != 0 and self.animTimer == 0:
      self.animTimer = ANIMDELAY
      self.deathFrame += 1

    if self.deathFrame > self.deathMax:
      allSprites.append(explosionEffect(self.x, self.y, self.radius*2, self.deathBubbles, 3, 0), 1)
      self.kill = True

    if self.halt == 0 and self.deathFrame == 0:
      ai = curRoom.aiGrid
      blockingA = 0
      if self.standRange == 0:
        ai = curRoom.aiGridMelee
        blockingA = 4

      if ai[round((self.x-20)/40)][round((self.y-20)/40)] == -1 and self.deathFrame == 0:
        self.deathFrame = 1

      if self.nextX * 40 + 20 > self.x:
        self.walkRight = True
      else:
        self.walkRight = False

      if self.nextX == round((self.x-20)/40) and self.nextY == round((self.y-20)/40):
        curGridX = round((self.x-20)/40)
        curGridY = round((self.y-20)/40)
        bestWays = []
        best = abs(ai[curGridX][curGridY] - self.standRange) - blockingA
        dir = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        for i in range(4):
          checkX = curGridX + dir[i][0]
          checkY = curGridY + dir[i][1]
          if ai[checkX][checkY] != -1:
            if abs(ai[checkX][checkY] - self.standRange) < best:
              best = abs(ai[checkX][checkY] - self.standRange)
              bestWays = [dir[i]]
            elif abs(ai[checkX][checkY] - self.standRange) == best:
              bestWays.append(dir[i])

        for i in range(4, 8):
          checkX = curGridX + dir[i][0]
          checkY = curGridY + dir[i][1]
          if ai[checkX][checkY] != -1 and ai[checkX][curGridY] != -1 and ai[curGridX][checkY] != -1:
            if abs(ai[checkX][checkY] - self.standRange) < best:
              best = abs(ai[checkX][checkY] - self.standRange)
              bestWays = [dir[i]]
            elif abs(ai[checkX][checkY] - self.standRange) == best:
              bestWays.append(dir[i])

        if len(bestWays) == 0 or abs(ai[round((self.x-20)/40)][round((self.y-20)/40)]-self.standRange) == best:
          if self.standRange != 0:
            self.halt = 30
        else:
          a, b = bestWays[random.randint(0, len(bestWays) - 1)]
          self.nextX += a
          self.nextY += b

      if self.halt == 0:
        walkAngle = angle(self.x, self.y, self.nextX*40+20, self.nextY*40+20)
        walkX, walkY = -1, -1
        if self.x < self.nextX*40+20:
          walkX = min(self.nextX*40+20, self.x + math.sin(walkAngle) * self.speed)
        else:
          walkX = max(self.nextX*40+20, self.x + math.sin(walkAngle) * self.speed)
        if self.y < self.nextY*40+20:
          walkY = min(self.nextY*40+20, self.y + math.cos(walkAngle) * self.speed)
        else:
          walkY = max(self.nextY*40+20, self.y + math.cos(walkAngle) * self.speed)

        self.x, self.y, tmp = tileCollision(walkX, walkY, self.x, self.y, self.radius)

        ai[self.nextX][self.nextY] += 2

    self.x, self.y, self.deathFrame, self.timeToShoot = self.attack.attack(self.x, self.y, self.deathFrame, self.timeToShoot)

  def draw(self):
    displayImage = -1
    if self.deathFrame != 0:
      displayImage = newImage(self.image, self.deathFrame * SHOOTSTRETCH, self.deathFrame * SHOOTSTRETCH, self.walkRight, False, 0)
    elif self.shootState != 0:
      if self.animTimer == 0:
        self.animTimer = ANIMDELAY
        self.shootState -= 1
      displayImage = newImage(self.image, -self.shootState*SHOOTSTRETCH, self.shootState*SHOOTSTRETCH, self.shootFaceLock, False, 0)
    elif self.halt == 0:
      if self.animTimer == 0:
        self.animTimer = ANIMDELAY
        self.walkState += self.walkAnimDir
        if self.walkState > self.walkMax:
          self.walkAnimDir *= -1
          self.walkState += 2 * self.walkAnimDir
        if self.walkState < 0:
          self.walkAnimDir *= -1
          self.walkState += 2 * self.walkAnimDir
      displayImage = newImage(self.image, self.walkState*WALKSQUISH, -self.walkState*WALKSQUISH, self.walkRight, False, 0)
    else:
      tmp = False
      if self.x < playerInstance.x:
        tmp = True
      displayImage = newImage(self.image, 0, 0, tmp, False, 0)

    if self.halt != 0:
      self.walkState = 0
      self.walkAnimDir = 1

    displayImage = newImage(displayImage, -(playerInstance.radius-self.radius), -(playerInstance.radius-self.radius), False, False, 0)
    displayRect = displayImage.get_rect()
    displayRect.center = (self.x, self.y)
    screen.blit(displayImage, displayRect)

  def hurt(self, damage, xVelocity, yVelocity):
    for i in range(math.floor(self.kbMulti)):
      self.x, self.y, tmp = tileCollision(self.x + xVelocity, self.y + yVelocity, self.x, self.y, self.radius)
    self.hp -= damage
    self.halt = 0

class enemyGreenFlopper():
  image = GreenFlopper
  kb = 3
  shootCD = 0
  speed = 3
  stand = 0
  hp = 4
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
    return (x, y, deathFrame, timeToShoot)

class enemyLongFlopper():
  image = LongFlopper
  kb = 5
  shootCD = 180
  speed = 2
  stand = 6
  hp = 2
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
    if timeToShoot == 0:
      shootAngle = angle(x, y, playerInstance.x, playerInstance.y)
      allSprites.append(bullet(False, 15, x, y, math.sin(shootAngle) * 5, math.cos(shootAngle) * 5, 1, [], 0), 1)
      timeToShoot = -1
    return (x, y, deathFrame, timeToShoot)

class enemyBlobFlopper():
  image = BlobFlopper
  kb = 2
  shootCD = 0
  speed = 3
  stand = 0
  hp = 5
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
    elif deathFrame == 3 and timeToShoot <= 1000:
      timeToShoot = 9999
      childCount = random.randint(2, 3)
      childType = enemyBlobFlopper()
      for i in range(childCount):
        child = enemy(x, y, childType.image, enemyGreenFlopper(), childType.stand, 3, childType.shootCD, childType.speed + 1, 2)
        child.radius //= 3
        xPush = random.randint(-10, 10)
        yPush = random.randint(-10, 10)
        child.x, child.y, tmp = tileCollision(xPush + x, yPush + y, x, y, child.radius)
        allSprites.append(child, 1)
        enemies.append(child)
    return (x, y, deathFrame, timeToShoot)

class enemyBlueFlopper():
  image = BlueFlopper
  kb = 2.5
  shootCD = 0
  speed = 3.5
  stand = 0
  hp = 5
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
    return (x, y, deathFrame, timeToShoot)

class enemyIceFlopper():
  image = IceFlopper
  kb = 3
  shootCD = 120
  speed = 3
  stand = 5
  hp = 4
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
    if timeToShoot == 0:
      shootAngle = angle(x, y, playerInstance.x, playerInstance.y)
      allSprites.append(bullet(False, 15, x, y, math.sin(shootAngle) * 5, math.cos(shootAngle) * 5, 1, [], 0), 1)
      timeToShoot = -1
      extraShots = random.randint(1, 2)
      for i in range(extraShots):
        extraAngle = angle(x, y, playerInstance.x + random.randint(-90, 90), playerInstance.y + random.randint(-90, 90))
        extraSpeed = 5 + (random.randint(-100, 100) / 100)
        allSprites.append(bullet(False, 15, x, y, math.sin(extraAngle) * extraSpeed, math.cos(extraAngle) * extraSpeed, 1, [], 0), 1)
    return (x, y, deathFrame, timeToShoot)

class enemyAnglerFlopper():
  image = AnglerFlopper
  kb = 1
  shootCD = 0
  speed = 4
  stand = 0
  hp = 12
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
    return (x, y, deathFrame, timeToShoot)

class enemyGoldFlopper():
  image = GoldFlopper
  kb = 2
  shootCD = 0
  speed = 4
  stand = 0
  hp = 6
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
    return (x, y, deathFrame, timeToShoot)

class enemySquareFlopper():
  image = SquareFlopper
  kb = 4
  shootCD = 360
  speed = 5
  stand = 999
  hp = 5
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        playerInstance.hurt()
    if timeToShoot == 0:
      timeToShoot = -1
      spawnX, spawnY, tmp = tileCollision(x + random.randint(-10, 10), y + random.randint(-10, 10), x, y, playerInstance.radius)
      spawnType = floors[random.randint(0, 1)][1][random.randint(0, 2)]
      spawn = enemy(spawnX, spawnY, spawnType.image, spawnType(), spawnType.stand, spawnType.kb, spawnType.shootCD, spawnType.speed, spawnType.hp)
      allSprites.append(spawn, 1)
      enemies.append(spawn)
      allSprites.append(explosionEffect(spawnX, spawnY, playerInstance.radius * 2, 3, 3, 0), 1)

    return (x, y, deathFrame, timeToShoot)

class enemyBombFlopper():
  image = BombFlopper
  kb = 2
  shootCD = 0
  speed = 5
  stand = 0
  hp = 10
  def attack(self, x, y, deathFrame, timeToShoot):
    if deathFrame == 0:
      if circleCircle(x, y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
        deathFrame = 1
    elif deathFrame == 3:
      #explosionEffect(x, y, size, density, frameMax, damage)
      allSprites.append(explosionEffect(x, y, 100, 10, 5, 5), 1)
    return (x, y, deathFrame, timeToShoot)

class item():
  def __init__(self, x, y, itemType, image):
    self.kill = False
    self.displayImage = image
    self.displayRect = self.displayImage.get_rect()
    self.displayRect.center = (x, y)
    self.itemType = itemType
    self.radius = 20
    self.x = x
    self.y = y

  def update(self):
    if circleCircle(self.x, self.y, self.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
      playerInstance.pickup(self.itemType)
      self.kill = True

  def draw(self):
    screen.blit(self.displayImage, self.displayRect)

class percItem():
  bulletProperties = False
  bulletSpeed = random.randint(0, 1)
  bulletSize = random.randint(0, 1)
  bulletKB = random.randint(0, 1)
  damage = random.randint(1, 2)
  shootCD = random.randint(1, 2)
  speed = random.randint(1, 2)
  maxHealth = random.randint(1, 2)
  name = "Perc 30"
  message = "Perk Up"
  image = PercItem

class roidsItem():
  bulletProperties = False
  bulletSpeed = 0
  bulletSize = 0
  bulletKB = 0
  damage = 3
  shootCD = 1
  speed = 0
  maxHealth = 1
  name = "Roids"
  message = "Damage and Health Up"
  image = RoidsItem

class chairItem():
  bulletProperties = True
  bulletSpeed = 0
  bulletSize = 0
  bulletKB = 0
  damage = 0
  shootCD = 1
  speed = 2
  maxHealth = 0
  name = "Gaming Chair"
  message = "Edison Ling 500ms Aim"
  image = ChairItem
  def modify(self, bubble):
    closestDist = 99999999
    closest = -1
    for i in enemies:
      check = distance(bubble.x, bubble.y, i.x, i.y)
      if check < closestDist:
        closestDist = check
        closest = i
    if closestDist < 120:
      newAngle = angle(bubble.x, bubble.y, closest.x, closest.y)
      bubble.xVelocity += math.sin(newAngle)
      bubble.yVelocity += math.cos(newAngle)

class airburstItem():
  bulletProperties = True
  bulletSpeed = -1
  bulletSize = 0
  bulletKB = 0
  damage = -1
  shootCD = 0.8
  speed = 0
  maxHealth = 0
  name = "Airburst"
  message = "0-0-2"
  image = AirburstItem
  def __init__(self):
    self.timer = 0

  def modify(self, bubble):
    self.timer += 1
    if self.timer >= 10:
      childProperties = copy.deepcopy(bubble.properties)
      for i in childProperties:
        if i.name == "Airburst":
          childProperties.remove(i)
          break
      bubble.kill = True
      bubble.properties.clear()
      for i in range(4):
        allSprites.append(bullet(True, bubble.radius // 2, bubble.x, bubble.y, bubble.xVelocity + random.randint(-3, 3), bubble.yVelocity + random.randint(-3, 3), max(1, bubble.damage // 3), childProperties, 0.8), 1)

class buckyItem():
  bulletProperties = True
  bulletSpeed = 0
  bulletSize = 0
  bulletKB = 0
  damage = 0
  shootCD = 0.7
  speed = 0
  maxHealth = 0
  name = "Shotgun"
  message = "0-0-0"
  image = BuckyItem

  def modify(self, bubble):
    childProperties = copy.deepcopy(bubble.properties)
    for i in childProperties:
      if i.name == "Shotgun":
        childProperties.remove(i)
        break
    bubble.kill = True
    bubble.properties.clear()
    for i in range(4):
      allSprites.append(bullet(True, bubble.radius, bubble.x, bubble.y, bubble.xVelocity + random.randint(-2, 2), bubble.yVelocity + random.randint(-2, 2), max(1, bubble.damage // 3), childProperties, 0.8), 1)

class balloonItem():
  bulletProperties = True
  bulletSpeed = -1
  bulletSize = 0
  bulletKB = 2
  damage = 1
  shootCD = 0.9
  speed = 0
  maxHealth = 0
  name = "Water Balloon"
  message = "splash damage"
  image = BalloonItem
  def modify(self, bubble):
    if bubble.kill:
      allSprites.append(explosionEffect(bubble.x, bubble.y, 50, 4, 4, max(1, bubble.damage//3)), 1)

class boomerangItem():
  bulletProperties = True
  bulletSpeed = 1
  bulletSize = 3
  bulletKB = 1
  damage = 5
  shootCD = 1.5
  speed = 0
  maxHealth = 0
  name = "Boomerang Bullets"
  message = "Damage At What Cost?"
  image = BoomerangItem
  def __init__(self):
    self.timer = 0
    self.newXVelocity = -1
    self.newYVelocity = -1

  def modify(self, bubble):
    self.timer += 1
    if self.timer == 15:
      self.newXVelocity = bubble.xVelocity*-1
      self.newYVelocity = bubble.yVelocity*-1
    elif self.timer > 15:
      bubble.xVelocity = bubble.xVelocity * 0.95 + self.newXVelocity * 0.05
      bubble.yVelocity = bubble.yVelocity * 0.95 + self.newYVelocity * 0.05

class jacketItem():
  bulletProperties = False
  bulletSpeed = 0
  bulletSize = 0
  bulletKB = 0
  damage = 0
  shootCD = 1
  speed = -1
  maxHealth = 5
  name = "Flak Jacket"
  message = "Explosion Proof"
  image = JacketItem
  def __init__(self):
    playerInstance.blastResistance = True

class wheelItem():
  bulletProperties = False
  bulletSpeed = 1
  bulletSize = 0
  bulletKB = 0
  damage = 0
  shootCD = 1.5
  speed = 4
  maxHealth = 0
  name = "The Wheel"
  message = "The Fast and the Furious"
  image = WheelItem

class arthritisItem():
  bulletProperties = False
  bulletSpeed = 2
  bulletSize = 0
  bulletKB = 0
  damage = -1
  shootCD = 3
  speed = 0
  maxHealth = 0
  name = "Arthritis"
  message = "21.249 cps"
  image = ArthritisItem

class popEffect():
  def __init__(self, x, y, size):
    self.kill = False
    self.animCounter = ANIMDELAY
    self.displayImage = newImage(BubblePop, -(120-size), -(120-size), False, False, random.randint(0, 359))
    self.displayRect = self.displayImage.get_rect()
    self.displayRect.center = (x, y)

  def update(self):
    self.animCounter = max(0, self.animCounter - 1)
    if self.animCounter == 0:
      self.kill = True

  def draw(self):
    screen.blit(self.displayImage, self.displayRect)

class hole():
  def __init__(self, x, y):
    self.kill = False
    self.x = x
    self.y = y
    self.openTime = 40
    self.animTimer = 0
    self.rotation = 0

  def update(self):
    self.animTimer = max(0, self.animTimer - 1)
    if self.animTimer == 0:
      self.animTimer = ANIMDELAY
      self.rotation += 5
      self.rotation %= 360

    self.openTime = max(0, self.openTime - 1)
    if self.openTime == 0 and circleCircle(self.x, self.y, playerInstance.radius, playerInstance.x, playerInstance.y, playerInstance.radius):
      global nextFloor
      nextFloor = True

  def draw(self):
    displayImage = newImage(Whirlpool, -self.openTime, -self.openTime, False, False, self.rotation)
    displayRect = displayImage.get_rect()
    displayRect.center = (self.x, self.y)
    screen.blit(displayImage, displayRect)

class explosionEffect():
  def __init__(self, x, y, size, bubbleDensity, frameMax, damage):
    self.kill = False
    self.animCounter = 0
    self.x = x
    self.y = y
    self.radius = size
    self.density = bubbleDensity
    self.frameCount = 0
    self.frameMax = frameMax
    self.damage = damage
    self.kb = 15

  def update(self):
    self.animCounter = max(0, self.animCounter - 1)
    if self.frameCount == 0 and self.damage != 0:
      if circleCircle(playerInstance.x, playerInstance.y, playerInstance.radius, self.x, self.y, self.radius) and playerInstance.blastResistance == False:
        playerInstance.hurt()
      for i in enemies:
        if circleCircle(i.x, i.y, i.radius, self.x, self.y, self.radius):
          pushAngle = angle(self.x, self.y, i.x, i.y)
          dist = distance(self.x, self.y, i.x, i.y)
          total = i.radius + self.radius
          i.hurt(self.damage, math.sin(pushAngle) * ((total - dist) / total) * self.kb, math.cos(pushAngle) * ((total - dist) / total) * self.kb)
    if self.animCounter == 0:
      for i in range(self.density):
        r = self.radius * math.sqrt(random.random())
        t = random.random() * 2 * math.pi
        allSprites.append(popEffect(self.x + r * math.cos(t), self.y + r * math.sin(t), playerInstance.radius * (2 + random.randint(-100, 100) / 100)), 1)
      self.frameCount += 1
    if self.frameCount > self.frameMax:
      self.kill = True

  def draw(self):
    pass

class messageEffect():
  def __init__(self, bigText, littleText):
    self.kill = False
    self.counter = 240
    self.curMessage = 0
    self.colourA = (255, 255, 242)
    self.colourB = (249, 241, 241)
    self.bigMessage = [BIGFONT.render(bigText, False, self.colourA), BIGFONT.render(bigText, False, self.colourB)]
    self.bigMessageRect = self.bigMessage[0].get_rect()
    self.bigMessageRect.center = (WIDTH / 2, 40)
    self.littleMessage = [LITTLEFONT.render(littleText, False, self.colourA), LITTLEFONT.render(littleText, False, self.colourB)]
    self.littleMessageRect = self.littleMessage[0].get_rect()
    self.littleMessageRect.center = (WIDTH / 2, 80)

  def update(self):
    self.counter = max(0, self.counter - 1)
    if self.counter == 0:
      self.kill = True
    if self.counter % 5 == 0:
      if self.curMessage == 0:
        self.curMessage = 1
      else:
        self.curMessage = 0

  def draw(self):
    screen.blit(self.bigMessage[self.curMessage], self.bigMessageRect)
    screen.blit(self.littleMessage[self.curMessage], self.littleMessageRect)

#define spritegroup and important lists
allSprites = spriteGroup(3)
enemies = []
counter = 1
curFloor = [[-1 for i in range(MAPSIZE)] for j in range(MAPSIZE)]
curX = MAPSIZE // 2
curY = MAPSIZE // 2
needRestart = False
nextFloor = True
floorIdx = 0
running = True

#make the player
playerInstance = player()

#make the hud
floorMap = hudMap()
healthBar = hudHealth()

#make the current room / floors and items
floors = [(Sand, [enemyGreenFlopper, enemyLongFlopper, enemyBlobFlopper]), (Dirt, [enemyBlueFlopper, enemyIceFlopper, enemyAnglerFlopper]), (Rock, [enemyGoldFlopper, enemySquareFlopper, enemyBombFlopper])]
curRoom = -1
allItems = [balloonItem, percItem, roidsItem, chairItem, airburstItem, buckyItem, boomerangItem, jacketItem, wheelItem, arthritisItem]

#---game loop---
while running:
  #force game to run at 60 fps for performance
  clock.tick(60)

  counter += 1
  if counter > 60:
    counter = 1
  
  #get events to update the mouse
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w:
        playerInstance.moving[0] = True
        playerInstance.moving[2] = False
      elif event.key == pygame.K_a:
        playerInstance.moving[1] = True
        playerInstance.moving[3] = False
      elif event.key == pygame.K_s:
        playerInstance.moving[2] = True
        playerInstance.moving[0] = False
      elif event.key == pygame.K_d:
        playerInstance.moving[3] = True
        playerInstance.moving[1] = False
      elif event.key == pygame.K_UP:
        playerInstance.shooting = [True, False, False, False]
      elif event.key == pygame.K_LEFT:
        playerInstance.shooting = [False, True, False, False]
      elif event.key == pygame.K_DOWN:
        playerInstance.shooting = [False, False, True, False]
      elif event.key == pygame.K_RIGHT:
        playerInstance.shooting = [False, False, False, True]
      elif event.key == pygame.K_TAB:
        floorMap.open = True
      elif event.key == pygame.K_r:
        if needRestart:
          needRestart = False
          nextFloor = True
          floorIdx = 0
          playerInstance = player()
          enemies.clear()
          allItems = [balloonItem, percItem, roidsItem, chairItem, airburstItem, buckyItem, boomerangItem, jacketItem, wheelItem, arthritisItem]
      elif event.key == pygame.K_p:
        curRoom.clear()
        enemies.clear()
    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_w:
        playerInstance.moving[0] = False
      elif event.key == pygame.K_a:
        playerInstance.moving[1] = False
      elif event.key == pygame.K_s:
        playerInstance.moving[2] = False
      elif event.key == pygame.K_d:
        playerInstance.moving[3] = False
      elif event.key == pygame.K_UP:
        playerInstance.shooting[0] = False
      elif event.key == pygame.K_LEFT:
        playerInstance.shooting[1] = False
      elif event.key == pygame.K_DOWN:
        playerInstance.shooting[2] = False
      elif event.key == pygame.K_RIGHT:
        playerInstance.shooting[3] = False
      elif event.key == pygame.K_TAB:
        floorMap.open = False
    elif event.type == pygame.QUIT:
      running = False

  #keep track of mouse inputs from the current frame and the previous frame
  pm1, pm2, pm3 = m1, m2, m3
  m1, m2, m3 = pygame.mouse.get_pressed(3)
  mousePos = pygame.mouse.get_pos()

  if nextFloor:
    if floorIdx >= len(floors):
      needRestart = True
      floorIdx = 0
    curX, curY = MAPSIZE // 2, MAPSIZE // 2
    allSprites.clear()
    curFloor = generateFloor(floors[floorIdx][0], floors[floorIdx][1])
    curRoom = curFloor[curX][curY]
    loadRoom(curRoom)
    floorIdx += 1
    nextFloor = False
    if needRestart and floorIdx == 1:
      allSprites.append(messageEffect("You Won!!!", "continue, or press R to restart"), 2)

  if curRoom.cleared == False and len(enemies) == 0:
    curRoom.clear()

  if playerInstance.x < -playerInstance.radius:
    curX -= 1
    playerInstance.x = WIDTH - 45 - playerInstance.radius
    curRoom = curFloor[curX][curY]
    loadRoom(curRoom)
  elif playerInstance.y < -playerInstance.radius:
    curY -= 1
    playerInstance.y = HEIGHT - 45 - playerInstance.radius
    curRoom = curFloor[curX][curY]
    loadRoom(curRoom)
  elif playerInstance.x > playerInstance.radius + WIDTH:
    curX += 1
    playerInstance.x = 45 + playerInstance.radius
    curRoom = curFloor[curX][curY]
    loadRoom(curRoom)
  elif playerInstance.y > playerInstance.radius + HEIGHT:
    curY += 1
    playerInstance.y = 45 + playerInstance.radius
    curRoom = curFloor[curX][curY]
    loadRoom(curRoom)

  if counter % 10 == 0:
    curRoom.updateGrid()

  #wipe the screen
  screen.fill((200, 200, 200))

  #call update and draw for all sprites in the spritegroup
  allSprites.update()
  allSprites.draw()

  #update the screen
  pygame.display.flip()