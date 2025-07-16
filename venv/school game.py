import pygame
import random
import math

#python clock
pygame.init()
clock = pygame.time.Clock()
start_scherm = True

# Kleuren
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
lBLUE = (0, 0, 150)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
YELLOW = (225, 225, 50)
ORANGE = (255, 140, 0)
PURPLE = (76, 19, 163)
GOLD = (255, 215, 0)
sky_blue = (137, 210, 255)
highscore = 928.7

# Scherm instellingen
WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Fonts
font = pygame.font.SysFont("Showcard Gothic", 100)
small_font = pygame.font.SysFont("Impact", 30)
death_font = pygame.font.SysFont("Wide Latin", 100)

# Sterren voor startscherm
stars = [(random.randint(0, 1920), random.randint(0, 1080)) for _ in range(100)]
pulse = 0
pulse_direction = 5


# Healthbar functie
def draw_health_bar(surface, x, y, health, max_health):
    bar_width = 300
    bar_height = 25
    fill = (health / max_health) * bar_width
    border_color = (0, 0, 0)
    fill_color = (200, 0, 0)
    background_color = (100, 100, 100)

    pygame.draw.rect(surface, background_color, (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, fill_color, (x, y, fill, bar_height))
    pygame.draw.rect(surface, border_color, (x, y, bar_width, bar_height), 2)


# Startscherm tekenen
def draw_start_screen(pulse_alpha):
    SCREEN.fill((10, 10, 50))
    for x, y in stars:
        pygame.draw.circle(SCREEN, (255, 255, 255), (x, y), 1)
    title_text = font.render("OUT OF LINE", True, (255, 255, 255))
    shadow = font.render("OUT OF LINE", True, (50, 50, 100))
    SCREEN.blit(shadow, (WIDTH // 2 - shadow.get_width() // 2 + 6, HEIGHT // 3 + 6))
    SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    instruction_text = small_font.render("Druk op SPATIE om te starten", True, (255, pulse_alpha, pulse_alpha))
    SCREEN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 100))
    quit_text = small_font.render("Druk op Q om te stoppen", True, (180, 180, 180))
    SCREEN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 140))
    quit_text = small_font.render("HIGH SCORE: " + str(round(int((highscore / 250 - 3.7)))) + " METER", True, (255, 0, 0))
    SCREEN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT - 1000))
    pygame.display.update()


# Death-scherm functie
def draw_death_screen(score):
    SCREEN.fill((30, 0, 0))
    death_text = death_font.render("GAME OVER", True, RED)
    score_text = small_font.render(f"Jouw score: {round(int((score / 250 - 3.7)))} meter", True, WHITE)
    retry_text = small_font.render("Druk op SPATIE om door te gaan", True, WHITE)

    SCREEN.blit(death_text, (WIDTH // 2 - death_text.get_width() // 2, HEIGHT // 3))
    SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    SCREEN.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    #knoppen
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    global start_scherm
                    start_scherm = True

#lucht en scroller
bg = pygame.image.load("lucht.png").convert()
bg = pygame.transform.scale(bg, (1900, 1000))
bg_width = bg.get_width()
bg_rect = bg.get_rect()
scroll = 0
tiles = math.ceil(WIDTH / bg_width) + 1

#speler texture
playerIMG = pygame.image.load("player img spel.png")
playerIMGspringen = pygame.image.load("player spel in de lucht.png")
playerIMGdmg = pygame.image.load("player img dmg.png")
climb_img = pygame.image.load("klimmen.png")
player_jumping_dmg_img = pygame.image.load("player jump damage.png")
player_climbing_dmg_img = pygame.image.load("player climb dmg.png")

#enemy texture
PolitieLVL1 = pygame.image.load("popo voor game.png")
PolitieLVL2 = pygame.image.load("popo voor game 2.png")
PolitieLVL2_5 = pygame.image.load("politie lvl2.png")
PolitieLVL3 = pygame.image.load("politie lvl3.png")
PolitieLVL4 = pygame.image.load("politie lvl4.png")
Politiereinforcement = pygame.image.load("p_reinforcement.png")
taser_dude_img = pygame.image.load("p_taser dude.png")
army_ranger_img = pygame.image.load("p_army ranger.png")

#extra texture
ground_texture = pygame.image.load("ground.png")
super_jump_img = pygame.image.load("jump_boost.png")
health_boost_img = pygame.image.load("health_boost.png")
grenade_img = pygame.image.load("grenade.png")
explosion_img = pygame.image.load("explosion.png")

#gebouwen texture
Gebouw1 = pygame.image.load("gebouw 2.png")
Gebouw2 = pygame.image.load("gebouw 3.png")
Gebouw3 = pygame.image.load("gebouw 4.png")

#hoofdloop
while True:
    #startscherm
    if start_scherm:
        pulse += pulse_direction
        if pulse >= 255 or pulse <= 50:
            pulse_direction *= -1
        draw_start_screen(pulse)

        #het spel uit kunnen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_scherm = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

    #hoofdgame
    if not start_scherm:
        #wapen en enemy variabelen
        timer = 0
        last_enemy1_spawn_x = -7500
        last_enemy2_spawn_x = 0
        last_enemy3_spawn_x = 0
        last_taser_spawn_x = 0
        last_police_spawn_x = 0
        last_police2_spawn_x = 0
        last_army_spawn_x = 0
        last_grenade_spawn_x = 0
        last_super_jump_spawn_x = 0
        last_heal_spawn_x = 0
        max_amount = 3
        max_amount2 = 2

        #speler en rest varabelen
        last_ground_spawn = -3000
        platform_y = 500
        platform_x = 1000
        player_width = 50
        player_height = 50
        player_x = WIDTH // 2 - player_width // 2
        player_y = HEIGHT // 2 - player_height // 2
        player_speed = 17
        player_jump_strength = 13
        player_velocity_y = 0
        player_gravity = 0.8
        camera_x = 0
        camera_y = 0
        score = 0
        health = 100
        enemy_height = 50
        enemy_width = 50
        color = BLUE

        #plaatjes ook kunnen flippen
        playerIMG_right = playerIMG
        playerIMG_left = pygame.transform.flip(playerIMG, True, False)

        playerIMGspringen_right = playerIMGspringen
        playerIMGspringen_left = pygame.transform.flip(playerIMGspringen, True, False)

        player_jumping_dmg_img_right = player_jumping_dmg_img
        player_jumping_dmg_img_left = pygame.transform.flip(player_jumping_dmg_img, True, False)

        player_climbing_dmg_img_right = player_climbing_dmg_img
        player_climbing_dmg_img_left = pygame.transform.flip(player_climbing_dmg_img, True, False)

        playerIMG_dmg_right = playerIMGdmg
        playerIMG_dmg_left = pygame.transform.flip(playerIMGdmg, True, False)

        player_klim_right = climb_img
        player_klim_left = pygame.transform.flip(climb_img, True, False)

        playerIMG_now = playerIMG_right
        player_climbing_dmg_img_now = player_climbing_dmg_img_right
        playerIMGspringen_now = playerIMGspringen_right
        player_jumping_dmg_img_now = player_jumping_dmg_img_right
        playerIMGdmg_now = playerIMG_dmg_right
        player_klim_now = player_klim_right

        #True/ False variabelen
        player_jumping = False
        hurting = False
        climbing = False
        calling = False
        movable = True
        super_jump = False
        right = True
        left = False

        groundlevel = HEIGHT - 150

        #gebouwen maken
        gebouw_images = [Gebouw1, Gebouw2, Gebouw3]
        y_platform = [
            (
                random.randint(1000, 5000000),
                random.randint(50, 400),
                random.randint(400, 900),
                1000,
                random.choice(gebouw_images)
            )
            for _ in range(2000)
        ]

        #lists
        enemies_type_1 = []
        enemies_type_2 = []
        enemies_type_3 = []
        reinforcements = []
        taser_dudes = []
        police_officer = []
        police_officer2 = []
        army_rangers = []
        items = []
        ground = []

        #definities
        #maak de grond
        def get_ground_height(x):
            return HEIGHT - 150

        def make_ground():
            global last_ground_spawn
            ground.append({'x': last_ground_spawn + 512
                           })
            last_ground_spawn = last_ground_spawn + 512

        #platform colission
        def check_platform_collision(px, py, pw, ph, vx, vy):
            for plat_x, plat_y, plat_w, plat_h, plat_img in y_platform:
                future_px = px + vx
                future_py = py + vy
                if px + pw > plat_x and px < plat_x + plat_w and py + ph > plat_y and py < plat_y + plat_h:
                    if vy > 0 and py + ph - vy <= plat_y:
                        return 'vertical', plat_y

                platform_rect = pygame.Rect(plat_x, plat_y, plat_w, plat_h)
                player_rect = pygame.Rect(future_px, future_py, pw, ph)

                if player_y <= 800:
                    if player_rect.colliderect(platform_rect):
                        if vx > 0 and px + pw <= plat_x:
                            return 'right', plat_x - pw
                        if vx < 0 and px >= plat_x + plat_w:
                            return 'left', plat_x + plat_w

            return None, None

        #alle individuele enemy's en items toevoegen
        def spawn_enemy():
            global last_enemy1_spawn_x
            if player_x - last_enemy1_spawn_x >= 7500:
                x = player_x + 1920
                y = HEIGHT - 100
                #alle individuele variabelen
                enemies_type_1.append(
                    {'x': x, 'y': y, 'width': 50, 'height': 50, 'acceleration': 0, 'color': RED, 'damage': 10,
                     'speed': 1, 'image': PolitieLVL1})
                last_enemy1_spawn_x = player_x


        def spawn_enemy2():
            global last_enemy2_spawn_x
            if player_x - last_enemy2_spawn_x >= 10000:
                x = player_x + 1920
                y = HEIGHT - 100
                enemies_type_2.append(
                    {'x': x, 'y': y, 'width': 50, 'height': 50, 'acceleration': 0, 'color': PURPLE, 'damage': 20,
                     'speed': 0.75, 'image': PolitieLVL3})
                last_enemy2_spawn_x = player_x


        def spawn_enemy3():
            global last_enemy3_spawn_x, calling
            if player_x - last_enemy3_spawn_x >= 20000:
                x = player_x + 1920
                y = HEIGHT - 100
                enemies_type_3.append(
                    {'x': x, 'y': y, 'width': 70, 'height': 75, 'acceleration': 0, 'color': GOLD, 'damage': 25,
                     'speed': 0.5, 'image': PolitieLVL4})
                last_enemy3_spawn_x = player_x
                calling = True


        def reinforcement():
            x = player_x + 1920
            y = HEIGHT - 100
            reinforcements.append(
                {'x': x, 'y': y, 'width': 40, 'height': 40, 'acceleration': 0, 'color': GOLD, 'damage': 10,
                 'speed': 0.7, 'image': Politiereinforcement,})


        def taser_dude():
            global last_taser_spawn_x
            if player_x - last_taser_spawn_x >= 10000:
                x = player_x + 1920
                y = HEIGHT - 100
                taser_dudes.append(
                    {'x': x, 'y': y, 'width': 50, 'height': 50, 'acceleration': 0, 'color': lBLUE, 'damage': 0,
                     'speed': 0.6, 'timer': 0, 'timer2': 0, 'cooldown': False, 'in_range': False, 'image': taser_dude_img,})
                last_taser_spawn_x = player_x


        def police():
            global last_police_spawn_x
            if player_x - last_police_spawn_x >= 10000:
                x = player_x + 1920
                y = HEIGHT - 100
                police_officer.append(
                    {'x': x, 'y': y, 'width': 50, 'height': 50, 'acceleration': 0, 'color': YELLOW, 'bullet_damage': 40, 'damage': 0,
                     'speed': 0.6, 'timer': 0, 'cooldown': False, 'in_range': False, 'shooting': False,
                     'bullet_x': 0, 'bullet_y': 600, 'x_heading': 0, 'y_heading': 0, 'cooldown_len': 100, 'image': PolitieLVL2,})
                last_police_spawn_x = player_x

        def army():
            global last_army_spawn_x
            if player_x - last_army_spawn_x >= 15000:
                x = player_x + 1920
                y = HEIGHT - 100
                army_rangers.append(
                    {'x': x, 'y': y, 'width': 50, 'height': 50, 'acceleration': 0, 'color': YELLOW, 'bullet_damage': 20, 'damage': 0,
                     'speed': 0.6, 'timer': 0, 'cooldown': False, 'in_range': False, 'shooting': False,
                     'bullet_x': 0, 'bullet_y': 600, 'x_heading': 0, 'y_heading': 0, 'cooldown_len': 0, 'image': army_ranger_img,})
                last_army_spawn_x = player_x

        def spawn_grenades():
            global last_grenade_spawn_x
            if player_x - last_grenade_spawn_x >= 12500:
                x = player_x + 2500
                y = get_ground_height(x) - 25

                items.append(
                    {'x': x, 'y': y, 'timer': 0, 'type': "grenade", 'item_on_ground': True, 'falling_item': False,
                     'explosion': False, 'item_in_inv': False, 'image': grenade_img})
                last_grenade_spawn_x = player_x


        #werking explosies
        def check_explosion_range(grenade_x, grenade_y, explosion_radius):
            for enemy in enemies_type_1 + enemies_type_2 + enemies_type_3 + reinforcements + taser_dudes + police_officer + army_rangers:
                distance = ((enemy['x'] - grenade_x) ** 2 + (enemy['y'] - grenade_y) ** 2) ** 0.5
                if distance <= explosion_radius:
                    if enemy in enemies_type_1:
                        enemies_type_1.remove(enemy)
                    elif enemy in enemies_type_2:
                        enemies_type_2.remove(enemy)
                    elif enemy in enemies_type_3:
                        enemies_type_3.remove(enemy)
                    elif enemy in reinforcements:
                        reinforcements.remove(enemy)
                    elif enemy in taser_dudes:
                        taser_dudes.remove(enemy)
                    elif enemy in police_officer:
                        police_officer.remove(enemy)
                    elif enemy in army_rangers:
                        army_rangers.remove(enemy)

        #spawn de super krachten
        def spawn_jumps():
            global last_super_jump_spawn_x
            if player_x - last_super_jump_spawn_x >= 10000:
                x = player_x + 2500
                y = get_ground_height(x) - 25
                items.append(
                    {'x': x, 'y': y, 'type': "super_jump", 'item_on_ground': True, 'falling_item': False, 'item_in_inv': False, 'image': super_jump_img})
                last_super_jump_spawn_x = player_x

        def spawn_heals():
            global last_heal_spawn_x
            if player_x - last_heal_spawn_x >= 15000:
                x = player_x + 2500
                y = get_ground_height(x) - 25
                items.append(
                    {'x': x, 'y': y, 'type': "heal", 'item_on_ground': True, 'falling_item': False, 'item_in_inv': False, 'image': health_boost_img})
                last_heal_spawn_x = player_x

        def if_jump():
            global super_jump
            super_jump = True

        def heal():
            global health
            health = 100

        #main game
        running = True
        while running:
            pygame.time.delay(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                running = False

            #roep de reïnforcements
            if calling:
                reinforcement()
                reinforcement()
                reinforcement()
                calling = False

            #score bijhouden
            if player_x > score:
                score = player_x

            #beweging player
            velocity_x = 0
            if movable is True:
                #naar links
                if keys[pygame.K_LEFT]:
                    velocity_x = -player_speed
                    right = False
                    left = True
                    playerIMG_now = playerIMG_left
                    player_climbing_dmg_img_now = player_climbing_dmg_img_left
                    player_jumping_dmg_img_now = player_jumping_dmg_img_left
                    playerIMGspringen_now = playerIMGspringen_left
                    playerIMGdmg_now = playerIMG_dmg_left
                    player_klim_now = player_klim_left

                #naar rechts
                if keys[pygame.K_RIGHT]:
                    velocity_x = player_speed
                    right = True
                    left = False
                    playerIMG_now = playerIMG_right
                    player_climbing_dmg_img_now = player_climbing_dmg_img_right
                    player_jumping_dmg_img_now = player_jumping_dmg_img_right
                    playerIMGspringen_now = playerIMGspringen_right
                    playerIMGdmg_now = playerIMG_dmg_right
                    player_klim_now = player_klim_right

            #botsing tegen gebouw
            collision_type, collision_pos = check_platform_collision(player_x, player_y, player_width, player_height,
                                                                     velocity_x, 0)
            #soort tegen zijkant
            if collision_type == 'right':
                climbing = True
                player_jumping = False
                player_x = collision_pos
                velocity_x = 0
                player_velocity_y = -10
            elif collision_type == 'left':
                climbing = True
                player_jumping = False
                player_x = collision_pos
                velocity_x = 0
                player_velocity_y = -10
            else:
                climbing = False
                player_x += velocity_x

            platform_collision_type, platform_y_pos = check_platform_collision(player_x, player_y + player_velocity_y,
                                                                               player_width, player_height, 0,
                                                                               player_velocity_y)
            #botsing van boven
            if platform_collision_type == 'vertical' and player_velocity_y > 0:
                if player_y + player_height <= platform_y_pos + player_velocity_y:
                    player_y = platform_y_pos - player_height
                    player_velocity_y = 0
                    player_jumping = True

            #spring functie
            if movable is True:
                if (player_y >= get_ground_height(
                        player_x) - player_height or platform_collision_type == 'vertical') and keys[pygame.K_UP]:
                    if not super_jump:
                        player_velocity_y = -player_jump_strength
                        player_jumping = True
                    elif super_jump:
                        player_velocity_y = -player_jump_strength * 2
                        super_jump = False
                        player_jumping = True


            player_y += player_velocity_y
            player_velocity_y += player_gravity

            if player_y >= get_ground_height(player_x) - player_height:
                player_y = get_ground_height(player_x) - player_height
                player_velocity_y = 0
                player_jumping = False

            #spawn alle enemy's
            if len(enemies_type_1) < 5: spawn_enemy()
            if len(enemies_type_2) < 3: spawn_enemy2()
            if len(enemies_type_3) < 1: spawn_enemy3()
            if len(taser_dudes) < 2: taser_dude()
            if len(police_officer) < 3: police()
            if len(army_rangers) < 3: army()
            spawn_grenades()
            spawn_jumps()
            spawn_heals()

            #damage model
            if hurting:
                timer += 10
            if timer >= 250:
                timer = 0
                hurting = False
                color = BLUE

            #speler centraal
            camera_x = player_x - WIDTH // 2
            camera_y = player_y - HEIGHT // 2

            #achtergrond en grond
            SCREEN.fill(sky_blue)
            make_ground()

            #leeft de speler nog
            if health <= 0:
                running = False

            #teken de grond texture en de lucht:
            for i in range(0, tiles):
                SCREEN.blit(bg, (i * bg_width + scroll, 0))
                bg_rect.x = i * bg_width + scroll
                pygame.draw.rect(SCREEN, (137, 210, 255), bg_rect, 1)

            scroll -= 5
            if abs(scroll) > bg_width:
                scroll = 0

            #teken de gebouwen
            for plat_x, plat_y, plat_w, plat_h, plat_img in y_platform:
                if -150 < plat_x - camera_x < WIDTH + 150:
                    scaled_img = pygame.transform.scale(plat_img, (plat_w, plat_h))
                    SCREEN.blit(scaled_img, (plat_x - camera_x, plat_y - camera_y))

            #de functie van alle enemy's op basis van de enemy waarden
            for enemy in enemies_type_1 + enemies_type_2 + enemies_type_3 + reinforcements + taser_dudes + police_officer + army_rangers:
                direction = 1 if player_x > enemy['x'] else -1
                if random.random() < 0.2:
                    enemy['acceleration'] += direction * random.uniform(1.5, 1.8) * enemy['speed']
                enemy['acceleration'] *= 0.98
                enemy['x'] += enemy['acceleration']
                enemy['y'] = get_ground_height(enemy['x']) - enemy['height']

                if not hurting and enemy not in (taser_dudes or police_officer):
                    if (player_x < enemy['x'] + enemy['width'] and player_x + player_width > enemy['x'] and
                            player_y < enemy['y'] + enemy['height'] and player_y + player_height > enemy['y']):
                        color = ORANGE
                        health -= enemy['damage']
                        hurting = True

                #herspawnen enemy's
                if enemy['x'] < player_x - 2500:
                    if enemy in enemies_type_1:
                        enemies_type_1.remove(enemy)
                    elif enemy in enemies_type_2:
                        enemies_type_2.remove(enemy)
                    elif enemy in enemies_type_3:
                        enemies_type_3.remove(enemy)
                    elif enemy in reinforcements:
                        reinforcements.remove(enemy)
                    elif enemy in taser_dudes:
                        taser_dudes.remove(enemy)
                    elif enemy in police_officer:
                        police_officer.remove(enemy)
                    elif enemy in army_rangers:
                        army_rangers.remove(enemy)

                #werking van de taser
                if not hurting and enemy in taser_dudes:
                    if enemy['cooldown'] is False:
                        if ((enemy['x'] - player_x) ** 2 + (enemy['y'] - player_y) ** 2) <= 50000:
                            enemy['in_range'] = True

                        if enemy['in_range'] is True:
                            pygame.draw.line(SCREEN, BLUE, (enemy['x'] - camera_x + 25, enemy['y'] - camera_y + 25),
                                             (player_x - camera_x + 25, player_y - camera_y + 25), 8)
                            pygame.draw.line(SCREEN, GOLD   , (enemy['x'] - camera_x + 25, enemy['y'] - camera_y + 28),
                                             (player_x - camera_x + 25, player_y - camera_y + 25), 1)
                            pygame.draw.line(SCREEN, GOLD, (enemy['x'] - camera_x + 25, enemy['y'] - camera_y + 22),
                                             (player_x - camera_x + 25, player_y - camera_y + 25), 1)
                            enemy['timer'] += 1
                            velocity_x = 0
                            movable = False
                        if enemy['timer'] == 25:
                            enemy['timer'] = 0
                            enemy['in_range'] = False
                            movable = True
                            enemy['cooldown'] = True

                    if enemy['cooldown'] is True:
                        enemy['timer2'] += 1
                        if enemy['timer2'] == 100:
                            enemy['cooldown'] = False
                            enemy['timer2'] = 0

                #werking kogels
                if not hurting and enemy in (police_officer or army_rangers):
                    if enemy['shooting'] is False:
                        if enemy['cooldown'] is False:
                            if ((enemy['x'] - player_x) ** 2 + (enemy['y'] - player_y) ** 2) <= 450000:
                                enemy['in_range'] = True

                            if enemy['in_range'] is True:
                                enemy['bullet_x'] = enemy['x'] + 25
                                enemy['bullet_y'] = enemy['y'] + 25
                                enemy['x_heading'] = (player_x - enemy['x']) / 15
                                enemy['y_heading'] = (player_y - enemy['y']) / 15
                                enemy['shooting'] = True

                    if enemy['shooting'] is True:
                        enemy['bullet_x'] += enemy['x_heading']
                        enemy['bullet_y'] += enemy['y_heading']
                        pygame.draw.rect(SCREEN, YELLOW,
                                         (enemy['bullet_x'] - camera_x, enemy['bullet_y'] - camera_y, 8, 8))

                        if (player_x < enemy['bullet_x'] + 8 and player_x + player_width > enemy['bullet_x'] and
                                player_y < enemy['bullet_y'] + 8 and player_y + player_height > enemy['bullet_y']):
                            enemy['shooting'] = False
                            health -= enemy['bullet_damage']
                            hurting = True
                            enemy['cooldown'] = True

                        if enemy['bullet_x'] <= player_x - 1920 or enemy['bullet_x'] >= player_x + 1920 or enemy[
                            'bullet_y'] <= player_y - 1080 or enemy['bullet_y'] >= player_y + 1080:
                            enemy['shooting'] = False
                            enemy['cooldown'] = True

                    if enemy['cooldown'] is True:
                        enemy['timer'] += 1
                        if enemy['timer'] == enemy['cooldown_len']:
                            enemy['cooldown'] = False
                            enemy['timer'] = 0

            #functioneren verschillende items
            for item in items:
                if item['falling_item'] is False:
                    item['y'] = get_ground_height(item['x']) - 45

                if item['falling_item'] is True:
                    if item['y'] <= get_ground_height(item['x']) - 50:
                        item['y'] = item['y'] + 8
                    if item['type'] == "grenade":
                        item['timer'] = item['timer'] + 1
                        if item['timer'] == 25:
                            item['item_on_ground'] = False
                            item['explosion'] = True

                if item['falling_item'] is False:
                    if (player_x < item['x'] + 25 and
                            player_x + player_width > item['x'] and
                            player_y < item['y'] + 25 and
                            player_y + player_height > item['y']):
                        item['item_on_ground'] = False
                        item['item_in_inv'] = True

                if item['item_on_ground'] is True:
                    SCREEN.blit(item['image'], (item['x'] - camera_x, item['y'] - camera_y, 25, 25))

                #werking grenaat
                if item['type'] == "grenade":
                    if item['item_on_ground'] is False and keys[pygame.K_SPACE] and item['item_in_inv'] is True:
                        item['timer'] = 0
                        item['x'] = player_x
                        item['y'] = player_y
                        item['item_in_inv'] = False
                        item['falling_item'] = True
                        item['item_on_ground'] = True

                    if item['explosion'] is True:
                        SCREEN.blit(explosion_img, (item['x'] - camera_x - 125, item['y'] - camera_y - 250, 250, 250))
                        movable = True

                        check_explosion_range(item['x'], item['y'], 150)

                        if item['timer'] == 30:
                            item['explosion'] = False

                #werking super jump
                if item['type'] == "super_jump":
                    if item['item_on_ground'] is False and item['item_in_inv'] is True:
                        if_jump()
                        item['item_in_inv'] = False

                #wering heal
                if item['type'] == "heal":
                    if item['item_on_ground'] is False and item['item_in_inv'] is True:
                        heal()
                        item['item_in_inv'] = False

            #health
            draw_health_bar(SCREEN, 30, 30, health, 100)

            #alle beweging staten speler
            if hurting and not player_jumping and not climbing:
                SCREEN.blit(playerIMGdmg_now,
                            (player_x - camera_x, player_y - camera_y, player_width, player_height))
            elif player_jumping and not hurting:
                SCREEN.blit(playerIMGspringen_now,
                            (player_x - camera_x, player_y - camera_y, player_width, player_height))
            elif player_jumping and hurting:
                SCREEN.blit(player_jumping_dmg_img_now,
                            (player_x - camera_x, player_y - camera_y, player_width, player_height))
            elif climbing and not hurting:
                SCREEN.blit(player_klim_now,
                            (player_x - camera_x, player_y - camera_y, player_width, player_height))
            elif climbing and hurting:
                SCREEN.blit(player_climbing_dmg_img_now,
                            (player_x - camera_x, player_y - camera_y, player_width, player_height))
            else:
                SCREEN.blit(playerIMG_now, (player_x - camera_x, player_y - camera_y, player_width, player_height))

            #teken alle enemy's
            for enemy in enemies_type_1 + enemies_type_2 + enemies_type_3 + reinforcements + police_officer + taser_dudes + army_rangers:
                facing_right = player_x > enemy['x']
                enemy_img = enemy['image']
                if not facing_right:
                    enemy_img = pygame.transform.flip(enemy_img, True, False)

                scaled_img = pygame.transform.scale(enemy_img, (enemy['width'], enemy['height']))
                SCREEN.blit(scaled_img, (enemy['x'] - camera_x, enemy['y'] - camera_y))

            #teken de grond
            for g in ground:
                SCREEN.blit(ground_texture, (g['x'] - camera_x, groundlevel - camera_y, 512, 512))

            pygame.display.update()
            clock.tick(45)

        #update de highscore
        if score > highscore:
            highscore = score

        #wanneer dood
        draw_death_screen(score)