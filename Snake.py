import libtcodpy as libtcod
import random

#actual size of the window
SCREEN_WIDTH = 20
SCREEN_HEIGHT = 20
 
LIMIT_FPS = 12  #20 frames-per-second maximum

 
def handle_keys():
    global dirx, diry
 
    key = libtcod.console_check_for_keypress()  #real-time
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
 
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP) and diry == 0:
        dirx = 0
        diry = -1
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) and diry == 0:
        dirx = 0
        diry = 1
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) and dirx == 0:
        dirx = -1
        diry = 0
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) and dirx == 0:
        dirx = 1
        diry = 0
 
 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)



break_int = 0
dirx = 1
diry = 0
snakex = SCREEN_WIDTH/2
snakey = SCREEN_HEIGHT/2
applex = random.randint(2,SCREEN_WIDTH - 2)
appley = random.randint(2,SCREEN_HEIGHT - 2)
snakex_loop = [snakex, snakex, snakex, snakex, snakex]
snakey_loop = [snakey, snakey, snakey, snakey, snakey]

libtcod.console_put_char(0, applex, appley, 'O', libtcod.BKGND_NONE)


while not libtcod.console_is_window_closed():
 
    libtcod.console_set_default_foreground(0, libtcod.white)
    snakex_tail = snakex_loop[len(snakex_loop) - 1]
    snakey_tail = snakey_loop[len(snakey_loop) - 1]
    libtcod.console_put_char(0, snakex_tail, snakey_tail, ' ', libtcod.BKGND_NONE)

    snakex = snakex + dirx
    snakey = snakey + diry

    snake_loop_int = len(snakex_loop) - 1
    while snake_loop_int > 0:
        snakex_loop[snake_loop_int] = snakex_loop[snake_loop_int - 1]
        snakey_loop[snake_loop_int] = snakey_loop[snake_loop_int - 1]
        snake_loop_int = snake_loop_int - 1

    snakex_loop[0] = snakex
    snakey_loop[0] = snakey

    

    if snakex < 0 or snakex >= SCREEN_WIDTH or snakey < 0 or snakey >= SCREEN_HEIGHT :
        break_int = 1

    snake_loop_int = len(snakex_loop) - 1
    while snake_loop_int > 0:
        if snakex == snakex_loop[snake_loop_int] and snakey == snakey_loop[snake_loop_int]:
            break_int = 1
        snake_loop_int = snake_loop_int - 1

    #Extend Snake Length When It Eats Apple
    if snakex == applex and snakey == appley:
        apple_loop_int = 1
        while apple_loop_int == 1:
            applex = random.randint(2,SCREEN_WIDTH - 2)
            appley = random.randint(2,SCREEN_HEIGHT - 2)
            snake_loop_int = len(snakex_loop) - 1
            while snake_loop_int > 0:
                if applex == snakex_loop[snake_loop_int] and appley == snakey_loop[snake_loop_int]:
                    apple_loop_int = 1
                    snake_loop_int = 0
                else:
                    apple_loop_int = 0
                snake_loop_int = snake_loop_int - 1
        snakex_loop.append(snakex_loop[len(snakex_loop) - 1])
        snakey_loop.append(snakey_loop[len(snakey_loop) - 1])
        libtcod.console_put_char(0, applex, appley, 'O', libtcod.BKGND_NONE)
        

    print snakex_loop[:]
    print snakey_loop[:]

    if break_int == 1:
        break
        
 
    libtcod.console_put_char(0, snakex, snakey, 'x', libtcod.BKGND_NONE)
    libtcod.console_flush()
 
    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
