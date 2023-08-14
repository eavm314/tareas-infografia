import math
import arcade
import random
from app_objects import Tank, Enemy
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, SPEED, ANGULAR_SPEED

def get_random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


class App(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.game_over = False
        self.rot_speed = 0.5
        self.speed = 10
        self.tank1 = Tank(100, 300, 5, get_random_color())
        self.tank2 = Tank(700, 300, 5, get_random_color())
        self.tank2.theta = math.pi
        for part in self.tank2.body:
            part.rotate(math.pi, pivot=(self.tank2.x, self.tank2.y))
        self.enemies = [Enemy(random.randint(100, 700),
                            random.randint(100, 500),
                            30, get_random_color())
                            for i in range(20)]

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.SPACE:
                self.tank1.shoot(20)

            case arcade.key.W:
                self.tank1.speed = SPEED
            case arcade.key.S:
                self.tank1.speed = -SPEED
            case arcade.key.A:
                self.tank1.angular_speed = ANGULAR_SPEED
            case arcade.key.D:
                self.tank1.angular_speed = -ANGULAR_SPEED

            case arcade.key.ENTER:
                self.tank2.shoot(20)

            case arcade.key.UP:
                self.tank2.speed = SPEED
            case arcade.key.DOWN:
                self.tank2.speed = -SPEED
            case arcade.key.LEFT:
                self.tank2.angular_speed = ANGULAR_SPEED
            case arcade.key.RIGHT:
                self.tank2.angular_speed = -ANGULAR_SPEED
                            
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.W, arcade.key.S):
            self.tank1.speed = 0

        if symbol in (arcade.key.A, arcade.key.D):
            self.tank1.angular_speed = 0

        if symbol in (arcade.key.UP, arcade.key.DOWN):
            self.tank2.speed = 0

        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.tank2.angular_speed = 0

    def on_update(self, delta_time: float):
        if self.game_over:
            return

        self.tank1.update(delta_time, self.enemies, self.tank2)
        self.tank2.update(delta_time, self.enemies, self.tank1)
        if self.tank1.life <= 0 or self.tank2.life <= 0:
            self.game_over = True
        
    def on_draw(self):
        if self.game_over:
            self.clear()
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT*.75,
                             font_size=50, anchor_x="center")
            arcade.draw_text(f"Player 1: {self.tank1.score}", 100, SCREEN_HEIGHT/2, font_size=30)
            arcade.draw_text(f"Player 2: {self.tank2.score}", SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2, font_size=30)

            arcade.draw_text("Winner: " + ("Player 1" if self.tank1.score > self.tank2.score else "Player 2"), SCREEN_WIDTH/2, SCREEN_HEIGHT/3, font_size=30, anchor_x="center")

            return
        
        self.clear()
         # Dibujar el puntaje y la vida en las esquinas superiores
        arcade.draw_text("Player 1", 10, SCREEN_HEIGHT - 20)
        arcade.draw_text(f"Score: {self.tank1.score}", 10, SCREEN_HEIGHT - 40)
        arcade.draw_text(f"Life: {self.tank1.life}", 10, SCREEN_HEIGHT - 60)

        arcade.draw_text("Player 2", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 20)
        arcade.draw_text(f"Score: {self.tank2.score}", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40)
        arcade.draw_text(f"Life: {self.tank2.life}", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 60)

        for e in self.enemies:
            e.draw()

        self.tank1.draw()
        self.tank2.draw()
    
if __name__ == "__main__":
    app = App()
    arcade.run()