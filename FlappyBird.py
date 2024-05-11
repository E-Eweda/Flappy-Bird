import random
import pgzrun
import time
HEIGHT=708
WIDTH=400
TITLE="Flappy Bird"

bird=Actor("bird1.png",(60,200))
bird.dead=False
bird.score=-1
bird.vy=0
started=False
top=Actor("top.png",anchor=("left","bottom"),pos=(-100,0))
bottom=Actor("bottom.png",anchor=("left","top"),pos=(-100,0))
game_over=False
game_over_time=0
level=0
sounds.music.play(-1)
sounds.music.set_volume(0.2)        
level_backgrounds = ["background0.png", "background1.png", "background2.png"]
def draw_start_screen():
    screen.blit(level_backgrounds[0], (0, 0))
    screen.draw.text("Flappy Bird", color="white", midtop=(WIDTH//2, HEIGHT//2 - 100), fontsize=70, shadow=(1, 1))
    screen.draw.text("Press Space To Start", color="white", midtop=(WIDTH//2, HEIGHT//2), fontsize=40, shadow=(1, 1))
def draw():
    if not started:
        draw_start_screen()
        return
    screen.clear()
    if level == 0:
        screen.blit(level_backgrounds[0], (0, 0))
    elif level == 1:
        screen.blit(level_backgrounds[1], (0, 0))
    elif level == 2:
        screen.blit(level_backgrounds[2], (0, 0))   
    elif level > 2:  # If the player finishes level 2
        screen.blit(level_backgrounds[2], (0, 0))  
        screen.draw.text("You Won!", color="white", midtop=(WIDTH//2, 320), fontsize=70, shadow=(1, 1))
        screen.draw.text("Press Space To Play Again", color="white", midtop=(WIDTH//2, 370), fontsize=40, shadow=(1, 1))
        return    
    top.draw()
    bottom.draw()
    bird.draw()
    screen.draw.text(str(bird.score),color="white",midtop=(WIDTH//2,10),fontsize=70,shadow=(1,1))
    screen.draw.text("Level: " + str(level+1), color="white", midtop=(WIDTH//2, 60), fontsize=40, shadow=(1, 1))
    if  bird.dead and time.time() - game_over_time>2 or bird.y > HEIGHT :  # Only show the Game Over message if the bird has not collided
        screen.blit(level_backgrounds[level], (0, 0))
        screen.draw.text("Level: " + str(level+1), color="white", midtop=(WIDTH//2, 80), fontsize=70, shadow=(1, 1))        
        screen.draw.text("Score: "+str(bird.score),color="white",midtop=(WIDTH//2,140),fontsize=70,shadow=(1,1))
        screen.draw.text("Game Over",color="white",midtop=(WIDTH//2,280),fontsize=70,shadow=(1,1))
        screen.draw.text("Press Space To Try Again",color="white",midtop=(WIDTH//2,380),fontsize=40,shadow=(1,1))

def update_pipes():
    top.left=top.left-3
    bottom.left=bottom.left-3
    if top.right<0:
        bird.score=bird.score+1
        gap=random.randint(200,HEIGHT-200)
        top.pos = (WIDTH,gap-160//2)
        bottom.pos = (WIDTH,gap+160//2)
        
def update(dt):
    global game_over, game_over_time, level,started
    if not started:
        if keyboard.space:
            started = True
        return
    if not game_over:
        update_pipes()
        level = int(bird.score/5)
        top.left = top.left- level * 1
        bottom.left = bottom.left - level * 1
        uy=bird.vy
        bird.vy=bird.vy+2000.0*dt
        bird.y=bird.y+(uy+bird.vy)*0.5*dt
        bird.x=75
        if bird.y > HEIGHT:
         game_over = True
         game_over_time = time.time()
        if not bird.dead:
            if bird.vy<-3:
                bird.image="bird2.png"
            else:
                bird.image="bird1.png"

        if bird.colliderect(top) or bird.colliderect(bottom):
            
            bird.dead=True
            bird.image="birddead.png"
            game_over=True
            game_over_time=time.time()
        
    else:
        if time.time() - game_over_time > 2 :
         if keyboard.space:
            game_over = False 
            bird.y = 200
            bird.dead = False
            bird.score = 0
            bird.vy = 0
            level = 1  # Reset the level to 0
            gap = random.randint(200, HEIGHT - 200)
            top.pos = (WIDTH, gap - 160 // 2)
            bottom.pos = (WIDTH, gap + 160 // 2)
def on_key_down(key):
    global game_over
    
    if key==keys.SPACE and not bird.dead and not game_over:
        bird.vy=-500

pgzrun.go()      