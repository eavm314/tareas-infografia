import random
import numpy as np
import arcade
import math
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Polygon2D:
    def __init__(self, vertices, color, rot_speed=1):
        self.vertices = vertices
        self.color = color
        self.rot_speed = rot_speed


    def translate(self, dx, dy):
        TM = np.array([
            [1, 0, dx], 
            [0, 1, dy], 
            [0, 0, 1]
        ])

        return self.apply_transform(TM)
    
    def rotate(self, dt, pivot=None):
        xc, yc = pivot if pivot is not None else self.get_center()

        theta = self.rot_speed * dt

        Mt1 = np.array([
            [1, 0, -xc], 
            [0, 1, -yc], 
            [0, 0, 1]
        ])
        Mr = np.array([
            [np.cos(theta), -np.sin(theta), 0], 
            [np.sin(theta), np.cos(theta), 0], 
            [0, 0, 1]
        ])
        Mt2 = np.array([
            [1, 0, xc], 
            [0, 1, yc], 
            [0, 0, 1]
        ])

        TM = np.dot(Mt2, np.dot(Mr, Mt1))
  
        return self.apply_transform(TM)

    def scale(self, sx, sy, pivot=None):
        xc, yc = pivot if pivot is not None else self.get_center()
        Mt1 = np.array([
            [1, 0, -xc], 
            [0, 1, -yc], 
            [0, 0, 1]
        ])
        Ms = np.array([
            [sx, 0, 0], 
            [0, sy, 0], 
            [0, 0, 1]
        ])
        Mt2 = np.array([
            [1, 0, xc], 
            [0, 1, yc], 
            [0, 0, 1]
        ])

        TM = np.dot(Mt2, np.dot(Ms, Mt1))
  
        return self.apply_transform(TM)

    def apply_transform(self, tr_matrix):
        v_array = np.transpose(np.array(
            [[v[0], v[1], 1] for v in self.vertices]
        ))

        self.vertices = np.transpose(
            np.dot(tr_matrix, v_array)[0:2, :]
        ).tolist()

    def get_center(self):
        return np.mean(np.array(self.vertices), axis=0)

    def draw(self):
        arcade.draw_polygon_outline(self.vertices, self.color, 5)

class Character:
    def __init__(self, x, y, life, size) -> None:
        self.x = x
        self.y = y
        self.life = life
        self.size = size

class Enemy(Character):
    def __init__(self, x, y, size, color) -> None:
        super().__init__(x,y,5, size)
        self.color = color 

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)


class Tank(Character):
    def __init__(self, x, y, size, color) -> None:
        super().__init__(x,y,100, size)
        self.size = size
        self.speed = 0
        self.angular_speed = 0
        self.theta = 0
        self.score = 0
        self.body = [
            Polygon2D([(x+10*size, y), (x, y+5*size), (x, y-5*size)], color),
            Polygon2D([(x-size, y+4*size), (x-size, y+6*size), (x+8*size, y+6*size), (x+8*size, y+4*size)], color),
            Polygon2D([(x-size, y-4*size), (x-size, y-6*size), (x+8*size, y-6*size), (x+8*size, y-4*size)], color),
            ]
        self.bullets = []
    
    def shoot(self, bullet_speed):
        self.bullets.append((self.x, self.y, self.theta, bullet_speed))

    def update(self, delta_time: float, enemies, e_tank):
        dtheta = self.angular_speed * delta_time
        dx = self.speed * math.cos(self.theta)
        dy = self.speed * math.sin(self.theta)
        self.theta += dtheta
        self.x += dx
        self.y += dy

        # transformar cada parte del body
        for part in self.body:
            part.translate(dx, dy)
            part.rotate(dtheta, pivot=(self.x, self.y))
        self.update_bullets(delta_time, enemies, e_tank)

    def update_bullets(self, delta_time, enemies, e_tank):
        for i, (x, y, theta, speed) in enumerate(self.bullets):
            new_x = x + speed * math.cos(theta)
            new_y = y + speed * math.sin(theta)
            self.bullets[i] = (new_x, new_y, theta, speed)
            self.check_enemies(i, new_x, new_y, enemies, e_tank)

            if new_x < 0 or new_x > SCREEN_WIDTH or new_y < 0 or new_y > SCREEN_HEIGHT:
                self.bullets.pop(i)

    def check_enemies(self, i, x_b,y_b, enemies: list[Enemy], e_tank: Character):
        if arcade.get_distance(e_tank.x,e_tank.y,x_b,y_b) < e_tank.size*7:
            e_tank.life -= 10
            self.bullets.pop(i)
            self.score += 50
            return

        for e in enemies:
            if arcade.get_distance(e.x,e.y,x_b,y_b) < e.size:
                enemies.remove(e)
                self.bullets.pop(i)
                self.score += 10
                break
        

    def draw(self):
        for part in self.body:
            part.draw()

        arcade.draw_point(self.x, self.y, arcade.color.RED, 4)

        for bx, by, theta, speed in self.bullets:
            arcade.draw_point(bx, by, arcade.color.YELLOW, 7)