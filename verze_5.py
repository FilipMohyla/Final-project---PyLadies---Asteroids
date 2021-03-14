import pyglet, math, random
from random import randrange
from math import sqrt, cos, sin, atan2
from pyglet import gl


batch = pyglet.graphics.Batch()
objects = []
bullets = []
window = pyglet.window.Window()

image = pyglet.image.load("ship2.png")
image.anchor_x = image.width // 2
image.anchor_y = image.height // 2

planet = pyglet.image.load("Green Gas Planet.png")
planet.anchor_x = planet.width // 2
planet.anchor_y = planet.height // 2
planet = pyglet.sprite.Sprite(planet, x=1000, y=560)

bullet_image = pyglet.image.load("laserRed10.png")
bullet_image.anchor_x = bullet_image.width // 2
bullet_image.anchor_y = bullet_image.height // 2

backgroud_image = pyglet.image.load("final_background.png")
backgroud_image.anchor_x = backgroud_image.width // 2
backgroud_image.anchor_y = backgroud_image.height // 2
backgroud_image = pyglet.sprite.Sprite(backgroud_image, x=window.width // 2, y=window.height // 2)

asteroid_image = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png',
                '9.png', '10.png', '11.png', '12.png', '13.png', '14.png', '15.png','16.png']
ROTATION_SPEED = 7
ACCELERATION = 400
BULLET_SPEED = 80

keys = pyglet.window.key.KeyStateHandler()


def chose_image(asteroid_image):
    ### Return random image for asteroid sprite from asteroid_image list ###
    load_asteroid_image = pyglet.image.load(random.choice(asteroid_image))
    load_asteroid_image.anchor_x = load_asteroid_image.width // 2
    load_asteroid_image.anchor_y = load_asteroid_image.height // 2

    return load_asteroid_image


class SpaceObject():
    def __init__(self, x, y, x_speed, y_speed, rotation, sprite):
        ### Defines atributes for every spaceobject in game ###
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation
        self.sprite = pyglet.sprite.Sprite(sprite, batch=batch)
        self.radius = self.sprite.width / 2

    def delete(self):
        ### Delete object from spaceships and objects list and sprite ###

        del spaceships[spaceships.index(self)]
        del objects[objects.index(self)]
        self.sprite.delete()


class Laser():
    def __init__(self):
        self.x = (spaceships[0]).x
        self.y = (spaceships[0]).y
        self.bullet_rotation = (spaceships[0]).rotation
        self.sprite = pyglet.sprite.Sprite(bullet_image, self.x, self.y, batch=batch)
        self.radius = self.sprite.width / 2

    def tick(self, dt):
        self.bullet_x_speed, self.bullet_y_speed = 0, 0
        self.bullet_x_speed += dt * BULLET_SPEED * math.cos(self.bullet_rotation)
        self.bullet_y_speed += dt * BULLET_SPEED * math.sin(self.bullet_rotation)

        self.x += + dt + self.bullet_x_speed * 15
        self.y += + dt + self.bullet_y_speed * 15

        self.sprite.bullet_rotation = 90 - math.degrees(self.bullet_rotation)
        self.sprite.x = self.x
        self.sprite.y = self.y

    def out_of_window(self):
        if self.x > window.width or self.x < 0 or self.y > window.height or self.y < 0:
            return True
        return False


class Spaceship(SpaceObject):
    def __init__(self, x, y, x_speed, y_speed, rotation, sprite):
        ### Just change source image for spaceship sprite ###
        
        self.sprite = pyglet.sprite.Sprite(image, batch=batch)
        super().__init__(x, y, x_speed, y_speed, rotation, sprite)

    def delete(self):
    ### Delete object from spaceships and objects list and sprite ###

        del spaceships[spaceships.index(self)]
        del objects[objects.index(self)]
        self.sprite.delete()

    def tick(self, dt):
        ### Defines handling of spaceship ###

        up = keys[pyglet.window.key.UP]
        left = keys[pyglet.window.key.LEFT]
        right = keys[pyglet.window.key.RIGHT]
        space = keys[pyglet.window.key.SPACE]

        self.y_speed += dt * ACCELERATION * math.sin(self.rotation)
        self.x_speed += dt * ACCELERATION * math.cos(self.rotation)

        if up:
            self.x = self.x + self.x_speed * dt
            self.y = self.y + self.y_speed * dt

        if not up:
            self.y_speed -= dt * ACCELERATION * math.sin(self.rotation)
            self.x_speed -= dt * ACCELERATION * math.cos(self.rotation)
            self.x = self.x + self.x_speed * dt
            self.y = self.y + self.y_speed * dt

        if left:
            self.rotation += + dt * ROTATION_SPEED

        if right:
            self.rotation -= + dt * ROTATION_SPEED

        if self.x > (window.width + 30):
            
            self.x = 0

        if self.x < -30:
            self.x = +(window.width + 28)

        if self.y > (window.height + 30):
            
            self.y = 0

        if self.y < -30:
            self.y = window.height + 30

        if space:

            bullets.append(Laser())

        self.sprite.rotation = 90 - math.degrees(self.rotation)
        self.sprite.x = self.x
        self.sprite.y = self.y

    def hit_by_asteroid(self):

        ### Call SpaceObject.delete method and then insert new spaceship into spaceships and objects lists ###

        try:
            self.delete()
            self.sprite.delete()
            
        except ValueError:
            
            if len(spaceships) == 0:
                spaceships.append(Spaceship(window.width // 2, window.height // 2, 0, 0, 0, image))
                objects.append(spaceships)


spaceships = [Spaceship(window.width // 2, window.height // 2, 0, 0, 0, image)]
objects.append(spaceships)


class Asteroid(SpaceObject):

    def tick(self, dt):
        ### Defines movement of asteroids ###
        self.rotation += 2
        self.x += + dt + self.x_speed
        self.y += + dt + self.y_speed

        if self.x <= -20 and self.y > 350:

            self.x += +1380
            self.y = randrange(20, 764)
            self.x_speed = randrange(-10, -5)
            self.y_speed = randrange(4, 15)

        if self.x <= -20 and self.y < 350:

            self.x = (window.width + 20)
            self.y = randrange(15, 764)
            self.x_speed = randrange(-10, -5)
            self.y_speed = randrange(-2, 2)

        if self.x >= 1395 and self.y >= 500:

            self.x -= +1379
            self.y = randrange(25, 700)
            self.x_speed = randrange(2, 5)
            self.y_speed = randrange(1, 3)

        if self.x >= 1395 and self.y < 500:
            self.y = -(window.height + 20)
            self.x = randrange(500, 1350)
            self.y_speed = randrange(-8, -2)
            self.x_speed = randrange(-10, -2)

        if self.y <= -40 and self.x > 550:

            self.y += 800
            self.x = randrange(25, 800)

        if self.y <= -42 and self.x <= 350:
            self.y += 800
            self.x = randrange(25, 800)
            self.x_speed = randrange(5, 15)
            self.y_speed = randrange(15, 25)

        if self.y >= 800 and self.x < 700:
            self.y -= 800
            self.x = randrange(5, 1350)
            self.y_speed = randrange(3, 5)
            self.x_speed = randrange(-9, -2)

        if self.y > 800 and self.x > 650:
            self.y = randrange(2, 750)
            self.x = 1380
            self.x_speed = randrange(-8, -2)
            self.y_speed = randrange(2, 4)

        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = self.rotation

    def hit_by_spaceship(self):

        ### Call SpaceObject.delete method and then insert new spaceship into spaceships and objects lists ###

        try:
            self.delete()
            self.sprite.delete()

        except ValueError:
            
            if len(spaceships) == 0:
                spaceships.append(Spaceship(window.width // 2, window.height // 2, 0, 0, 0, image))
                objects.append(spaceships)

    def hit_by_laser(self):
        try:
            del asteroids[asteroids.index(self)]
            self.sprite.delete()
        except ValueError:
            pass

asteroids = []

def distance(a, b, wrap_size):
    """Distance in one direction (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result


def overlaps(a, b):
    """Returns true iff two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared


def tick(dt):

    for index, laser in enumerate(bullets):
        laser.tick(dt)
        if laser.out_of_window():
            del bullets[index]
            del laser.sprite

    for spaceship in spaceships:
        spaceship.tick(dt)
        

    for asteroid in asteroids:
        objects.append(asteroid)
        asteroid.tick(dt)

        if overlaps(spaceship, asteroid) and isinstance(spaceship, Spaceship) and isinstance(asteroid, Asteroid):
            
            asteroid.hit_by_spaceship()
            spaceship.hit_by_asteroid()
            
        for index, bull in enumerate(bullets):
            if overlaps(bull, asteroid) and isinstance(bull, Laser):
                
                asteroid.hit_by_laser()

                del bullets[index]
                del bull.sprite
                break

    if not asteroids:
        for i in range(10):
            asteroids.append(Asteroid(0, 0, randrange(-20, 20), randrange(-20, 20), 2, chose_image(asteroid_image)))


pyglet.clock.schedule_interval(tick, 1/50)


def window_draw():
    window.clear()
    backgroud_image.draw()
    planet.draw()
    batch.draw()


window.push_handlers(
    keys,
    on_draw=window_draw)

pyglet.app.run()
