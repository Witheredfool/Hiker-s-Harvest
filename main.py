import pygame, asyncio
import sys
from pygame.locals import *
import random


#music implemenation
pygame.mixer.init()
pygame.mixer.music.load(r"Assets\bit-beats-1-168243.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)




player_collected_items = []

Total_Collectibles = 45

#Massive Collectables library (45)
COLLECTIBLES = {
    "Temperate Forest":{
        "Nadia":[{"name":"Lily of the Valley","image":r"Assets\TF_folder\LOTF.png"},
                  {"name":"Blueberry","image":r"Assets\TF_folder\BlueBerry.png"},
                  {"name":"Viburnum","image":r"Assets\TF_folder\Viburnum.png"},
                  {"name":"Trillium","image":r"Assets\TF_folder\Trillium.png"},
                  {"name":"Mahonia","image":r"Assets\TF_folder\Mahonia.png"}],
        "Mika":[{"name":"Box Turtle","image":r"Assets\TF_folder\BoxTurtle.png"},
                {"name":"Polyphemus Moth","image":r"Assets\TF_folder\PolyMoth.png"},
                {"name":"Pill Bug","image":r"Assets\TF_folder\PillBug.png"},
                {"name": "Stag Beetle","image":r"Assets\TF_folder\StagBeetle.png"},
                {"name": "Blue Jay", "image":r"Assets\TF_folder\BlueJay.png"}],
        "Wolfie":[{"name":"Heals All","image":r"Assets\TF_folder\HealsAll.png"},
                  {"name":"Yarrow","image":r"Assets\TF_folder\Yarrow.png"},
                  {"name":"Ginseng","image":r"Assets\TF_folder\Ginseng.png"},
                  {"name":"Blood Root","image":r"Assets\TF_folder\BloodRoot.png"},
                  {"name": "Black Cohosh", "image": r"Assets\TF_folder\BlackCohosh.png"}]},
    "Tide Pool":{
        "Nadia":[{"name":"Sea Holly","image":r"Assets\TP_folder\SeaHolly.png"},
                 {"name":"Sea Mayweed","image":r"Assets\TP_folder\Mayweed.png"},
                 {"name":"Eel Grass","image":r"Assets\TP_folder\Eelgrass.png"},
                 {"name":"Leymus","image":r"Assets\TP_folder\DuneGrass.png"},
                 {"name":"Salal","image":r"Assets\TP_folder\Salal.png"}],
        "Mika":[{"name":"Hermit Crab","image":r"Assets\TP_folder\HermitCrab.png"},
                {"name":"Dead Coral","image":r"Assets\TP_folder\DeadCoral.png"},
                {"name":"Purple Sea Urchin","image":r"Assets\TP_folder\SeaUrchin.png"},
                {"name": "Bat Star","image":r"Assets\TP_folder\BatStar.png"},
                {"name": "NudiBranch","image":r"Assets\TP_folder\Nudibranch.png"}],
        "Wolfie":[{"name":"Sea Berry","image":r"Assets\TP_folder\Seaberry.png"},
                  {"name":"Rosemary","image":r"Assets\TP_folder\Rosemary.png"},
                  {"name":"Sage","image":r"Assets\TP_folder\Sage.png"},
                  {"name": "Sea Thrift", "image": r"Assets\TP_folder\SeaThrift.png"},
                  {"name":"Bladderwrack","image":r"Assets\TP_folder\Bladderwrack.png"}]},
    "Grass Land":{
        "Nadia":[{"name":"Wild Indigo","image":r"Assets\GL_folder\Indigo.png"},
                 {"name":"Parish's Nightshade","image":r"Assets\GL_folder\Nightshade.png"},
                 {"name":"Gumplant","image":r"Assets\GL_folder\Gumplant.png"},
                 {"name":"Violet","image":r"Assets\GL_folder\Violet.png"},
                 {"name":"Crocus","image":r"Assets\GL_folder\Crocus.png"}],
        "Mika":[{"name":"Deer Skull","image":r"Assets\GL_folder\DeerSkull.png"},
                {"name":"Burrowing Owls","image":r"Assets\GL_folder\owl.png"},
                {"name":"Rattlesnake","image":r"Assets\GL_folder\RattleSnake.png"},
                {"name": "Milkweed Bug","image":r"Assets\GL_folder\MilkweedBug.png"},
                {"name": "Cottontail Rabbit","image":r"Assets\GL_folder\Rabbit.png"}],
        "Wolfie":[{"name":"Red Clover","image":r"Assets\GL_folder\RedClover.png"},
                  {"name":"Mugwort","image":r"Assets\GL_folder\Mugwort.png"},
                  {"name":"Wild Thyme","image":r"Assets\GL_folder\Thyme.png"},
                  {"name": "Heather", "image": r"Assets\GL_folder\Heather.png"},
                  {"name":"Catnip","image":r"Assets\GL_folder\Catnip.png"}]}}
    


pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 768, 512
scene = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hiker's Harvest")

WHITE = (255,255,255)
LIGHT_GREY = (170,170,170)
DARK_GREY = (100,100,100)

title_font = pygame.font.SysFont("Nunito", 60)
button_font = pygame.font.SysFont("Nunito", 30)

background = pygame.image.load(r"Assets\title_screen.png").convert()

char_images = {
    "Nadia": r"Assets\mysprite_nadia.png",
    "Mika": r"Assets\MySprite_Mika.png",
    "Wolfie": r"Assets\MySprite_Wolfie.png"
}

map_images = {
    "Tide Pool": r"Assets\TP_folder\TP_map.png",
    "Grass Land": r"Assets\GL_folder\GL_map.png",
    "Temperate Forest": r"Assets\TF_folder\TF_map.png"
}

char_icons = {}
for name, path in char_images.items():
    icon = pygame.image.load(path).convert_alpha()
    char_icons[name] = pygame.transform.scale(icon, (80,80))

map_icons = {}
for name, path in map_images.items():
    icon = pygame.image.load(path).convert_alpha()
    map_icons[name] = pygame.transform.scale(icon, (80,80))


full_maps = {
    name: pygame.image.load(path).convert()
    for name, path in map_images.items()
}

def draw_text(text, font, color, surface, x, y):
    t = font.render(text, True, color)
    surface.blit(t, t.get_rect(center=(x,y)))



#Title Screen
def title_screen():
    buttons = {
        "Start!": pygame.Rect(WIDTH//2 - 80, HEIGHT//2 - 50, 160, 80),
        "Exit": pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 50, 160, 80),
    }

    while True:
        scene.blit(background, (0,0))
        draw_text("Hiker's Harvest", title_font, WHITE, scene, WIDTH//2, HEIGHT//4-50)
        draw_text("By: Daisy Holt", button_font, WHITE, scene, WIDTH//2, HEIGHT//2-125)

        mouse_pos = pygame.mouse.get_pos()

        for text, rect in buttons.items():
            color = LIGHT_GREY if rect.collidepoint(mouse_pos) else DARK_GREY
            pygame.draw.rect(scene, color, rect, border_radius=10)
            draw_text(text, button_font, WHITE, scene, rect.centerx, rect.centery)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for text, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return text.lower()

        pygame.display.flip()
        clock.tick(60)



def character_select():
    names = list(char_icons.keys())
    spacing = 200
    start_x = WIDTH//2 - spacing
    y = HEIGHT//2 - 40

    buttons = [(name, pygame.Rect(start_x + i * spacing, y, 80, 80))
               for i, name in enumerate(names)]

    journal_button = pygame.Rect(WIDTH//2 - 100, HEIGHT - 120, 200, 60)

    while True:
        scene.fill((40,80,120))
        draw_text("Choose Your Cat", title_font, WHITE, scene, WIDTH//2, 100)

        mouse_pos = pygame.mouse.get_pos()

        for name, rect in buttons:
            color = LIGHT_GREY if rect.collidepoint(mouse_pos) else DARK_GREY
            pygame.draw.rect(scene, color, rect.inflate(10,10), border_radius=10)
            scene.blit(char_icons[name], rect)

            label = button_font.render(name, True, WHITE)
            scene.blit(label, (rect.centerx - label.get_width()//2, rect.bottom + 10))

        jb_color = LIGHT_GREY if journal_button.collidepoint(mouse_pos) else DARK_GREY
        pygame.draw.rect(scene, jb_color, journal_button, border_radius=15)
        draw_text("Journal", button_font, WHITE, scene,
                  journal_button.centerx, journal_button.centery)

        
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return "back"

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in buttons:
                    if rect.collidepoint(event.pos):
                        return name
                if journal_button.collidepoint(event.pos):
                    journal_screen()

        pygame.display.flip()
        clock.tick(60)




def journal_screen():
    global player_collected_items
    your_collectibles = player_collected_items

    #Collectable icons
    item_icons = {}
    for map_data in COLLECTIBLES.values():
        for char_items in map_data.values():
            for item in char_items:
                path = item["image"]
                if item["name"] in your_collectibles and item["name"] not in item_icons:
                    icon = pygame.image.load(path).convert_alpha()
                    icon = pygame.transform.scale(icon, (48, 48))  # resize for journal
                    item_icons[item["name"]] = icon

    back_button = pygame.Rect(WIDTH//2 - 80, HEIGHT - 100, 160, 50)
    scroll_offset = 0
    SCROLL_SPEED = 30

    while True:
        scene.fill((30, 60, 90))
        draw_text("Journal", title_font, WHITE, scene, WIDTH//2, 70)
        if len(your_collectibles) < Total_Collectibles:
            counter_text = f"You've Collected {len(your_collectibles)} / {Total_Collectibles}"
        else:
            counter_text = f"You've Collected All {Total_Collectibles} items in the game!"
        draw_text(counter_text, button_font, WHITE, scene, WIDTH//2, 120)

        
        y = 160 + scroll_offset
        for item in your_collectibles:
            
            if item in item_icons:
                scene.blit(item_icons[item], (WIDTH//2 - 200, y - 20))  # left of text

            draw_text(item, button_font, WHITE, scene, WIDTH//2, y)
            y += 50


        
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            #adding scroll wheel to look at all collactables
            if event.type == MOUSEWHEEL:
                scroll_offset += event.y * SCROLL_SPEED
                min_offset = min(0, HEIGHT - (160 + len(your_collectibles)*50 + 50))
                scroll_offset = max(min_offset, min(0, scroll_offset))

        pygame.display.flip()
        clock.tick(60)



#Map Selection Screen
def map_select():
    names = list(map_icons.keys())
    spacing = 200
    start_x = WIDTH//2 - spacing
    y = HEIGHT//2 - 40

    buttons = [(name, pygame.Rect(start_x + i * spacing, y, 80, 80))
               for i, name in enumerate(names)]

    while True:
        scene.fill((40,80,120))
        draw_text("Choose Your Map", title_font, WHITE, scene, WIDTH//2, 100)

        mouse_pos = pygame.mouse.get_pos()

        for name, rect in buttons:
            color = LIGHT_GREY if rect.collidepoint(mouse_pos) else DARK_GREY
            pygame.draw.rect(scene, color, rect.inflate(10,10), border_radius=10)
            scene.blit(map_icons[name], rect)

            label = button_font.render(name, True, WHITE)
            scene.blit(label, (rect.centerx - label.get_width()//2, rect.bottom + 10))

        
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
                
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return "back"
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:

                for name, rect in buttons:
                    if rect.collidepoint(event.pos):
                        return name

        pygame.display.flip()
        clock.tick(60)



class Collectible:
    def __init__(self, name, image_path, pos):
        self.name = name
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


class Collectible_manager: #Spawns collactibles randomly throughout the maps
    def __init__(self, map_name, character_name):
        self.collectibles = []
        items = COLLECTIBLES[map_name][character_name]
        self.pickup_sound = pygame.mixer.Sound(r"Assets\leafrustle-92102.mp3")
        self.pickup_sound.set_volume(0.6)

        num_spawn = random.randint(5,25)
        for item in range(num_spawn):
            item = random.choice(items)
            pos = (random.randint(0, 1920), random.randint(0, 1080))
            c = Collectible(item["name"], item["image"], pos)
            self.collectibles.append(c)

    def update(self, player_rect, camera_x, camera_y):
        global player_collected_items
        for c in self.collectibles[:]:
            screen_rect = pygame.Rect(
                c.rect.x - camera_x,
                c.rect.y - camera_y,
                c.rect.width,
                c.rect.height
            )

            if player_rect.colliderect(screen_rect):
                if c.name not in player_collected_items: 
                    player_collected_items.append(c.name)
                
                self.pickup_sound.play()
                self.collectibles.remove(c)

    def draw(self, surface, camera_x, camera_y):
        for c in self.collectibles:
            c.draw(surface, camera_x, camera_y)






#Main Game loop Post-character selection and Map Selection
def run_game(player_sprite_path, chosen_map_name, chosen_character):
    

    
    collection_manager = Collectible_manager(chosen_map_name, chosen_character)


    
    #Load Sprite Sheet
    try:
        sprite_sheet = pygame.image.load(player_sprite_path).convert_alpha()
    except pygame.error as e:
        raise SystemExit(f"Failed to load sprite sheet '{player_sprite_path}': {e}")

    FRAME = 30 #size of sprite is 30x30 not 32x32
    ROWS, COLS = 4, 4

    
    sheet_w, sheet_h = sprite_sheet.get_width(), sprite_sheet.get_height()
    if sheet_w < COLS * FRAME or sheet_h < ROWS * FRAME:
        raise SystemExit(
            f"Sprite sheet too small: sheet size {sheet_w}x{sheet_h}, "
            f"expected at least {COLS*FRAME}x{ROWS*FRAME}."
        )

    
    animation_WASD = {"down": [], "left": [], "right": [], "up": []}
    dirs = ["down", "left", "right", "up"]

    for row in range(ROWS):
        direction = dirs[row]
        for col in range(COLS):
            rect = pygame.Rect(col * FRAME, row * FRAME, FRAME, FRAME)
            animation_WASD[direction].append(sprite_sheet.subsurface(rect).copy())

    
    game_map = full_maps[chosen_map_name]
    map_w, map_h = game_map.get_width(), game_map.get_height()

    #Starting position
    x, y = map_w // 2, map_h // 2

    current_dir = "down"
    frame_index, frame_timer = 0, 0
    FRAME_DELAY = 8
    speed = 4
    half_frame = FRAME // 2


    #Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return "back"

        #WASD movement
        keys = pygame.key.get_pressed()
        moving = False

        if keys[K_s]:
            current_dir = "down"; y += speed; moving = True
        elif keys[K_w]:
            current_dir = "up"; y -= speed; moving = True
        elif keys[K_a]:
            current_dir = "left"; x -= speed; moving = True
        elif keys[K_d]:
            current_dir = "right"; x += speed; moving = True

        
        x = max(half_frame, min(x, map_w - half_frame))
        y = max(half_frame, min(y, map_h - half_frame))

        #flick through images/frames
        if moving:
            frame_timer += 1
            if frame_timer >= FRAME_DELAY:
                frame_timer = 0
                frame_index = (frame_index + 1) % len(animation_WASD[current_dir])
        else:
            frame_index = 0

        
        camera_x = x - WIDTH // 2
        camera_y = y - HEIGHT // 2

        camera_x = max(0, min(camera_x, map_w - WIDTH))
        camera_y = max(0, min(camera_y, map_h - HEIGHT))

        
        scene.blit(game_map, (0, 0), (camera_x, camera_y, WIDTH, HEIGHT))

        
        player_screen_x = x - camera_x - half_frame
        player_screen_y = y - camera_y - half_frame

        #import collectables
        collection_manager.draw(scene, camera_x, camera_y)

        
        player_rect = pygame.Rect(player_screen_x, player_screen_y, FRAME, FRAME)
        collection_manager.update(player_rect, camera_x, camera_y)

        
        scene.blit(animation_WASD[current_dir][frame_index],
                   (player_screen_x, player_screen_y))

        pygame.display.flip()
        clock.tick(60)

        
#Run Game
choice = title_screen()

while True:
    choice = title_screen()

    if choice == "start!".lower():
        while True:
            chosen_character = character_select()
            if chosen_character == "back":
                break

            chosen_map = map_select()
            if chosen_map == "back":
                continue

            result = run_game(char_images[chosen_character], chosen_map, chosen_character)
            if result == "back":
                continue

            break

    elif choice == "load game":
        print("Load Game – not implemented yet!")

    elif choice == "exit":
        pygame.quit()
        sys.exit()








