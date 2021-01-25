import pygame
pygame.init()

win_width = 1000
win_length = 520
window = pygame.display.set_mode((win_width, win_length))

pygame.display.set_caption("naruto")

# images
walkLeft = [pygame.image.load('images/L1.png'),
            pygame.image.load('images/L2.png'),
            pygame.image.load('images/L3.png'),
            pygame.image.load('images/L4.png'),
            pygame.image.load('images/L5.png'),
            pygame.image.load('images/L6.png'),
            pygame.image.load('images/L7.png')]

walkRight = [pygame.transform.flip(walkLeft[0], True, False),
             pygame.transform.flip(walkLeft[1], True, False),
             pygame.transform.flip(walkLeft[2], True, False),
             pygame.transform.flip(walkLeft[3], True, False),
             pygame.transform.flip(walkLeft[4], True, False),
             pygame.transform.flip(walkLeft[5], True, False),
             pygame.transform.flip(walkLeft[6], True, False)]


bg = pygame.transform.scale(pygame.image.load('images/bg14.png'), (1000, 600))
char_l = pygame.image.load('images/l_stand.png')
char_r = pygame.transform.flip(char_l, True, False)
down_r = pygame.image.load('images/r_down.png')
down_l = pygame.transform.flip(down_r, True, False)
up_r = pygame.transform.flip(down_r, False, True)
up_l = pygame.transform.flip(up_r, True, False)
up_standing = pygame.image.load('images/r_up.png')
down_standing = pygame.transform.flip(up_standing, False, True)
throwing_r = pygame.image.load('images/throw.png')
throwing_l = pygame.transform.flip(throwing_r, True, False)
kunai_l = pygame.transform.scale(pygame.image.load('images/kunai.png'), (44, 33))
kunai_r = pygame.transform.flip(kunai_l, True, False)
arrow = pygame.transform.flip(pygame.image.load('images/enemies/arrow.png'),
                              True, False)
jutsu = pygame.image.load('images/jutsu.png')
rasengan = pygame.image.load('images/rasengan1.png')
smoke = pygame.image.load('images/smoke.png')


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = char_r.get_width()
        self.height = char_r.get_height()
        self.velocity = 5
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.standing = True
        self.throwing = False
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.max_health = 1
        self.curr_health = self.max_health
        self.ult = False
        self.u_count = 0
        self.weapons = set()

    def draw(self, win):
        if not self.ult:
            if self.walkCount + 1 >= 18:
                self.walkCount = 0

            if not self.standing:
                if self.left:
                    if self.up:
                        win.blit(up_l, (self.x, self.y - self.height))
                        self.y -= 100
                        self.up = False
                    elif self.down:
                        win.blit(down_l, (self.x, self.y))
                        self.y += 100
                        self.down = False
                    win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                    self.width = walkLeft[self.walkCount//3].get_width()
                    self.height = walkLeft[self.walkCount//3].get_height()
                    self.walkCount += 1

                elif self.right:
                    if self.up:
                        win.blit(up_r, (self.x, self.y - self.height))
                        self.y -= 100
                        self.up = False
                    elif self.down:
                        win.blit(down_r, (self.x, self.y))
                        self.down = False
                        self.y += 100
                    win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                    self.width = walkRight[self.walkCount//3].get_width()
                    self.height = walkRight[self.walkCount//3].get_height()

            else:
                if self.left:
                    if self.up:
                        win.blit(up_standing, (self.x, self.y - self.height))
                        self.y -= 100
                        self.up = False
                    elif self.down:
                        win.blit(down_standing, (self.x, self.y))
                        self.y += 100
                        self.down = False

                    if self.throwing:
                        win.blit(throwing_l, (self.x, self.y))
                        self.width = throwing_l.get_width()
                        self.height = throwing_l.get_height()

                    else:
                        win.blit(char_l, (self.x, self.y))
                        self.width = char_l.get_width()
                        self.height = char_l.get_height()
                else:
                    if self.up:
                        win.blit(up_standing, (self.x, self.y - self.height))
                        self.y -= 100
                        self.up = False
                    elif self.down:
                        win.blit(down_standing, (self.x, self.y))
                        self.y += 100
                        self.down = False
                    if self.throwing:
                        win.blit(throwing_r, (self.x, self.y))
                        self.width = throwing_r.get_width()
                        self.height = throwing_r.get_height()
                    else:
                        win.blit(char_r, (self.x, self.y))
                        self.width = char_r.get_width()
                        self.height = char_r.get_height()
            self.hitbox = (self.x, self.y, self.width, self.height)

        else:
            if self.u_count < 15:
                win.blit(jutsu, (self.x, self.y))
            if 8 <= self.u_count <= 17:
                if self.y == 220:
                    win.blit(smoke, (self.x, 317))
                    win.blit(smoke, (self.x, 417))
                elif self.y == 320:
                    win.blit(smoke, (self.x, 217))
                    win.blit(smoke, (self.x, 417))
                else:
                    win.blit(smoke, (self.x, 217))
                    win.blit(smoke, (self.x, 317))

            elif 17 < self.u_count <= 30:
                if self.u_count == 30:
                    self.weapons.add(Ultimate(self.x + self.width - 40,
                                              round(217 + self.height // 4)
                                              - 4, 1))
                    self.weapons.add(Ultimate(self.x + self.width - 40,
                                              round(317 + self.height // 4)
                                              - 4, 1))
                    self.weapons.add(Ultimate(self.x + self.width - 40,
                                              round(417 + self.height // 4)
                                              - 4, 1))

                win.blit(char_r, (self.x, 217))
                win.blit(char_r, (self.x, 317))
                win.blit(char_r, (self.x, 417))

            elif 30 < self.u_count <= 40:
                win.blit(throwing_r, (self.x, 217))
                win.blit(throwing_r, (self.x, 317))
                win.blit(throwing_r, (self.x, 417))

            elif self.u_count > 40:
                self.ult = False
            self.u_count += 1

        pygame.draw.rect(win, (0, 0, 0), (97, 16, 280, 40), 4)  # health border
        pygame.draw.rect(win, (255, 0, 0), (100, 19, 275, 35))  # red
        if self.curr_health > 0:
            pygame.draw.rect(win, (0, 255, 0), (100, 19, 275 -
                                                (275//self.max_health) *
                                                (self.max_health -
                                                 self.curr_health), 35))


class SandEnemy(Character):
    sand_enemy = [pygame.image.load('images/enemies/l_sand1.png'),
                  pygame.image.load('images/enemies/l_sand2.png'),
                  pygame.image.load('images/enemies/l_sand3.png'),
                  pygame.image.load('images/enemies/l_sand4.png'),
                  pygame.image.load('images/enemies/l_sand5.png'),
                  pygame.image.load('images/enemies/l_sand6.png'),
                  pygame.image.load('images/enemies/l_sand7.png')]

    def __init__(self, x, y, velocity):
        Character.__init__(self, x, y)
        self.velocity = velocity
        self.stop = False
        self.max_health = 3
        self.curr_health = self.max_health

    def draw(self, win):
        self.x -= self.velocity
        if self.walkCount + 1 >= 21:  # num of pics * 3
            self.walkCount = 0
        else:
            self.walkCount += 1

        win.blit(self.sand_enemy[self.walkCount//3], (self.x, self.y))
        self.width = self.sand_enemy[self.walkCount//3].get_width()
        self.height = self.sand_enemy[self.walkCount//3].get_height()
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, (255, 0, 0), (self.x - 5, self.y - 12, 84, 6))
        pygame.draw.rect(win, (0, 255, 0), (self.x - 5, self.y - 12,
                                            84 - (28 * (self.max_health -
                                                        self.curr_health)), 6))
        pygame.draw.rect(win, (0, 0, 0), (self.x - 6, self.y - 13, 86, 8), 1)


class Puppets(SandEnemy):
    puppets = [pygame.transform.flip(pygame.image.load(
        'images/enemies/puppet1.png'), True, False),
               pygame.transform.flip(pygame.image.load(
                   'images/enemies/puppet2.png'), True, False)]

    def __init__(self, x, y, velocity):
        SandEnemy.__init__(self, x, y, velocity)
        self.max_health = 5
        self.curr_health = self.max_health
        self.velocity = velocity

    def draw(self, win):
        if self.walkCount + 1 >= 80:  # num of pics * 3
            self.walkCount = 0
        else:
            self.walkCount += 1

        if self.walkCount <= 10:
            v = 0
            self.x -= self.velocity
        else:
            v = 1

        win.blit(self.puppets[v], (self.x, self.y))
        self.width = self.puppets[v].get_width()
        self.height = self.puppets[v].get_height()
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, (255, 0, 0), (self.x - 5, self.y - 12, 84, 6))
        pygame.draw.rect(win, (0, 255, 0), (self.x - 5, self.y - 12,
                                            84 - (84//self.max_health *
                                                  (self.max_health -
                                                   self.curr_health)), 6))
        pygame.draw.rect(win, (0, 0, 0), (self.x - 6, self.y - 13, 86, 8), 1)


class Archers(SandEnemy):
    archers = [pygame.image.load('images/enemies/archer1.png'),
               pygame.image.load('images/enemies/archer2.png'),
               pygame.image.load('images/enemies/archer3.png'),
               pygame.image.load('images/enemies/archer4.png'),
               pygame.image.load('images/enemies/archer5.png')]

    def __init__(self, x, y, line):
        SandEnemy.__init__(self, x, y, velocity=3)
        self.pauseCount = 0
        self.arrow_x = self.x + self.width
        self.line = line
        self.arrow_lst = []

    def draw(self, win):
        self.arrow_x += self.velocity * 3
        if self.walkCount + 1 >= 15:  # want to stop
            self.walkCount = 0
            self.pauseCount = 80
        elif self.walkCount + 1 < 15 and self.pauseCount > 0:
            self.pauseCount -= 1

        elif self.walkCount + 1 < 15:
            self.walkCount += 1

        if self.pauseCount == 0:
            if self.walkCount//3 == 4:
                if len(self.arrow_lst) == 0:
                    self.arrow_lst.append(EnemyWeapon(self.x + 20, self.y +
                                                      self.height//3 + 1, 1))

            self.width = self.archers[self.walkCount//6].get_width()
            self.height = self.archers[self.walkCount//6].get_height()
            win.blit(self.archers[self.walkCount//3], (self.x, self.line -
                                                       self.height))
            self.hitbox = (self.x, self.y, self.width, self.height)

        else:
            win.blit(self.archers[0], (self.x, self.line -
                                       self.archers[0].get_height()))

        pygame.draw.rect(win, (255, 0, 0), (self.x - 5, self.y - 5, 84, 6))
        pygame.draw.rect(win, (0, 255, 0), (self.x - 5, self.y - 5,
                                            84 - (28 * (self.max_health -
                                                        self.curr_health)), 6))
        pygame.draw.rect(win, (0, 0, 0), (self.x - 6, self.y - 6, 86, 8), 1)


class Weapon:
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.velocity = 10 * facing
        self.width = kunai_l.get_width()
        self.num = 0

    def draw(self, win):
        if self.facing == 1:
            win.blit(kunai_r, (self.x, self.y))
        else:
            win.blit(kunai_l, (self.x, self.y))


class Ultimate(Weapon):
    def __init__(self, x, y, facing):
        Weapon.__init__(self, x, y, facing)

    def draw(self, win):
        if self.facing == 1:
            win.blit(rasengan, (self.x, self.y))
        else:
            win.blit(rasengan, (self.x, self.y))


class EnemyWeapon(Weapon):
    def __init__(self, x, y, facing):
        Weapon.__init__(self, x, y, facing)

    def draw(self, win):
        win.blit(arrow, (self.x, self.y))
