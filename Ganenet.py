import pygame as pg
import os
from pygame.locals import *
import time
import random


BULLET_SPEED = 15
MADPESOT_SPEED = 7

display = pg.display.set_mode((1024,1024)) # window size is determined here
pg.init()
size = width, height = 1200,  900
screen = pg.display.set_mode(size)

pg.mixer.init()
music = pg.mixer.Sound("music.wav")
pg.mixer.Sound.play(music)



madpeset = pg.image.load("PIcs/madpeset.png")
character = pg.image.load("PIcs/ganenet_boss.jpg")
witch = pg.image.load("PIcs/kid2.jpg")
liel = pg.image.load("PIcs/kid1.jpg")
table = pg.image.load("PIcs/table.jpg")


madpeset = pg.transform.scale(madpeset, (70, 70))
table = pg.transform.scale(table, (80, 80))
witch = pg.transform.scale(witch, (60, 60))
liel = pg.transform.scale(liel, (60, 60))



screen.fill((255, 255, 255))

characterx = 900
charactery = 60

new_bullet = False


lielx = 0
liely = 0
witchx = 0
witchy = 0

class bangarang1:
    img = madpeset
    location = [lielx, liely]


class bangarang1:
    img = madpeset
    location = [witchx, witchy]


class bullet:
    color = (0,0,0)
    size = 4
    location = (characterx - 10, charactery)


class Score:
    def __init__(self):
        self.score = 0
        self.font = pg.font.SysFont('monospace', 30)

    def draw(self, screen):
        txt = self.font.render('SCORE: ' + str(self.score), True, pg.color.Color("black"))
        screen.blit(txt, (100, 0))

    def add(self):
        self.score += 1

    def val(self):
        return self.score

    def reset(self):
        self.score = 0

    def draw_gameover(self, screen):
        txt = self.font.render(
            'GAMEOVER! You scored ' + str(self.score) + ' points.  Good on ya! ', True, pg.color.Color("black"))
        screen.blit(txt, (400 - txt.get_width() / 2, 100))
    def draw_title(self, screen):
        self.font = pg.font.SysFont('monospace', 70)
        txt = self.font.render("GANENET FEVER TM", True, pg.color.Color("black"))
        screen.blit(txt, (400 - txt.get_width() / 2, 200))
        self.font = pg.font.SysFont('monospace', 30)



score = Score()

for i in range(150):
    pg.display.update()
    pg.display.flip()

    clock = pg.time.Clock()
    clock.tick(60)
    screen.fill((255, 255, 255))
    score.draw_title(screen)
    display.blit(character, (characterx, charactery + 50))

#pg.key.set_repeat(10,10)

bullets = []
numBullets = 0
b1 = bullet()

seed = 9090
fired = 0

lHit = True #liel being hit
wHit = True #witch being hit


madpasots = []

mad_timer1= 0
mad_timer2 = 0
new_madpeset1 = False
new_madpeset2 = False


while True:
    pg.display.update()
    pg.display.flip()

    clock = pg.time.Clock()
    clock.tick(60)
    screen.fill((255, 255, 255))


    for i in madpasots:
        print(str(i) + "  --  Charachter:" + str([characterx, charactery]))

        if (i[0] in range(characterx - 50, characterx + 100)) and (i[1] in range(charactery-20, charactery+71)):
            score.draw_gameover(screen)
            display.blit(character, (characterx, charactery-75))
            pg.display.update()
            os.system("echo " + str(score.val()) + " >> scores.txt")
            time.sleep(3)
            print("game over!")
            exit()

    if mad_timer1 == 100:
        new_madpeset1 = True

        madpasots.append([lielx, liely, 1])
        mad_timer1 = 0
    if mad_timer2 == 100:
        new_madpeset2 = True
        madpasots.append([witchx, witchy, 1])
        mad_timer2 = 0

    display.blit(character, (characterx, charactery))
    score.draw(screen)

    for i in madpasots:

        display.blit(madpeset, (i[0], i[1]))
        i[0] += MADPESOT_SPEED * i[2]
        i[2] += 0.000
        if(i[0] > 1100):
            madpasots.remove(i)


    mad_timer1 +=1
    mad_timer2+=1

    rowBuff = 75
    colBuff = 150
    x = 50
    y = 50


    if wHit:
        witchRow = random.randint(0, 7)
        witchCol = random.randint(1, 5)
        witchx = rowBuff * witchRow
        witchy = witchCol * (colBuff) - 20
        print("Witch loc: " + str((witchx, witchy)))

        wHit = False

    random.seed(seed)
    seed+=900

    if lHit:
        lielRow = random.randint(0, 7)
        lielCol = random.randint(1, 5)
        lielx = lielRow*rowBuff
        liely = lielCol*(colBuff) - 20

        lHit = False

    display.blit(witch, (witchx, witchy))
    display.blit(liel, (lielx, liely))

    for i in range(8):
        for j in range(6):
            display.blit(table, (x + rowBuff * i, y + colBuff * j))


    if (numBullets > 0):
        if fired == 1:
            fired = 1

        if new_bullet and fired == 1:
            bullets.append([characterx, charactery + 98])
            new_bullet = False


        for i in bullets:
            print(str(i))
            if i[0] in range(witchx-6, witchx + 6) and i[1] in range(witchy - 60, witchy + 60):
                wHit = True
                score.add()
                print("witch Hit Hit!  Bullet location:" + str(i))
                bullets.remove(i)
                numBullets -= 1

                print("Bullet location: " + str(i) + "witch location: " + str((witchx, witchy)))


            elif i[0] in range(lielx - 6, lielx + 6) and i[1] in range(liely - 60, liely + 60):
                lHit = True
                print("Liel Hit Hit!  Bullet location:" + str(i))
                bullets.remove(i)
                numBullets -= 1
                score.add()

        for i in bullets:
            if i[0] == 0:
                bullets.remove(i)


        for i in bullets:
            #print("Location is: " + str(i[0]))
            i[0] -= BULLET_SPEED
            pg.draw.circle(screen, b1.color, (i[0], i[1]), bullet.size)



    for event in pg.event.get():
        if event.type == KEYDOWN:
            #if event.key == K_LEFT:
             #   characterx -= 5
            #if event.key == K_RIGHT:
             #   characterx += 5
            if event.key == K_UP and charactery > 125:
                charactery -= 150
            if event.key == K_DOWN and charactery < 570:
                charactery += 150
            if event.key == K_SPACE:
                new_bullet = True
                numBullets += 1

                fired = 1 #fired +=1

                #print("boom")
        if event.type == QUIT:
            pg.quit()
            exit()

        pg.display.update()
        pg.display.flip()
