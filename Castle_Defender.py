import pygame
import math
import random
from enemy import Enemy
import button
import os
from pygame import mixer

#initialize pygame
pygame.init()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Defender By JediCubing')

clock = pygame.time.Clock()
FPS = 60

#define game variables
level = 1
high_score = 0
level_difficulty = 0
target_difficulty = 1000
DIFFICULTY_MULTIPLIER = 1.1
num_of_towers = 0
death_sound_counter = 0
playing_background_music = False
K_K = 75
K_G = 100
K_P = 150
K_R = 200 
game_over = False
next_level = False
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
max_towers = 10
TOWER_COST = 6000
ARMOUR_COST = 1000
REPAIR_COST = 2000
Enemy_Speed = 1
tower_positions = [
[SCREEN_WIDTH - 250, SCREEN_HEIGHT - 150],
[SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150],
[SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150],
[SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150],
[SCREEN_WIDTH - 50, SCREEN_HEIGHT - 150],
[SCREEN_WIDTH - 790, SCREEN_HEIGHT - 300],
[SCREEN_WIDTH - 740, SCREEN_HEIGHT - 300],
[SCREEN_WIDTH - 690, SCREEN_HEIGHT - 300],
[SCREEN_WIDTH - 640, SCREEN_HEIGHT - 300],
[SCREEN_WIDTH - 590, SCREEN_HEIGHT - 300],
]

#Load High Score
if os.path.exists('score.txt'):
	with open('score.txt', 'r') as file:
		high_score = int(file.read())


#define colors
Sky_Blue = (42, 129, 229)
GREY = (100, 100, 100)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

#define font
font = pygame.font.SysFont('Futura', 30)
font_60 = pygame.font.SysFont('Comicsansms', 60, "bold italic")


#load images
bg = pygame.image.load('img/background.png').convert_alpha()

#castle
castle_img_100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()
castle_img_50 = pygame.image.load('img/castle/castle_50.png').convert_alpha()
castle_img_25 = pygame.image.load('img/castle/castle_25.png').convert_alpha()

#tower
tower_img_100 = pygame.image.load('img/tower/tower_100.png').convert_alpha()
tower_img_50 = pygame.image.load('img/tower/tower_50.png').convert_alpha()
tower_img_25 = pygame.image.load('img/tower/tower_25.png').convert_alpha()

#bullet image
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))

#load enemies
enemy_animations = []
enemy_types = ['knight', 'goblin', 'purple_goblin', 'red_goblin']
enemy_health = [K_K, K_G, K_P, K_R]

animation_types = ['walk', 'attack', 'death']
for enemy in enemy_types:
	#load animation
	animation_list = []
	for animation in animation_types:
		#reset temporary list of images
		temp_list = []
		#define number of frames
		num_of_frames = 20
		for i in range(num_of_frames):
			img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
			e_w = img.get_width()
			e_h = img.get_height()
			img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
			temp_list.append(img)
		animation_list.append(temp_list)
	enemy_animations.append(animation_list)

#button images
#repair image
repair_img = pygame.image.load('img/repair.png').convert_alpha()
#armor image
armour_img = pygame.image.load('img/armour.png').convert_alpha()

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#Music
def Theme():
	pygame.mixer.music.load('Theme.mp3')
	pygame.mixer.music.play(-1, 5000)

Death = pygame.mixer.Sound("GameOver.wav")

#function for displaying status
def show_info():
	draw_text('Money: ' + str(castle.money), font, GREY, 10, 10)
	draw_text('Score: ' + str(castle.score), font, GREY, 180, 10)
	draw_text('High Score: ' + str(high_score), font, GREY, 180, 30)
	draw_text('Level: ' + str(level), font, GREY, SCREEN_WIDTH // 2, 10)
	draw_text('Health: ' + str(castle.health) + " / " + str(castle.max_health), font, GREY, SCREEN_WIDTH - 230, SCREEN_HEIGHT - 30)
	draw_text('$2000', font, GREY, SCREEN_WIDTH - 220 , 70)
	draw_text('$6000', font, GREY, SCREEN_WIDTH - 150, 70)
	draw_text('$1000', font, GREY, SCREEN_WIDTH - 70 , 70)
	draw_text('High Score Holder: Abheek', font, GREY, 180, 50)

#castle class
class Castle():
	def __init__(self, image100, image50, image25, x, y, scale):
		self.health = 1000
		self.max_health = self.health
		self.fired = False
		self.money = 0
		self.score = 0

		width = image100.get_width()
		height = image100.get_height()

		self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
		self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
		self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
		self.rect = self.image100.get_rect()
		self.rect.x = x
		self.rect.y = y

	def shoot(self):
		pos = pygame.mouse.get_pos()
		x_dist = pos[0] - self.rect.midleft[0]
		y_dist = -(pos[1] - self.rect.midleft[1])
		self.angle = math.degrees(math.atan2(y_dist, x_dist))
		#get mouse click
		if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 70:
			self.fired = True
			bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
			bullet_group.add(bullet)
		#reset mouse click
		if pygame.mouse.get_pressed()[0] == False:
			self.fired = False

	def draw(self):
		#check which image to use based on health
		if self.health <= 250:
			self.image = self.image25
		elif self.health <= 500:
			self.image = self.image50
		else:
			self.image = self.image100

		screen.blit(self.image, self.rect)

	def repair(self):
		if self.money >= REPAIR_COST and self.health < self.max_health:
			self.health += 500
			self.money -= 1000
			if castle.health > castle.max_health:
				castle.health = castle.max_health

	def armour(self):
		if self.money >= ARMOUR_COST:
			self.max_health += 250
			self.money -= 500

class Fades():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed 
		self.fade_counter = 0

	def fade(self):
		if self.direction == 1:
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2,	SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH,	SCREEN_HEIGHT))

		if self.direction == 2:
			pygame.draw.rect(screen, self.colour, (0 + self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH * 2 - self.fade_counter, 2, SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (0, 0 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
		self.fade_counter += self.speed *2
		return self.fade_counter >= SCREEN_WIDTH

intro = Fades(direction=1, colour=BLACK, speed=4)
death = Fades(direction=2, colour=BLACK, speed=4)

#tower class
class Tower(pygame.sprite.Sprite):
	def __init__(self, image100, image50, image25, x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		self.got_target = False
		self.angle = 0
		self.last_shot = pygame.time.get_ticks()
		width = image100.get_width()
		height = image100.get_height()
		self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
		self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
		self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
		self.image = self.image100
		self.rect = self.image100.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, enemy_group):
		self.got_target = False

		for e in enemy_group:
			if e.alive:
				target_x, target_y = e.rect.midbottom
				self.got_target = True
				break

		if self.got_target:
			x_dist = target_x - self.rect.midleft[0]
			y_dist = -(target_y - self.rect.midleft[1])
			self.angle = math.degrees(math.atan2(y_dist, x_dist))
			shot_cooldown = 1000
			#fire bullet
			if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
				self.last_shot = pygame.time.get_ticks()
				bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
				bullet_group.add(bullet)

		#check which image to use based on health
		if castle.health <= 250:
			self.image = self.image25
		elif castle.health <= 500:
			self.image = self.image50
		else:
			self.image = self.image100

#bullet class
class Bullet(pygame.sprite.Sprite):
	def __init__(self, image, x, y, angle):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.angle = math.radians(angle)#convert input angle into radians
		self.speed = 10
		#calculate the horizontal and vertical speeds based on the angle
		self.dx = math.cos(self.angle) * self.speed
		self.dy = -(math.sin(self.angle) * self.speed)
	def update(self):
		#check if bullet has gone off the screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
			self.kill()			

		#move bullet
		self.rect.x += self.dx
		self.rect.y += self.dy

class Crosshair():
	def __init__(self, scale):
		image = pygame.image.load('img/crosshair.png').convert_alpha()
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		#hide mouse
		pygame.mouse.set_visible(False)

	def draw(self):
		mx, my = pygame.mouse.get_pos()
		self.rect.center = (mx, my)
		screen.blit(self.image, self.rect)

#create castle
castle = Castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 280, 0.2)

#create crosshair
crosshair = Crosshair(0.025)

#create buttons
repair_button = button.Button(SCREEN_WIDTH - 220, 10, repair_img, 0.5)
tower_button = button.Button(SCREEN_WIDTH - 140, 10, tower_img_100, 0.1)
armour_button = button.Button(SCREEN_WIDTH - 75, 10, armour_img, 1.5)

#create groups
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#game loop
run = True
start_intro = True
death_fade = True
while run:

	clock.tick(FPS)
	
	if game_over == False:
		if playing_background_music == False:
			Theme()
			playing_background_music = True
		death_fade = True
		screen.blit(bg, (0, 0))

		#draw castle
		castle.draw()
		castle.shoot()
		#draw towers
		tower_group.draw(screen)
		tower_group.update(enemy_group)

		#draw crosshair
		crosshair.draw()

		#draw bullets
		bullet_group.update()
		bullet_group.draw(screen)

		#draw enemies
		enemy_group.update(screen, castle, bullet_group)

		#Show intro
		if start_intro == True:
			if intro.fade():
				start_intro = False
				intro.fade_counter = 0

		#show details
		show_info()

		#draw buttons
		if repair_button.draw(screen):
			castle.repair()
		if tower_button.draw(screen):
			#check if there is enough money and build a tower
			if castle.money >= TOWER_COST and len(tower_group) < max_towers:
				tower = Tower(
					tower_img_100,
					tower_img_50,
					tower_img_25,
					tower_positions[len(tower_group)][0],
					tower_positions[len(tower_group)][1],
					0.2
					)
				tower_group.add(tower)
				#subtract money
				castle.money -= TOWER_COST
		if armour_button.draw(screen):
			castle.armour()

		num_of_towers = len(tower_group)
		damage = 25

		if num_of_towers <= 2:
			damage = 25
		if num_of_towers > 2 and num_of_towers <= 4:
			damage = 19
		if num_of_towers > 4 and num_of_towers <= 6:
			damage = 17
		if num_of_towers > 6 and num_of_towers <= 10:
			damage = 14	

		#create enemies
		#check if max number of enemies has been reached
		if level_difficulty < target_difficulty:
			if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
				#create enemies
				e = random.randint(0, len(enemy_types) -1)
				enemy = Enemy(enemy_health[e], enemy_animations[e], -100, SCREEN_HEIGHT - 100, Enemy_Speed, damage)
				enemy_group.add(enemy)
				#reset enemy timer
				last_enemy = pygame.time.get_ticks()
				#increase level difficulty by enemy health
				level_difficulty += enemy_health[e]

		#check if all the enemies have been spawned
		if level_difficulty >= target_difficulty:
			#check how many are still alive
			enemies_alive = 0
			for e in enemy_group:
				if e.alive == True:
					enemies_alive += 1
			#if there are none alive the level is complete
			if enemies_alive == 0 and next_level == False:
				next_level = True
				level_reset_time = pygame.time.get_ticks()

		#move onto the next level
		if next_level == True:
			draw_text('LEVEL COMPLETE!', font_60, Sky_Blue, 100, 300)
			#Update high score
			if castle.score > high_score:
				high_score = castle.score
				with open('score.txt', 'w') as file:
					file.write(str(high_score))

			if pygame.time.get_ticks() - level_reset_time > 1500:
				next_level = False
				level += 1
				last_enemy = pygame.time.get_ticks()
				target_difficulty *= DIFFICULTY_MULTIPLIER
				level_difficulty = 0
				enemy_group.empty()
			#Check game Over
		if castle.health <= 0:
			game_over = True
			death_sound_counter = 0 
	else:
		if death_sound_counter == 0:
			pygame.mixer.music.stop()
			playing_background_music = False
			Death.play()
			death_sound_counter = 1
		start_intro = True
		screen.blit(bg, (0, 0))
		if death_fade:
			if death.fade():
				death_fade = False
				death.fade_counter = 0

		draw_text('GAME OVER!', font, BLACK, 300, 100)
		draw_text('PRESS "SPACE" TO PLAY AGAIN!', font, BLACK, 230, 160)
		pygame.mouse.set_visible(True)
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] and death.fade_counter == 0: 
			y = 1
			#SHOW INTRO
			if start_intro == True:
				if intro.fade():
					start_intro = False
					intro.fade_counter = 0
			#RESET VARIABLES
			game_over = False
			level = 1
			target_difficulty = 1000
			level_difficulty = 0
			last_enemy = pygame.time.get_ticks()
			enemy_group.empty()
			tower_group.empty()
			castle.score = 0
			castle.health = 1000
			castle.max_health = 1000
			castle.money = 1000
			pygame.mouse.set_visible(False)

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#update display window
	pygame.display.update()

pygame.quit()