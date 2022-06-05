 #In diesem Spiel wurden keine Rechte von Daten, Bildern und Audios  verletzt.
import pygame
from pygame.locals import *
from pygame import mixer # importiert die Musik
import pickle  # um die Level Daten zu laden 
from os import path 


#  die Lautstäre des Soundes 
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()



clock = pygame.time.Clock()
fps = 60 

# Bildschirm Groesse
screen_width = 680
screen_height = 650


screen = pygame.display.set_mode((screen_width, screen_height))
# Namen des Games 
pygame.display.set_caption('Super Super Mario') 

headline = pygame.font.SysFont("Bauhaus 93", 70)
headline_score = pygame.font.SysFont("Bauhaus 93", 30)

# Spiel haupt Einstellungen 
tile_size = 34
game_over = 0
main_menu = True
level = 1
max_levels = 7
score = 0

# festlegen der Farben
blue = (0,0,255)
reed = (255,0,0)

# lade Bilder 
sun_img = pygame.image.load('img/sun.png')
background_img = pygame.image.load('img/mario.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# lade die Sound Daten 
pygame.mixer.music.load("img/music.wav")
pygame.mixer.music.play(-1, 0.0,5000)
coin_fx = pygame.mixer.Sound("img/coin.wav")
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound("img/jump.wav")
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound("img/game_over.wav")
game_over_fx.set_volume(0.5)


# Fuege den Text im Programme ein 
# mit der  x und y Koordinate
def draw_text(text, font, text_col, x, y):
	img = font.render(text,True,text_col)	
	screen.blit(img, (x,y))
    	

# zuruecksetzten des Levels und laden der Level Daten 
# es werden die Objekte nicht im naechsten Level gezeigt
def reset_level(level):	
	player.reset(100,screen_height -130)	
	blob_group.empty()
	platform_group.empty()	
	lava_group.empty()
	exit_group.empty()
	coin_group.empty()
	if path.exists(f"level{level}_data"):	
		pickle_in = open(f"level{level}_data","rb")	
		world_data = pickle.load(pickle_in)	
		world = World(world_data)	
		return world
    	

# Klasse Button  mit der Positionierung
class Button():	
	def __init__(self, x, y ,image):	
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x =  x + 25
		self.rect.y = y
		self.clicked =  False
#  Fuege die Button im programm ein 
	def draw(self):	
# get mouse position 
		action = False

# die Maus positionierung
		pos = pygame.mouse.get_pos()
# kontrolliere die Maus position
		if self.rect.collidepoint(pos):	
			if 	pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:	
				action = True	
				self.clicked = True 	
		screen.blit(self.image,self.rect)
		
		if pygame.mouse.get_pressed()[0]==0:		
				self.clicked = False
				
		screen.blit(self.image, self.rect)	
				
		return action

    		
   
# Die Klasse Spieler mit der positionierung
class Player():
	def __init__(self, x, y ):	
		self.reset(x, y)
		

	#  die Funktion schaut wann game_over  trifft 
	def update(self,game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5
		col_thresh = 20
		if game_over == 0:
    			
			key = pygame.key.get_pressed()
			#wenn  die Taste gedrückt wurde 
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
              #Taste K_Space ist ein Event zum Springen          
				jump_fx.play()
               #wenn die Figur springt kommt ein sound      
				self.vel_y = -15
				self.jumped = True # Wen die Leertaste gedrueckt wurde
               #Springen wird auf richtig gesetzt 
			if key[pygame.K_SPACE] == False: # Wir auf Falch gesetzt wenn die Leertaste nicht gedrückt wurde
				self.jumped = False 
              # setzt das Springen wieder auf falsch 
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1 
				self.direction = -1
            # wenn die linke taste gedruekt wird  addiere 1 am Counter und -1 an der direction
			if key[pygame.K_RIGHT]:
            # wenn die right  taste gedruekt wird  addiere 1 am Counter und 1 an der direction
				dx += 5 
				self.counter += 1 	
				self.direction = 1
			if key[pygame.K_LEFT] == False and  [pygame.K_RIGHT] == False:
            # wenn die Tasten Links und Rechts nicht dedrueckt sind bleibe auf 0	
				self.counter = 0 
				self.index = 0	

#            Mit der Richtung veraendern sich die Bilder der Figure
			if self.direction == 1:	
				self.image = self.images_right[self.index]
			if self.direction == -1:
				self.image = self.images_left[self.index]
			if self.counter > walk_cooldown:	
				self.counter = 0 	
				self.index += 1	
				if self.index >= len(self.images_right):	
					self.index = 0
				if self.direction == 1:	
					self.image = self.images_right[self.index]
				if self.direction == -1:	
					self.image = self.images_left[self.index]
	   
        #Schwerkraft
			self.vel_y += 1 
			if self.vel_y > 10:
				self.vel_y = 10 
			dy += self.vel_y 
                    # kontrolliere die Kollision 
			self.in_air = True 
			for tile in world.tile_list:
    				# check for Kollision  in der x Richtung 
				if tile[1].colliderect(self.rect.x + dx,self.rect.y ,self.width, self.height):	
					dx = 0 
					# check for Kollision  in der y Richtung 
				if tile[1].colliderect(self.rect.x, self.rect.y + dy ,self.width, self.height):	
					# ueberpruefe ob  ob  Sie springen 
					if self.vel_y < 0:	
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0 
                    # ueberpruefe ob  ob  Sie  fallen 
					elif self.vel_y >= 0:	
						dy = tile[1].top - self.rect.bottom	
						self_vel_y = 0
						self.in_air = False
		
#     Die Kolision  mit der blob_group
			if pygame.sprite.spritecollide(self,blob_group, False):
#     Wenn der Spieler stirbt spiele Sound 
				game_over = -1
				game_over_fx.play()
#     Die Kolision  mit der lava_group
			if pygame.sprite.spritecollide(self,lava_group, False):
				game_over = -1
#     Wenn der Spieler stirbt spiele Sound 
				game_over_fx.play()
#     Die Kolision  mit der exit_group
			if pygame.sprite.spritecollide(self,exit_group, False):	
#     Wenn der Spieler stirbt 
				game_over = 1

#ueberprueffe ob man mit der platform_group kollision 
			for platform in platform_group:	
				# Kollision  in der x Kordinate 
				if platform.rect.colliderect(self.rect.x + dx,self.rect.y ,self.width, self.height):
						dx = 0	
				# Kollision  in der y Kordinate 
				if platform.rect.colliderect(self.rect.x,self.rect.y+dy,self.width, self.height):	
					# Überprüfen Sie die Plattform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:	
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top	
					elif abs((self.rect.bottom + dy)- platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top -1 
						self.in_air = False
						dy = 0
					# Bewegen Sie sich mit der Plattform seitwärts
					if platform.move_x != 0:	
						self.rect.x += platform.move_direction

# Aktualisiere Spieler Koordinaten 			
			self.rect.x += dx
			self.rect.y += dy	
		
	# Wenn der Spieler stirbt
		elif game_over == -1:
    			# setzte game_over auf -1 	
			self.image = self.dead_image
			#  nehme tots_Bild
			draw_text("GAME OVER!",headline,reed,(screen_width // 2)-200, screen_height // 2)
			if self.rect.y > 200:	# der Geist bleibt bei einer hoehe stehen 
				self.rect.y -= 5
			# Zeige Game over an mit der Farbe und mit der Positionierung
	

		screen.blit(self.image, self.rect)
		return game_over

# setzt fuer den Spieler verschide Bilder ein rechts fuer die Rechte Richtung,
#links fuer die Linkte Richtung 
	def reset(self,x,y):	
		self.images_right = []
		self.images_left = []
		self.index = 0 
		self.counter = 0 
#  es werden von 1 bis 5 Bilder eingesetz 
		for num in range(1, 5):
# Parth fuerer  mehr Bilder
			img_right = pygame.image.load(f"img/guy{num}.png")
			img_right = pygame.transform.scale(img_right,(40, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
#       lade beim sterben das Bild vom Geist 
		self.dead_image = pygame.image.load("img/ghost.png") # wenn der Spieler stirbt
#	    Wann welches Bild geladen werden soll
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False  # springen ist auf Falsch gesetzt 
		self.direction = 0
		self.in_air = True 



# Klasse Spielwelt 
class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('img/dirt.png')
		grass_img = pygame.image.load('img/grass.png')

# welches  um welches Objekt sich handelt in der Welt Datei 
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
#  Erde 
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
# Grass
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
#        Alien 
				if tile == 3:		
					blob = Enemy(col_count * tile_size, row_count * tile_size -5)
					blob_group.add(blob)
#        Platform 
				if tile == 4:	
					platform = Platform(col_count * tile_size, row_count * tile_size,1, 0)
					platform_group.add(platform)
#       Platform 	
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
#       Lava 	
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2)) # wie hoch soll die Lava 
					lava_group.add(lava)
#       Coin 
				if tile == 7:	
					coin = Coin(col_count * tile_size + (tile_size //2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
#       Exit 			
				if tile == 8:	
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)

				col_count += 1
			row_count += 1

# zeichne die Objekte 
	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
	


class Enemy(pygame.sprite.Sprite):
	def __init__(self,x,y): # x und y Koordinate
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/blob.png")
		self.rect = self.image.get_rect()
		self.rect.x = x  # x position  
		self.rect.y = y # y position 
		self.move_direction = 1 # richtung der Alien 
		self.move_counter = 0

# bringe Alien in Bewegung  
	def update(self): 
		self.rect.x += self.move_direction # bewege die Richtung
		self.move_counter += 1
		if self.move_counter > 30: 
			self.move_direction *= -1
			self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
	def __init__(self,x,y, move_x, move_y): # x und y Koordinate
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load("img/platform.png")  
		self.image = pygame.transform.scale(img,(tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x  #  Koordinate x
		self.rect.y = y  # Koordinate y
		self.move_counter = 0  # setze den counter auf 0
		self.move_direction = 1  # die richtung 
		self.move_x = move_x  # bewege nach x 
		self.move_y = move_y  # bewge nach y 

#   bringt die Platform in bewegung 
	def update(self):	
		self.rect.x += self.move_direction * self.move_x #  bewegung nach x
		self.rect.y += self.move_direction * self.move_y # bewegung nch y 
		self.move_counter += 1 # die schnelligkeit der Platform
		if self.move_counter > 50:  # bewege dich in den Bereich 
			self.move_direction *= -1  
			self.move_counter *= -1  


class Lava(pygame.sprite.Sprite): 
	def __init__(self,x,y): #  position   mit x und y 
		pygame.sprite.Sprite.__init__(self) 
		img = pygame.image.load("img/lava.png") 
		self.image = pygame.transform.scale(img,(tile_size,tile_size // 2)) # teilt durch 2 
		self.rect = self.image.get_rect() 
		self.rect.x = x   # positionierung x
		self.rect.y = y  # positionierung y


class Coin(pygame.sprite.Sprite):	
	def __init__(self,x,y):	 # position mit  x und y
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load("img/coin.png")
		self.image = pygame.transform.scale(img,(tile_size //2,tile_size // 2)) # teilt durch 2 
		self.rect = self.image.get_rect()
		self.rect.center = (x, y) # mitte von x und y 

class Exit(pygame.sprite.Sprite):	
	def __init__(self,x,y): # position mit  x und y
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load("img/exit.png")
		self.image = pygame.transform.scale(img,(tile_size,int(tile_size * 1.5 )))  # teilt durch 2 
		self.rect = self.image.get_rect()
		self.rect.x = x    # positionierung x
		self.rect.y = y	    # positionierung y


player = Player(100, screen_height - 130)  # groesse des Spielers 

# gruppen der verschiedenen Objekte 
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group =  pygame.sprite.Group()
coin_group =  pygame.sprite.Group()
exit_group =  pygame.sprite.Group()

# load in leval data and create wold 
if path.exists(f"level{level}_data"): #  lade die verschiedenen Level ein 	
	pickle_in = open(f"level{level}_data","rb") # oeffne die Daten	
	world_data = pickle.load(pickle_in) 
	world = World(world_data)  # lade in level die Daten und erstelle die welt 

# erstelle  Buttons 
restart_button = Button(screen_width//2 -50, screen_height//2 +100, restart_img)
start_button = Button(screen_width //2 -350, screen_height //2, start_img)
exit_button = Button(screen_width //2 +150, screen_height //2, exit_img)


run = True
while run:
	clock.tick(fps)
	# positionierung der Objekte
	screen.blit(background_img, (0, 0))
	screen.blit(sun_img, (100, 100))
	if main_menu == True:	
		if exit_button.draw():	 # zeichne die Button
			run = False	
		if start_button.draw(): # zeine die Button
			main_menu = False		
	else:	
		world.draw()
		if game_over == 0:	
			# Aktualiesiere die Gruppen 
			blob_group.update()
			# kontrolliere ob eine muenze eingesammelt wurde 
			platform_group.update()	
			if pygame.sprite.spritecollide(player, coin_group,True):	 #kollision Spieler mit der coin_group
				score += 1  #  addiere den Punkt 
				coin_fx.play()	#  spiele Musik
			draw_text("X"+ str(score),headline_score,blue,tile_size -10, 10) # schreibe den Text

# zeichne die Gruppen
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)	
		coin_group.draw(screen)
		exit_group.draw(screen)
		game_over =player.update(game_over)

	
	if game_over == -1:	 # wenn der Spiel stirbt
		if	restart_button.draw():	 # zeige den Reset Button
			world_data = []
			world = reset_level(level) # setze level zuruek
			game_over = 0  
			score = 0 

# Wenn der Spieler das level geschaft hat
	if game_over == 1: 
#  das Spiel setzt sich zurueck
		level += 1 
		if level <= max_levels:	
# zurueck setzten des Spieles			
			world_data = []	
#	zurueck setzen des  level
			world = reset_level(level) # setzte die Level zuruek
			game_over = 0 # Punkte 0
		else:	# neustarten des Spiels 
			draw_text("YOU WIN!",headline,reed,(screen_width // 2)- 140, screen_height // 2) # posizoniere den Text in die Mitte 
			if restart_button.draw(): # zeige den restart_button
				level = 1  # setze level auf 1 
				world_data = []	# lade world data
				world = reset_level(level) # setzte level zuruek
				game_over = 0	 
				score = 0
    			
# ist eine Taste gedrückt 		
	for event in pygame.event.get():
#   wenn  quit gedrueckt wird 
		if event.type == pygame.QUIT:
#          aendere pygame auf false 
			run = False

# Aktualisiere den Display
	pygame.display.update()


pygame.quit()
