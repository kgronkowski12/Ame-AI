import pygame as pg
import g4f
from g4f.cookies import set_cookies
import random
import ollama

from dataset.letters import dataset_letters
from dataset.system import dataset_system
from dataset.universal import dataset_universal
from dataset.parameter import dataset_parameter
#from ollama import Client

#client = Client(host='http://localhost:11434')
g4f.debug.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking

def render_text(text, color, max_width):
    global font
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Check for newline character
        if '\n' in word:
            parts = word.split('\n')
            for i, part in enumerate(parts):
                if i > 0:
                    lines.append(current_line)
                    current_line = ""
                if current_line:
                    test_line = current_line + " " + part
                else:
                    test_line = part
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = part
        else:
            if current_line:
                test_line = current_line + " " + word
            else:
                test_line = word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_text(text, color, screen, x, y, max_width, max_height):
    global font
    lines = render_text(text, color, max_width)
    y_offset = y
    for line in lines:
        if y_offset>=max_height-30:
            font = pg.font.Font("zpix.ttf", font.get_height()-1)
        if y_offset + font.get_height() > y + max_height:
            break
        txt_surface = font.render(line, True, color)
        screen.blit(txt_surface, (x, y_offset))
        y_offset += font.get_height()



def main():
    global font
    clipper = 0
    doer = "idle"
    romin = ""
    a = pg.image.load("icon.png")

    pg.display.set_icon(a)
    pg.display.set_caption('Ame-chan')
    idle = ["idle0.png","idle1.png","idle2.png","idle3.png"]
    talk_normal = ["talk1.png","talk2.png","talk3.png","talk4.png","talk5.png","talk6.png"]
    messag = []

    b=0
    resp = ""
    affection = 100
    stress = 75
    darkness = 75

    messag = dataset_system(messag,affection)
    messag = dataset_universal(messag)
    messag = dataset_letters(messag,affection)
    messag = dataset_system(messag,affection)
 


   


    screen = pg.display.set_mode((700, 900))
    clock = pg.time.Clock()
    input_box = pg.Rect(2, 460, 699, 200)

    romin = ""
    color_inactive = pg.Color('black')
    color_active = pg.Color('black')
    color = color_inactive
    active = True
    text = ''
    done = False
    prev_quest = ""
    prev_answ = ""
    while not done:
        b+=1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    #active = not active
                    continue
                else:
                    continue
                    #active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        messag.append({"role": "user", "content": text})

                        #response = client.chat(
                        response = ollama.chat(
                            messages=messag,
                            #model='ame-chan',
                            model='ame-chan3',
                            stream=True,
                        )


                        print()
                        resp = ""
                        resp2 = ""
                        for chunk in response:

                            sayer = "normal"
                            resp+=chunk["message"]["content"]
                            resp2+=chunk["message"]["content"]
                            text=resp

                            screen.fill((30, 30, 30))
                            sprite = pg.image.load('./back.png')
                            screen.blit(sprite, (0, 0))
                            chat = pg.image.load('./chat.png')
                            screen.blit(chat, (0, 454))

                            if sayer == "normal":
                                if clipper >= 60:
                                    clipper = 0
                                romin = pg.image.load(talk_normal[int(clipper / 10)])
                                clipper+=1
                            sprite2 = pg.transform.scale(romin, (277, 378))
                            screen.blit(sprite2, (185, 83))

                            draw_text(text, color, screen, input_box.x + 10, input_box.y + 5, 680, 800)
                            print(chunk["message"]["content"],end="")

                            pg.display.flip()
                            clock.tick(30) 

                        messag.append({"role": "assistant", "content": resp2})
                        text = resp
                        print(messag)
                    elif event.key == pg.K_ESCAPE:
                        font = pg.font.Font("zpix.ttf", 28)
                        text = ""
                    elif event.key == pg.K_LCTRL:
                        font = pg.font.Font("zpix.ttf", 15)
                    elif event.key == pg.K_BACKSPACE:
                        if b>10:
                            text = text[:-1]
                            b=0
                    else:
                        text += event.unicode
        keys=pg.key.get_pressed()
        if keys[pg.K_BACKSPACE]:
            if b>4:
                text = text[:-1]
                b = 0

        screen.fill((30, 30, 30))
        sprite = pg.image.load('./back.png')
        chat = pg.image.load('./chat.png')
        screen.blit(chat, (0, 454))
        screen.blit(sprite, (0, 0))
        
        if doer == "idle":
            if clipper >= 40:
                clipper = 0
            romin = pg.image.load(idle[int(clipper / 10)])
        clipper+=0.7
        sprite2 = pg.transform.scale(romin, (277, 378))
        screen.blit(sprite2, (185, 83))
        # Render the current text.
        draw_text(text,color,screen,input_box.x + 10,input_box.y+5,680,800)
        #draw_text(resp, font2, (0,0,0), screen,20,20, 400, 200)
        # Blit the input_box rect.

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    global font
    pg.init()
    font = pg.font.Font("zpix.ttf", 28)
    main()
    pg.quit()
