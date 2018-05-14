import libtcodpy as libtcod
 
#actual size of the window
SCREEN_WIDTH = 60
SCREEN_HEIGHT = 60
 
LIMIT_FPS = 10  

print' '
print'THE GAME OF LIFE'
print'by John Horton Conway, recoded by Samuel Moyer'
print' '
print' '
print'Controls'
print' '
print'8     : Move Up'
print'2     : Move Down'
print'4     : Move Left'
print'6     : Move Right'
print'5     : Place/Delete Individual'
print'Enter : Start/pause Growth'
print'+     : Toggle Speed'
print' '
print' '
print'Rules'
print' '
print'1. Any individual with fewer than two neighbors dies due to under population.'
print'2. Any individual with two or three neighbors lives on to the next generation.'
print'3. Any individual with more than three neighbors dies due to overpopulation.'
print'4. Any empty cell with exactly three neighbors gives birth to an individual.'
print' '


 
def handle_keys():
    global playerx, playery
 
    key = libtcod.console_check_for_keypress()
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
 
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_KP8):
        playery -= 1
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_KP2):
        playery += 1
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_KP4):
        playerx -= 1
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_KP6):
        playerx += 1



def next_generation(time):
    global general_map

    #Define General Map
    if time == 0:
        map_loop_int_y = 0
        general_map = []
        while map_loop_int_y < SCREEN_HEIGHT:
            map_loop_int_x = 0
            mapy = []
            while map_loop_int_x < SCREEN_WIDTH:
                mapy.append(0)
                map_loop_int_x = map_loop_int_x + 1
            general_map.append(mapy)
            map_loop_int_y = map_loop_int_y + 1

    if time == 0 or time == 2:
        #Clear Copy Map
        map_loop_int_y = 0
        copy_map = []
        while map_loop_int_y < SCREEN_HEIGHT:
            map_loop_int_x = 0
            mapy = []
            while map_loop_int_x < SCREEN_WIDTH:
                mapy.append(0)
                map_loop_int_x = map_loop_int_x + 1
            copy_map.append(mapy)
            map_loop_int_y = map_loop_int_y + 1

        #Fill Copy Map and Create/Delete Population
        map_loop_int_y = 1
        while map_loop_int_y < SCREEN_HEIGHT - 1:
            map_loop_int_x = 1
            while map_loop_int_x < SCREEN_WIDTH - 1:
                neighbours = general_map[map_loop_int_y - 1][map_loop_int_x + 1] + general_map[map_loop_int_y][map_loop_int_x + 1] + general_map[map_loop_int_y + 1][map_loop_int_x + 1] + general_map[map_loop_int_y - 1][map_loop_int_x - 1] + general_map[map_loop_int_y][map_loop_int_x - 1] + general_map[map_loop_int_y + 1][map_loop_int_x - 1] + general_map[map_loop_int_y - 1][map_loop_int_x] + general_map[map_loop_int_y + 1][map_loop_int_x]
                if general_map[map_loop_int_y][map_loop_int_x] == 0 and neighbours == 3:
                    copy_map[map_loop_int_y][map_loop_int_x] = 1
                if general_map[map_loop_int_y][map_loop_int_x] == 1 and neighbours < 2:
                    copy_map[map_loop_int_y][map_loop_int_x] = 0
                if general_map[map_loop_int_y][map_loop_int_x] == 1 and neighbours > 3:
                    copy_map[map_loop_int_y][map_loop_int_x] = 0
                if general_map[map_loop_int_y][map_loop_int_x] == 1 and (neighbours == 3 or neighbours == 2):
                    copy_map[map_loop_int_y][map_loop_int_x] = 1
                map_loop_int_x = map_loop_int_x + 1
            map_loop_int_y = map_loop_int_y + 1

        #Translate Copy Map to General Map
        map_loop_int_y = 0
        while map_loop_int_y < SCREEN_HEIGHT:
            map_loop_int_x = 0
            while map_loop_int_x < SCREEN_WIDTH:
                general_map[map_loop_int_y][map_loop_int_x] = copy_map[map_loop_int_y][map_loop_int_x]
                map_loop_int_x = map_loop_int_x + 1
            map_loop_int_y = map_loop_int_y + 1


    #Print General Map
    map_loop_int_x = 0
    while map_loop_int_x < SCREEN_WIDTH:
        map_loop_int_y = 0
        while map_loop_int_y < SCREEN_HEIGHT:
            if general_map [map_loop_int_y][map_loop_int_x] == 0:
                libtcod.console_put_char(0, map_loop_int_x, map_loop_int_y, ' ', libtcod.BKGND_NONE)
            elif general_map [map_loop_int_y][map_loop_int_x] == 1:
                libtcod.console_put_char(0, map_loop_int_x, map_loop_int_y, 176, libtcod.BKGND_NONE)
            map_loop_int_y = map_loop_int_y + 1
        map_loop_int_x = map_loop_int_x + 1 
 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
 
playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2
time = 0
general_map = []
 
while not libtcod.console_is_window_closed():

    #Display Character/Population
    libtcod.console_set_default_foreground(0, libtcod.white)
    if time == 0:
        next_generation(time)
        time = 1
    if general_map[playery][playerx] == 1:
        libtcod.console_put_char(0, playerx, playery, 178, libtcod.BKGND_NONE)
    else:
        libtcod.console_put_char(0, playerx, playery, 177, libtcod.BKGND_NONE)
    libtcod.console_flush()

    
    libtcod.console_put_char(0, playerx, playery, ' ', libtcod.BKGND_NONE)

    next_generation(time)

    libtcod.sys_set_fps(LIMIT_FPS)

    #Create/Delete Population
    key = libtcod.console_check_for_keypress()
    if key.vk == libtcod.KEY_KP5:
        if general_map[playery][playerx] == 0:
            general_map[playery][playerx] = 1
        else:
            general_map[playery][playerx] = 0
    #Start/Stop Loop
    elif key.vk == libtcod.KEY_KPENTER:
        if time == 1:
            time = 2
        else:
            time = 1
    #Speed Control
    elif key.vk == libtcod.KEY_KPADD:
        if LIMIT_FPS == 10:
            LIMIT_FPS = 30
        elif LIMIT_FPS == 60:
            LIMIT_FPS = 10
        else:
            LIMIT_FPS = 60
    #Clear Map
    elif key.vk == libtcod.KEY_KP0:
        time = 0

    if time == 1:
        libtcod.console_put_char(0, 1, 1, 186, libtcod.BKGND_NONE)

    elif time == 2:
        libtcod.console_put_char(0, 1, 1, 16, libtcod.BKGND_NONE)

    if LIMIT_FPS == 10:
        libtcod.console_print(0, 3, 1, 'Slow')

    if LIMIT_FPS == 30:
        libtcod.console_print(0, 3, 1, 'Fast')

    if LIMIT_FPS == 60:
        libtcod.console_print(0, 3, 1, 'Fastest')
 
    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
