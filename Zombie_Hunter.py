import libtcodpy as libtcod
import random
import math

print 'Zombie Hunter'
print ''
print 'Move with arrow keys,'
print 'Shoot with spacebar.'
print ''
print 'Good luck.'
print ''
 
#actual size of the window
SCREEN_WIDTH = 40
SCREEN_HEIGHT = 39
 
LIMIT_FPS = 20  #20 frames-per-second maximum
 
 
def handle_keys():
    global playerx, playery, SCREEN_WIDTH, SCREEN_HEIGHT, directionx, directiony
 
    key = libtcod.console_check_for_keypress()  #real-time
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
 
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        playery -= 1
        directionx = 0
        directiony = -1
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        playery += 1
        directionx = 0
        directiony = 1
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        playerx -= 1
        directionx = -1
        directiony = 0
        
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        playerx += 1
        directionx = 1
        directiony = 0

    if playerx > SCREEN_WIDTH - 1:
        playerx = SCREEN_WIDTH -1

    if playerx < 0:
        playerx = 0

    if playery > SCREEN_HEIGHT -1:
        playery = SCREEN_HEIGHT -1

    if playery < 0:
        playery = 0
    
 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT + 1, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
 
playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2

bulletx = playerx
bullety = playery

bulletdirectionx = 0
bulletdirectiony = 0

directionx = 0
directiony = -1
zombiex = [1]
zombiey = [1]
zombie_movement_loop = 0
zombie_generation_loop = 0
zombie_generation_speed = 100
#the lower generation number is, the faster zombies will spawn
zombie_speed = 0.3
#the higher the zombie speed is, the faster zombies will move
multiplier = 1.1
health = -100
start = 1

while not libtcod.console_is_window_closed():

    libtcod.console_set_default_foreground(0, libtcod.white)

    #Starting the Game
    while start == 0:
        key = libtcod.console_check_for_keypress()
        if key.vk == libtcod.KEY_SPACE:
            start = 1
            health = 10
            libtcod.console_print(0, SCREEN_WIDTH/2 -10, SCREEN_HEIGHT/2, '                    ')

    #Game Over Screen
    if health > 0:
        handle_keys()
    elif health <= 0:
        libtcod.console_print(0, SCREEN_WIDTH/2 -4, SCREEN_HEIGHT/2, 'GAME OVER')

    #Player Display
    if directiony == -1:
        libtcod.console_put_char(0, playerx, playery, 30, libtcod.BKGND_NONE)
    elif directionx == 1:
        libtcod.console_put_char(0, playerx, playery, 16, libtcod.BKGND_NONE)
    elif directiony == 1:
        libtcod.console_put_char(0, playerx, playery, 31, libtcod.BKGND_NONE)
    elif directionx == -1:
        libtcod.console_put_char(0, playerx, playery, 17, libtcod.BKGND_NONE)

    #Start Screen
    if health == -100:
        libtcod.console_print(0, SCREEN_WIDTH/2 -10, SCREEN_HEIGHT/2, 'Press SPACE to begin')
        start = 0
    
    libtcod.console_flush()

    #Player Display
    libtcod.console_put_char(0, playerx, playery, ' ', libtcod.BKGND_NONE)

    #Zombie Movement
    while zombie_movement_loop < len(zombiex):

        libtcod.console_put_char(0, int(zombiex[zombie_movement_loop]), int(zombiey[zombie_movement_loop]), ' ', libtcod.BKGND_NONE)

        #Follow Player's X Coordinates
        if zombiex[zombie_movement_loop] > playerx:
            zombiex[zombie_movement_loop] -= zombie_speed * (abs(zombiex[zombie_movement_loop] - playerx) / math.sqrt(math.pow(abs(zombiex[zombie_movement_loop] - playerx), 2) + math.pow(abs(zombiey[zombie_movement_loop] - playery), 2)))
        elif zombiex[zombie_movement_loop] < playerx:
            zombiex[zombie_movement_loop] += zombie_speed * (abs(zombiex[zombie_movement_loop] - playerx) / math.sqrt(math.pow(abs(zombiex[zombie_movement_loop] - playerx), 2) + math.pow(abs(zombiey[zombie_movement_loop] - playery), 2)))
        elif zombiex[zombie_movement_loop] == playerx:
            zombiex[zombie_movement_loop] -= 0
            
        #Follow Player's Y Coordinates
        if zombiey[zombie_movement_loop] > playery:
            zombiey[zombie_movement_loop] -= zombie_speed  * (abs(zombiey[zombie_movement_loop] - playery) / math.sqrt(math.pow(abs(zombiex[zombie_movement_loop] - playerx), 2) + math.pow(abs(zombiey[zombie_movement_loop] - playery), 2)))
        elif zombiey[zombie_movement_loop] < playery:
            zombiey[zombie_movement_loop] += zombie_speed * (abs(zombiey[zombie_movement_loop] - playery) / math.sqrt(math.pow(abs(zombiex[zombie_movement_loop] - playerx), 2) + math.pow(abs(zombiey[zombie_movement_loop] - playery), 2)))
        elif zombiey[zombie_movement_loop] == playery:
            zombiey[zombie_movement_loop] -= 0

        #Trap Dead Zombies in the Void
        if zombiey[zombie_movement_loop] < 0 and zombiex[zombie_movement_loop] < 0:
            zombiey[zombie_movement_loop] = -5
            zombiex[zombie_movement_loop] = -5

        #Kill Zombies Hit by Bullets by Placing Them in the Void
        if int(zombiex[zombie_movement_loop]) == bulletx and int(zombiey[zombie_movement_loop]) == bullety:
            #zombiex.replace(zombie_movement_loop, '')
            #zombiey.replace(zombie_movement_loop, '')
            zombiex[zombie_movement_loop] = -5
            zombiey[zombie_movement_loop] = -5
            zombie_generation_speed = zombie_generation_speed/multiplier
            libtcod.console_put_char(0, bulletx, bullety, 177, libtcod.BKGND_NONE)
            bulletx = -1
            bullety = -1

        #Remove Health of Player that Comes in Contact with Zombie    
        if int(zombiex[zombie_movement_loop]) == playerx and int(zombiey[zombie_movement_loop]) == playery:
            health = health - 1

        #Display Zombie
        libtcod.console_put_char(0, int(zombiex[zombie_movement_loop]), int(zombiey[zombie_movement_loop]), 'Z', libtcod.BKGND_NONE)
            
        zombie_movement_loop += 1

    zombie_movement_loop = 0

    #Generate New Zombies
    if zombie_generation_loop < zombie_generation_speed:
        zombie_generation_loop += 1
    else:
        zombie_generation_loop = 0
        zombiex.append(random.randint(0, SCREEN_WIDTH))
        zombiey.append(random.randint(0, SCREEN_HEIGHT))

    #Bullet Generation
    key = libtcod.console_check_for_keypress()
    if key.vk == libtcod.KEY_SPACE:
        libtcod.console_put_char(0, bulletx, bullety, ' ', libtcod.BKGND_NONE)
        bulletx = playerx + directionx
        bullety = playery + directiony
        bulletdirectionx = directionx
        bulletdirectiony = directiony

    if bulletx != playerx or bullety != playery:
        libtcod.console_put_char(0, bulletx, bullety, ' ', libtcod.BKGND_NONE)
        bulletx = bulletx + bulletdirectionx
        bullety = bullety + bulletdirectiony
        libtcod.console_put_char(0, bulletx, bullety, 'x', libtcod.BKGND_NONE)

    libtcod.console_print(0, 1, SCREEN_HEIGHT, 'HEALTH')

    #Display Healthbar
    healthloop = 18
    while healthloop > 8:
        libtcod.console_put_char(0, healthloop, SCREEN_HEIGHT, 176, libtcod.BKGND_NONE)
        healthloop = healthloop - 1

    #Display Health
    healthloop = health + 8 
    while healthloop > 8:
        libtcod.console_put_char(0, healthloop, SCREEN_HEIGHT, 178, libtcod.BKGND_NONE)
        healthloop = healthloop - 1


    #handle keys and exit game if needed
    #exit = handle_keys()
    #if exit:
        #break



#GLITCHES/BUGS TO FIX
#
#Zombies 'shuffle', don't remove player's health
#Bullets don't always kill zombies
#Blood stains should be red
#No way of escaping the game by pressing escape after death
#No way of quickly restarting the game
