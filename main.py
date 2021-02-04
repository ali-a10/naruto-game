import random
from character import *
pygame.init()


def main_menu():
    menu = True
    close = False

    while menu:
        window.fill((255, 215, 0))
        menu_font = pygame.font.SysFont('Agency FB', 100, True)
        inst_font = pygame.font.SysFont('Agency FB', 40, True)
        press_space1 = menu_font.render('Press Space to Start', 1,
                                        (255, 255, 255))
        inst_title = menu_font.render('Instructions', 1, (5, 14, 166))
        instructions1 = inst_font.render('Use arrows to move', 1, (5, 14, 166))
        instructions2 = inst_font.render('Space to throw weapon', 1,
                                         (5, 14, 166))
        instructions3 = inst_font.render('X for special ability', 1,
                                         (5, 14, 166))

        window.blit(press_space1, (150, 75))
        pygame.draw.rect(window, (255, 255, 255), (0, 208, win_width, 4))
        window.blit(inst_title, (288, 225))
        window.blit(instructions1, (365, 335))
        window.blit(instructions2, (350, 390))
        window.blit(instructions3, (375, 445))
        window.blit(menu_pic1, (720, 210))
        window.blit(menu_pic2, (0, 205))
        
        for event12 in pygame.event.get():
            if event12.type == pygame.QUIT:
                menu = False
                close = True

            if event12.type == pygame.KEYDOWN:
                if event12.key == pygame.K_SPACE:
                    menu = False

        pygame.display.update()
        clock.tick(5)
    if close:
        return False
    return True


def game_over():
    over = True

    while over:
        pygame.draw.rect(window, (0, 0, 0), (140, 90, 720, 370))  # (190, 110, 670, 350)
        pygame.draw.rect(window, (255, 255, 255), (150, 100, 700, 350))  # (200, 120, 650, 330)
        over_font = pygame.font.SysFont('Agency FB', 120, True)
        instruc_font = pygame.font.SysFont('Agency FB', 80, True)
        over_text = over_font.render('GAME OVER', 1, (0, 255, 0))
        press_r = instruc_font.render('Press R to Restart', 1,
                                      (0, 255, 0))

        window.blit(over_text, (275, 100))
        window.blit(press_r, (260, 270))
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                over = False
                pygame.quit()

            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_r:
                    player.curr_health = player.max_health
                    player.left = False
                    player.right = False
                    player.up = False
                    player.down = False
                    player.walkCount = 0
                    player.standing = True
                    player.throwing = False
                    player.x, player.y = 250, 220
                    over = False

        clock.tick(5)
        pygame.display.update()


# drawing function
def redraw_window(started: bool):
    window.blit(bg, (0, 70))

    pygame.draw.rect(window, (255, 215, 0), (0, 0, win_width, 69))
    pygame.draw.rect(window, (255, 255, 255), (2, 2, win_width - 4, 70), 5)
    score_text = score_font.render('Score = ' + str(score), 1, (139, 0, 0))
    high_text = score_font.render('High Score = ' + str(high_score), 1, (139, 0,
                                                                         0))
    health_text = score_font.render('Health', 1, (139, 0, 0))
    level_text = score_font.render('Level: ' + str(level), 1, (139, 0, 0))

    window.blit(score_text, (660, 20))
    window.blit(high_text, (825, 20))
    window.blit(health_text, (20, 20))
    window.blit(level_text, (520, 20))
    pygame.draw.rect(window, (139, 0, 0), (395, 7, 67, 61))
    window.blit(pygame.transform.scale(rasengan, (57, 56)), (400, 10))
    if ult_timer < 650:
        pygame.draw.rect(window, (139, 0, 0), (395, 7, 67,
                                               round(61 * ult_timer / 650)))

    player.draw(window)
    if not started:
        start_font = pygame.font.SysFont('Ink Free', 75, True)
        start_text = start_font.render('START', 1, (0, 0, 205))
        pygame.draw.ellipse(window, (255, 215, 0), (325, 95, 310, 210))
        pygame.draw.ellipse(window, (255, 255, 255), (330, 100, 300, 200))
        window.blit(start_text, (340, 140))
    else:
        for enemyy in curr_enemies:
            enemyy.draw(window)
        for archer in curr_archers:
            archer.draw(window)
        for weapon1 in player.weapons:
            weapon1.draw(window)
        if archer_in_lst:
            for enmy_wpn in arch1.arrow_lst:
                enmy_wpn.draw(window)

    pygame.display.update()


score = 0
high_score = 0
score_font = pygame.font.SysFont('arial', 25, True, True)
clock = pygame.time.Clock()
run = True
player = Character(250, 220)
spawn_y = [217, 317, 417]
curr_enemies = []
curr_archers = []
shoot_timer = 0
ult_timer = 650
enemy_wpns = []
menu1 = main_menu()
start_timer = 0
down_timer = 0
up_timer = 0
level = 1
archer_in_lst = False
puppet_in_lst = False
archer_timer = 0
vel_enmy = 3
ras_in_wpns = False

wpn_count = 0

# main loop
while run and menu1:
    clock.tick(40)
    if start_timer <= 60:
        start_timer += 1
        redraw_window(False)

    else:
        if player.curr_health > 0:
            level = score // 8 + 1

            if shoot_timer > 0:
                shoot_timer += 1
            if shoot_timer > 8:
                player.throwing = False
            if shoot_timer > 15:
                shoot_timer = 0

            if ult_timer < 650:
                ult_timer -= 1
            if ult_timer < 0:
                ult_timer = 650

            if down_timer <= 1:
                down_timer -= 0.2
            if down_timer < 0:
                down_timer = 0

            if up_timer <= 1:
                up_timer -= 0.2
            if up_timer < 0:
                up_timer = 0

            if archer_timer > 100:
                archer_timer = 0
            else:
                archer_timer += 1

            if not ras_in_wpns:
                if level >= 4:
                    if len(curr_enemies) < 5 and not puppet_in_lst:
                        curr_enemies.append(Puppets(900, random.choice(spawn_y),
                                                    6))
                        puppet_in_lst = True
                    vel_enmy = 4

                if level >= 3:
                    if not archer_in_lst and archer_timer == 0:
                        enmy_y1 = random.choice(spawn_y)
                        curr_enemies.append(Archers(win_width - 80, enmy_y1,
                                                    enmy_y1 + 100))
                        arch1 = curr_enemies[-1]
                        archer_in_lst = True

                if archer_timer != 0 and level > 0:
                    if level > 5 and curr_enemies:
                        while len(curr_enemies) < 6:
                            enmy_y = random.choice(spawn_y)
                            curr_enemies.append(SandEnemy(1000, enmy_y,
                                                          vel_enmy))

                    else:
                        while len(curr_enemies) < level:
                            enmy_y = random.choice(spawn_y)
                            curr_enemies.append(SandEnemy(1000, enmy_y,
                                                          vel_enmy))

                if level >= 5:
                    vel_enmy = 5

                if level >= 7:
                    vel_enmy = 6

            if archer_in_lst:
                for a in arch1.arrow_lst:
                    if player.y <= a.y <= player.y + player.height and \
                            player.x <= a.x + a.width <= player.x + \
                            player.width:
                        player.curr_health -= 2
                        arch1.arrow_lst.pop(arch1.arrow_lst.index(a))

                    if win_width > a.x > 0:
                        a.x -= a.velocity
                    else:
                        arch1.arrow_lst.pop(arch1.arrow_lst.index(a))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            weapons2 = player.weapons.copy()
            for weapon in weapons2:
                for enemy1 in curr_enemies:
                    if enemy1.y <= weapon.y <= enemy1.y + enemy1.height and \
                            enemy1.x <= weapon.x + weapon.width <= enemy1.x + \
                            enemy1.width and enemy1.stop is False:

                        if ras_in_wpns:
                            enemy1.curr_health = 0
                        else:
                            enemy1.curr_health -= 1
                            player.weapons.discard(weapon)

                if win_width > weapon.x > 0:
                    weapon.x += weapon.velocity
                else:
                    if ras_in_wpns:
                        player.weapons.clear()
                        ras_in_wpns = False
                    else:
                        player.weapons.discard(weapon)

            keys = pygame.key.get_pressed()

            for enemy in curr_enemies:
                if enemy.x <= 0:
                    if score > 0:
                        score -= 1
                    player.curr_health -= 1
                if enemy.curr_health <= 0 or enemy.x <= 0:
                    if enemy.curr_health <= 0:
                        score += 1
                    if isinstance(enemy, Archers):
                        archer_in_lst = False
                        archer_timer = 1
                    if isinstance(enemy, Puppets):
                        puppet_in_lst = False
                    curr_enemies.remove(enemy)

            if keys[pygame.K_LEFT] and player.x - player.velocity >= 0:
                player.x -= player.velocity
                player.left = True
                player.right = False
                player.standing = False

            elif keys[pygame.K_RIGHT] and player.x + player.velocity <= \
                    (win_width - player.width):
                player.x += player.velocity
                player.left = False
                player.right = True
                player.standing = False

            else:
                player.standing = True
                player.walkCount = 0

            if keys[pygame.K_DOWN] and player.y < 420 and down_timer == 0:
                player.down = True
                down_timer = 1

            if keys[pygame.K_UP] and player.y > 220 and up_timer == 0:
                player.up = True
                up_timer = 1

            if keys[pygame.K_SPACE] and shoot_timer == 0:
                if len(player.weapons) < 4:
                    player.throwing = True
                    if player.left:
                        w = Weapon(player.x, round(player.y +
                                                   player.height // 4)
                                   - 4, -1)
                        player.weapons.add(w)
                    else:
                        w2 = Weapon(player.x + player.width,
                                    round(player.y + player.height // 4)
                                    - 4, 1)
                        player.weapons.add(w2)
                shoot_timer = 1

            if keys[pygame.K_x] and ult_timer == 650:
                player.weapons.clear()
                player.ult = True
                player.u_count = 0
                if player.left:
                    ult = Ultimate(player.x, 200, -1)
                ras_in_wpns = True
                enemy_wpns.clear()
                pygame.display.update()
                ult_timer = 649

            redraw_window(True)

        if player.curr_health <= 0:
            level = 1
            if score > high_score:
                high_score = score
            score = 0
            vel_enmy = 3
            curr_enemies.clear()
            archer_in_lst = False
            player.weapons.clear()
            start_timer = 0
            shoot_timer = 0
            ult_timer = 0
            game_over()

pygame.quit()
