# imports
import arcade
import pathlib
from random import randint
import random
import math
# networked multiplayer game
import Player
import asyncio
import socket
import Server
import threading


# main class that sets the initial maps, lists, sprites, variables, and sounds
class ShaneHartProject3(arcade.Window):
    def __init__(self, server_add, client_add):  # def __init__(self):
        super().__init__(960, 960)
        # the three multilayer tiles maps
        self.mapOne = None
        self.mapOne_wall_list = None
        self.currentMap = None
        self.mapTwo = None
        self.mapTwo_wall_list = None
        self.mapThree = None
        self.mapThree_wall_list = None
        self.mapLoss = None
        self.mapLoss_wall_list = None
        self.mapWon = None
        self.mapWon_wall_list = None
        self.player = None
        self.player_list = None
        # first type of enemy that can 'shoot'
        self.shootingEnemy = None
        self.shootingEnemy_list = None
        # second type of enemy(s)
        self.walkingEnemy = None
        self.walkingEnemy_list = None
        self.jumpingEnemy = None
        self.jumpingEnemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        # eight unique sounds
        self.bullet_sound = None
        self.player_hit_sound = None
        self.bullet_hit_sound = None
        self.enemy_hit_sound = None
        self.next_map_sound = None
        self.player_lose_sound = None
        self.player_win_sound = None
        self.bullet_collision_sound = None
        # sets the score at 0
        self.score = 0
        self.direction = 0
        self.enemy = None
        # starts the player out with three lives
        self.lives = 3
        self.frames = 0
        self.player_bullet = None
        self.enemy_bullet = None
        # networked multiplayer game
        self.ip_address = client_add
        self.server_address = server_add
        self.from_server = ""

    # sets up the different lists, maps, animated sprites, sounds, and the first maps enemies to be used in the game
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.shootingEnemy_list = arcade.SpriteList()
        self.walkingEnemy_list = arcade.SpriteList()
        self.jumpingEnemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        # each map gets more complicated as the game progresses
        map1 = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / 'Assets' / 'Maps' / 'Map 1.json')
        self.mapOne = arcade.Scene.from_tilemap(map1)
        # "Walls" can be interacted with
        self.mapOne_wall_list = map1.sprite_lists["Walls"]
        self.currentMap = self.mapOne
        map2 = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / 'Assets' / 'Maps' / 'Map 2.json')
        self.mapTwo = arcade.Scene.from_tilemap(map2)
        self.mapTwo_wall_list = map2.sprite_lists["Walls"]
        map3 = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / 'Assets' / 'Maps' / 'Map 3.json')
        self.mapThree = arcade.Scene.from_tilemap(map3)
        self.mapThree_wall_list = map3.sprite_lists["Walls"]
        lose = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / 'Assets' / 'Maps' / 'Lose Screen.json')
        self.mapLoss = arcade.Scene.from_tilemap(lose)
        self.mapLoss_wall_list = lose.sprite_lists["Walls"]
        win = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / 'Assets' / 'Maps' / 'Win Screen.json')
        self.mapWon = arcade.Scene.from_tilemap(win)
        self.mapWon_wall_list = win.sprite_lists["Walls"]
        # AnimatedTimeBased player sprite (one is used)
        self.player = arcade.AnimatedTimeBasedSprite(None, 0.5, center_x=100, center_y=480)
        player_count = 0
        # first unique appearance
        player = pathlib.Path.cwd() / 'Assets' / 'Sprites' / 'Player'
        player_files = player.glob('*.png')
        player_textures = []
        for player_path in player_files:
            player_count += 1
            if player_count == 1:
                self.player.texture = arcade.load_texture(str(player_path))
            player_frame = arcade.AnimationKeyframe(player_count, 100, arcade.load_texture(str(player_path)))
            player_textures.append(player_frame)
        self.player.frames = player_textures
        self.player_list.append(self.player)
        # AnimatedTimeBased player sprite (three are used)
        self.shootingEnemy = arcade.AnimatedTimeBasedSprite(None, 0.5)
        shooting_count = 0
        # second unique appearance
        shooting = pathlib.Path.cwd() / 'Assets' / 'Sprites' / 'Shooting Enemy'
        shooting_files = shooting.glob('*.png')
        shooting_textures = []
        for shooting_path in shooting_files:
            shooting_count += 1
            if shooting_count == 1:
                self.shootingEnemy.texture = arcade.load_texture(str(shooting_path))
            shooting_frame = arcade.AnimationKeyframe(shooting_count, 100, arcade.load_texture(str(shooting_path)))
            shooting_textures.append(shooting_frame)
        self.shootingEnemy.frames = shooting_textures
        self.shootingEnemy_list.append(self.shootingEnemy)
        # AnimatedTimeBased player sprite (three are used)
        self.walkingEnemy = arcade.AnimatedTimeBasedSprite(None, 0.5)
        walking_count = 0
        # third unique appearance
        walking = pathlib.Path.cwd() / 'Assets' / 'Sprites' / 'Walking Enemy'
        walking_files = walking.glob('*.png')
        walking_textures = []
        for walking_path in walking_files:
            walking_count += 1
            if walking_count == 1:
                self.walkingEnemy.texture = arcade.load_texture(str(walking_path))
            walking_frame = arcade.AnimationKeyframe(walking_count, 100, arcade.load_texture(str(walking_path)))
            walking_textures.append(walking_frame)
        self.walkingEnemy.frames = walking_textures
        self.walkingEnemy_list.append(self.walkingEnemy)
        # AnimatedTimeBased player sprite (three are used)
        self.jumpingEnemy = arcade.AnimatedTimeBasedSprite(None, 0.5)
        jumping_count = 0
        # fourth unique appearance
        jumping = pathlib.Path.cwd() / 'Assets' / 'Sprites' / 'Jumping Enemy'
        jumping_files = jumping.glob('*.png')
        jumping_textures = []
        for jumping_path in jumping_files:
            jumping_count += 1
            if jumping_count == 1:
                self.jumpingEnemy.texture = arcade.load_texture(str(jumping_path))
            jumping_frame = arcade.AnimationKeyframe(jumping_count, 150, arcade.load_texture(str(jumping_path)))
            jumping_textures.append(jumping_frame)
        self.jumpingEnemy.frames = jumping_textures
        self.jumpingEnemy_list.append(self.jumpingEnemy)
        self.bullet_sound = arcade.sound.load_sound(":resources:sounds/hurt5.wav")
        self.player_hit_sound = arcade.sound.load_sound(":resources:sounds/hit3.wav")
        self.bullet_hit_sound = arcade.sound.load_sound(":resources:sounds/hit4.wav")
        self.enemy_hit_sound = arcade.sound.load_sound(":resources:sounds/hurt4.wav")
        self.next_map_sound = arcade.sound.load_sound(":resources:sounds/rockHit2.ogg")
        self.player_lose_sound = arcade.sound.load_sound(":resources:sounds/gameover4.wav")
        self.player_win_sound = arcade.sound.load_sound(":resources:sounds/secret4.wav")
        self.bullet_collision_sound = arcade.sound.load_sound(":resources:sounds/explosion1.wav")
        # enemies can be interacted with (nine of them in between all three maps)
        self.map_one_enemies()
        # networked multiplayer game
        self.from_server = ""

    # draws the first map, different sprites in their lists, and scoreboard in order from back to front
    def on_draw(self):
        arcade.start_render()
        # starts the player out on map one
        self.currentMap.draw()
        # starts the player and randomly placed enemies out on map one
        self.player_bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.player_list.draw()
        self.shootingEnemy_list.draw()
        self.walkingEnemy_list.draw()
        self.jumpingEnemy_list.draw()
        # displays the score at all times
        score = f"Score: {self.score}"
        arcade.draw_text(score, start_x=350, start_y=10, color=arcade.csscolor.BLACK, font_size=40)

    # creates keys to press for the user to use while playing the game (needed keyboard input)
    def on_key_press(self, key, modifiers):
        # when the W key is pressed the player will move up the screen (two directions)
        if key == arcade.key.W:
            self.player.change_y = 3
            # sets the players direction for their shot
            self.direction = 1
            # chooses a random enemy to move each time the player takes a step
            self.enemy = randint(1, 3)
            # having the enemies move toward the player keeps them on the map
            self.enemy_movement()
        # when the S key is pressed the player will move down the screen (two directions)
        elif key == arcade.key.S:
            self.player.change_y = -3
            self.direction = 2
            self.enemy = randint(1, 3)
            self.enemy_movement()
        # when the A key is pressed the player will move left of the screen (two directions)
        elif key == arcade.key.A:
            self.player.change_x = -3
            self.direction = 3
            self.enemy = randint(1, 3)
            self.enemy_movement()
        # when the S key is pressed the player will move right of the screen (two directions)
        elif key == arcade.key.D:
            self.player.change_x = 3
            self.direction = 4
            self.enemy = randint(1, 3)
            self.enemy_movement()
        # when the E key is pressed the player will 'shoot' a bullet across the screen
        elif key == arcade.key.E and self.player_bullet not in self.player_bullet_list:
            # will play a sound when the players bullet is 'shot' across the screen
            arcade.play_sound(self.bullet_sound)
            self.player_bullet = arcade.Sprite(":resources:images/space_shooter/meteorGrey_tiny2.png")
            self.player_bullet.center_x = self.player.center_x
            self.player_bullet.center_y = self.player.center_y
            # will shoot in the direction the player was last moving
            if self.direction == 0:
                self.player_bullet.change_x = 5
            if self.direction == 1:
                self.player_bullet.change_y = 5
            if self.direction == 2:
                self.player_bullet.change_y = -5
            if self.direction == 3:
                self.player_bullet.change_x = -5
            if self.direction == 4:
                self.player_bullet.change_x = 5
            self.player_bullet_list.append(self.player_bullet)

    # creates keys to release for the user to use while playing the game (needed keyboard input)
    def on_key_release(self, key, modifiers):
        # when the W key or the S key is released the player will stop moving up or down the screen
        if key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0
            # stops the enemy from moving
            self.enemy_stop()
        # when the A key or the D key is released the player will stop moving left or right of the screen
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0
            self.enemy_stop()

    # spawns the enemies on map one randomly
    def map_one_enemies(self):
        for i in range(1):
            shooting_enemy_spawned = False
            while not shooting_enemy_spawned:
                self.shootingEnemy.center_x = random.randrange(900)
                self.shootingEnemy.center_y = random.randrange(900)
                wall_hit_shooting_enemy = arcade.check_for_collision_with_list(self.shootingEnemy,
                                                                               self.mapOne_wall_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.shootingEnemy_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.shootingEnemy_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.shootingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.shootingEnemy_list)
                if len(wall_hit_shooting_enemy) == 0 and len(shooting_enemy_hit) == 0 and len(walking_enemy_hit) == 0 \
                        and len(jumping_enemy_hit) == 0 and len(player_hit) == 0:
                    shooting_enemy_spawned = True
            if self.shootingEnemy not in self.shootingEnemy_list:
                self.shootingEnemy_list.append(self.shootingEnemy)
        for j in range(1):
            walking_enemy_spawned = False
            while not walking_enemy_spawned:
                self.walkingEnemy.center_x = random.randrange(900)
                self.walkingEnemy.center_y = random.randrange(900)
                wall_hit_walking_enemy = arcade.check_for_collision_with_list(self.walkingEnemy, self.mapOne_wall_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.walkingEnemy_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.walkingEnemy_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.walkingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.walkingEnemy_list)
                if len(wall_hit_walking_enemy) == 0 and len(walking_enemy_hit) == 0 and len(shooting_enemy_hit) == 0 \
                        and len(jumping_enemy_hit) == 0 and len(player_hit) == 0:
                    walking_enemy_spawned = True
            if self.walkingEnemy not in self.walkingEnemy_list:
                self.walkingEnemy_list.append(self.walkingEnemy)
        for k in range(1):
            jumping_enemy_spawned = False
            while not jumping_enemy_spawned:
                self.jumpingEnemy.center_x = random.randrange(900)
                self.jumpingEnemy.center_y = random.randrange(900)
                wall_hit_jumping_enemy = arcade.check_for_collision_with_list(self.jumpingEnemy, self.mapOne_wall_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.jumpingEnemy_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.jumpingEnemy_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.jumpingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.jumpingEnemy_list)
                if len(wall_hit_jumping_enemy) == 0 and len(jumping_enemy_hit) == 0 and len(shooting_enemy_hit) == 0 \
                        and len(walking_enemy_hit) == 0 and len(player_hit) == 0:
                    jumping_enemy_spawned = True
            if self.jumpingEnemy not in self.jumpingEnemy_list:
                self.jumpingEnemy_list.append(self.jumpingEnemy)

    # spawns the enemies on map two randomly (spawns more enemies than map one)
    def map_two_enemies(self):
        for i in range(3):  # broken
            shooting_enemy_spawned = False
            while not shooting_enemy_spawned:
                self.shootingEnemy.center_x = random.randrange(900)
                self.shootingEnemy.center_y = random.randrange(900)
                wall_hit_shooting_enemy = arcade.check_for_collision_with_list(self.shootingEnemy,
                                                                               self.mapTwo_wall_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.shootingEnemy_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.shootingEnemy_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.shootingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.shootingEnemy_list)
                if len(wall_hit_shooting_enemy) == 0 and len(shooting_enemy_hit) == 0 and len(walking_enemy_hit) == 0 \
                        and len(jumping_enemy_hit) == 0 and len(player_hit) == 0:
                    shooting_enemy_spawned = True
            if self.shootingEnemy not in self.shootingEnemy_list:
                self.shootingEnemy_list.append(self.shootingEnemy)
        for j in range(3):  # broken
            walking_enemy_spawned = False
            while not walking_enemy_spawned:
                self.walkingEnemy.center_x = random.randrange(900)
                self.walkingEnemy.center_y = random.randrange(900)
                wall_hit_walking_enemy = arcade.check_for_collision_with_list(self.walkingEnemy, self.mapTwo_wall_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.walkingEnemy_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.walkingEnemy_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.walkingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.walkingEnemy_list)
                if len(wall_hit_walking_enemy) == 0 and len(walking_enemy_hit) == 0 and len(shooting_enemy_hit) == 0 \
                        and len(jumping_enemy_hit) == 0 and len(player_hit) == 0:
                    walking_enemy_spawned = True
            if self.walkingEnemy not in self.walkingEnemy_list:
                self.walkingEnemy_list.append(self.walkingEnemy)
        for k in range(3):  # broken
            jumping_enemy_spawned = False
            while not jumping_enemy_spawned:
                self.jumpingEnemy.center_x = random.randrange(900)
                self.jumpingEnemy.center_y = random.randrange(900)
                wall_hit_jumping_enemy = arcade.check_for_collision_with_list(self.jumpingEnemy, self.mapTwo_wall_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.jumpingEnemy_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.jumpingEnemy_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.jumpingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.jumpingEnemy_list)
                if len(wall_hit_jumping_enemy) == 0 and len(jumping_enemy_hit) == 0 and len(shooting_enemy_hit) == 0 \
                        and len(walking_enemy_hit) == 0 and len(player_hit) == 0:
                    jumping_enemy_spawned = True
            if self.jumpingEnemy not in self.jumpingEnemy_list:
                self.jumpingEnemy_list.append(self.jumpingEnemy)

    # spawns the enemies on map three randomly (spawns more enemies than map two)
    def map_three_enemies(self):
        for i in range(5):  # broken
            shooting_enemy_spawned = False
            while not shooting_enemy_spawned:
                self.shootingEnemy.center_x = random.randrange(900)
                self.shootingEnemy.center_y = random.randrange(900)
                wall_hit_shooting_enemy = arcade.check_for_collision_with_list(self.shootingEnemy,
                                                                               self.mapThree_wall_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.shootingEnemy_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.shootingEnemy_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.shootingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.shootingEnemy_list)
                if len(wall_hit_shooting_enemy) == 0 and len(shooting_enemy_hit) == 0 and len(walking_enemy_hit) == 0 \
                        and len(jumping_enemy_hit) == 0 and len(player_hit) == 0:
                    shooting_enemy_spawned = True
            if self.shootingEnemy not in self.shootingEnemy_list:
                self.shootingEnemy_list.append(self.shootingEnemy)
        for j in range(5):  # broken
            walking_enemy_spawned = False
            while not walking_enemy_spawned:
                self.walkingEnemy.center_x = random.randrange(900)
                self.walkingEnemy.center_y = random.randrange(900)
                wall_hit_walking_enemy = arcade.check_for_collision_with_list(self.walkingEnemy,
                                                                              self.mapThree_wall_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.walkingEnemy_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.walkingEnemy_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.walkingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.walkingEnemy_list)
                if len(wall_hit_walking_enemy) == 0 and len(walking_enemy_hit) == 0 and len(shooting_enemy_hit) == 0 \
                        and len(jumping_enemy_hit) == 0 and len(player_hit) == 0:
                    walking_enemy_spawned = True
            if self.walkingEnemy not in self.walkingEnemy_list:
                self.walkingEnemy_list.append(self.walkingEnemy)
        for k in range(5):  # broken
            jumping_enemy_spawned = False
            while not jumping_enemy_spawned:
                self.jumpingEnemy.center_x = random.randrange(900)
                self.jumpingEnemy.center_y = random.randrange(900)
                wall_hit_jumping_enemy = arcade.check_for_collision_with_list(self.jumpingEnemy,
                                                                              self.mapThree_wall_list)
                jumping_enemy_hit = arcade.check_for_collision_with_list(self.jumpingEnemy, self.jumpingEnemy_list)
                shooting_enemy_hit = arcade.check_for_collision_with_list(self.shootingEnemy, self.jumpingEnemy_list)
                walking_enemy_hit = arcade.check_for_collision_with_list(self.walkingEnemy, self.jumpingEnemy_list)
                player_hit = arcade.check_for_collision_with_list(self.player, self.jumpingEnemy_list)
                if len(wall_hit_jumping_enemy) == 0 and len(jumping_enemy_hit) == 0 and len(shooting_enemy_hit) == 0 \
                        and len(walking_enemy_hit) == 0 and len(player_hit) == 0:
                    jumping_enemy_spawned = True
            if self.jumpingEnemy not in self.jumpingEnemy_list:
                self.jumpingEnemy_list.append(self.jumpingEnemy)

    # if the player touches any walls the player will lose a life
    def player_collision(self):
        if self.currentMap == self.mapOne:
            if arcade.check_for_collision_with_list(sprite=self.player, sprite_list=self.mapOne_wall_list):
                # will play a sound when the player runs into a wall
                arcade.play_sound(self.player_hit_sound)
                self.lives = self.lives - 1
                # will reset the player in a relatively save location
                self.player.center_x = 100
                self.player.center_y = 480
            # keeps the player on map one until all the enemies are 'shot'
            if self.player.center_x > 945 and self.shootingEnemy in self.shootingEnemy_list:
                self.player.center_x = 945
            if self.player.center_x > 945 and self.walkingEnemy in self.walkingEnemy_list:
                self.player.center_x = 945
            if self.player.center_x > 945 and self.jumpingEnemy in self.jumpingEnemy_list:
                self.player.center_x = 945
        if self.currentMap == self.mapTwo:
            if arcade.check_for_collision_with_list(sprite=self.player, sprite_list=self.mapTwo_wall_list):
                arcade.play_sound(self.player_hit_sound)
                self.lives = self.lives - 1
                self.player.center_x = 100
                self.player.center_y = 480
            # keeps the player on map two until all the enemies are 'shot'
            if self.player.center_x < 15:
                self.player.center_x = 15
            if self.player.center_x > 945 and self.shootingEnemy in self.shootingEnemy_list:
                self.player.center_x = 945
            if self.player.center_x > 945 and self.walkingEnemy in self.walkingEnemy_list:
                self.player.center_x = 945
            if self.player.center_x > 945 and self.jumpingEnemy in self.jumpingEnemy_list:
                self.player.center_x = 945
        if self.currentMap == self.mapThree:
            if arcade.check_for_collision_with_list(sprite=self.player, sprite_list=self.mapThree_wall_list):
                arcade.play_sound(self.player_hit_sound)
                self.lives = self.lives - 1
                self.player.center_x = 100
                self.player.center_y = 480
            # keeps the player on map three
            if self.player.center_x < 15:
                self.player.center_x = 15
        # if the player touches a wall they will randomly spawn somewhere on the map
        if self.currentMap == self.mapLoss:
            if arcade.check_for_collision_with_list(sprite=self.player, sprite_list=self.mapLoss_wall_list):
                arcade.play_sound(self.player_hit_sound)
                self.player.center_x = random.randrange(900)
                self.player.center_y = random.randrange(900)
        if self.currentMap == self.mapWon:
            if arcade.check_for_collision_with_list(sprite=self.player, sprite_list=self.mapWon_wall_list):
                arcade.play_sound(self.player_hit_sound)
                self.player.center_x = random.randrange(900)
                self.player.center_y = random.randrange(900)

    # if the player touches an enemy or is 'shot' by the enemy, the player will lose a life
    def player_hit(self):
        if arcade.check_for_collision_with_list(sprite_list=self.shootingEnemy_list, sprite=self.player):
            # will play a sound when the player runs into an enemy
            arcade.play_sound(self.player_hit_sound)
            self.lives = self.lives - 1
            self.player.center_x = 100
            self.player.center_y = 480
        if arcade.check_for_collision_with_list(sprite_list=self.walkingEnemy_list, sprite=self.player):
            arcade.play_sound(self.player_hit_sound)
            self.lives = self.lives - 1
            self.player.center_x = 100
            self.player.center_y = 480
        if arcade.check_for_collision_with_list(sprite_list=self.jumpingEnemy_list, sprite=self.player):
            arcade.play_sound(self.player_hit_sound)
            self.lives = self.lives - 1
            self.player.center_x = 100
            self.player.center_y = 480
        if arcade.check_for_collision_with_list(sprite_list=self.enemy_bullet_list, sprite=self.player):
            arcade.play_sound(self.player_hit_sound)
            self.lives = self.lives - 1
            self.enemy_bullet.remove_from_sprite_lists()
            self.player.center_x = 100
            self.player.center_y = 480

    # walls will block and delete the players shot
    def bullet_collision(self):
        if self.player_bullet in self.player_bullet_list:
            if self.currentMap == self.mapOne:
                if arcade.check_for_collision_with_list(sprite_list=self.mapOne_wall_list, sprite=self.player_bullet):
                    # will play a sound when the players 'shot' hits a wall
                    arcade.play_sound(self.bullet_hit_sound)
                    self.player_bullet.remove_from_sprite_lists()
                if self.player_bullet.center_x > 960:
                    self.player_bullet.remove_from_sprite_lists()
            if self.currentMap == self.mapTwo:
                if arcade.check_for_collision_with_list(sprite_list=self.mapTwo_wall_list, sprite=self.player_bullet):
                    arcade.play_sound(self.bullet_hit_sound)
                    self.player_bullet.remove_from_sprite_lists()
                if self.player_bullet.center_x < 0:
                    self.player_bullet.remove_from_sprite_lists()
                if self.player_bullet.center_x > 960:
                    self.player_bullet.remove_from_sprite_lists()
            if self.currentMap == self.mapThree:
                if arcade.check_for_collision_with_list(sprite_list=self.mapThree_wall_list, sprite=self.player_bullet):
                    arcade.play_sound(self.bullet_hit_sound)
                    self.player_bullet.remove_from_sprite_lists()
                if self.player_bullet.center_x < 0:
                    self.player_bullet.remove_from_sprite_lists()
            if self.currentMap == self.mapLoss:
                if arcade.check_for_collision_with_list(sprite_list=self.mapLoss_wall_list, sprite=self.player_bullet):
                    arcade.play_sound(self.bullet_hit_sound)
                    self.player_bullet.remove_from_sprite_lists()
            if self.currentMap == self.mapWon:
                if arcade.check_for_collision_with_list(sprite_list=self.mapWon_wall_list, sprite=self.player_bullet):
                    arcade.play_sound(self.bullet_hit_sound)
                    self.player_bullet.remove_from_sprite_lists()
        if self.enemy_bullet in self.enemy_bullet_list:
            if self.currentMap == self.mapOne:
                if arcade.check_for_collision_with_list(sprite_list=self.mapOne_wall_list, sprite=self.enemy_bullet):
                    # will play a sound when the enemies 'shot' hits a wall
                    arcade.play_sound(self.bullet_hit_sound)
                    self.enemy_bullet.remove_from_sprite_lists()
                if self.enemy_bullet.center_x > 960:
                    self.enemy_bullet.remove_from_sprite_lists()
            if self.currentMap == self.mapTwo:
                if arcade.check_for_collision_with_list(sprite_list=self.mapTwo_wall_list, sprite=self.enemy_bullet):
                    arcade.play_sound(self.bullet_hit_sound)
                    self.enemy_bullet.remove_from_sprite_lists()
                if self.enemy_bullet.center_x < 0:
                    self.enemy_bullet.remove_from_sprite_lists()
                if self.enemy_bullet.center_x > 960:
                    self.enemy_bullet.remove_from_sprite_lists()
            if self.currentMap == self.mapThree:
                if arcade.check_for_collision_with_list(sprite_list=self.mapThree_wall_list, sprite=self.enemy_bullet):
                    arcade.play_sound(self.bullet_hit_sound)
                    self.enemy_bullet.remove_from_sprite_lists()
                if self.enemy_bullet.center_x < 0:
                    self.enemy_bullet.remove_from_sprite_lists()

    # the shootingEnemy's 'shot'
    def enemy_shot(self):
        self.frames += 1
        for self.shootingEnemy in self.shootingEnemy_list:
            if self.frames % 240 == 0 and self.enemy_bullet not in self.enemy_bullet_list:
                # will play a sound when the enemies bullet is 'shot' across the screen
                arcade.play_sound(self.bullet_sound)
                self.enemy_bullet = arcade.Sprite(":resources:images/space_shooter/meteorGrey_tiny2.png")
                # the enemy will 'shoot' at the player regardless of obstacles
                self.enemy_bullet.center_x = self.shootingEnemy.center_x
                self.enemy_bullet.center_y = self.shootingEnemy.center_y
                self.enemy_bullet.change_x = math.cos(math.atan2((self.player.center_y - self.shootingEnemy.center_y),
                                                                 (self.player.center_x
                                                                  - self.shootingEnemy.center_x))) * 5
                self.enemy_bullet.change_y = math.sin(math.atan2((self.player.center_y - self.shootingEnemy.center_y),
                                                                 (self.player.center_x
                                                                  - self.shootingEnemy.center_x))) * 5

    # increases the score each time an enemy is 'shot' and removes the 'shot' enemy
    def enemy_hit(self):
        if self.shootingEnemy in self.shootingEnemy_list:
            if arcade.check_for_collision_with_list(sprite_list=self.player_bullet_list, sprite=self.shootingEnemy):
                # will play a sound when an enemy is 'shot'
                arcade.play_sound(self.enemy_hit_sound)
                self.score = self.score + 150
                self.player_bullet.remove_from_sprite_lists()
                self.shootingEnemy.remove_from_sprite_lists()
        if self.walkingEnemy in self.walkingEnemy_list:
            if arcade.check_for_collision_with_list(sprite_list=self.player_bullet_list, sprite=self.walkingEnemy):
                arcade.play_sound(self.enemy_hit_sound)
                self.score = self.score + 50
                self.player_bullet.remove_from_sprite_lists()
                self.walkingEnemy.remove_from_sprite_lists()
        if self.jumpingEnemy in self.jumpingEnemy_list:
            if arcade.check_for_collision_with_list(sprite_list=self.player_bullet_list, sprite=self.jumpingEnemy):
                arcade.play_sound(self.enemy_hit_sound)
                self.score = self.score + 100
                self.player_bullet.remove_from_sprite_lists()
                self.jumpingEnemy.remove_from_sprite_lists()

    # the enemies will move toward the player
    def enemy_movement(self):
        if self.shootingEnemy in self.shootingEnemy_list and self.enemy == 1:
            self.shootingEnemy.change_x = math.cos(math.atan2((self.player.center_y - self.shootingEnemy.center_y),
                                                              (self.player.center_x
                                                               - self.shootingEnemy.center_x))) * 1
            self.shootingEnemy.change_y = math.sin(math.atan2((self.player.center_y - self.shootingEnemy.center_y),
                                                              (self.player.center_x
                                                               - self.shootingEnemy.center_x))) * 1
        if self.walkingEnemy in self.walkingEnemy_list and self.enemy == 2:
            self.walkingEnemy.change_x = math.cos(math.atan2((self.player.center_y - self.walkingEnemy.center_y),
                                                             (self.player.center_x - self.walkingEnemy.center_x))) * 1
            self.walkingEnemy.change_y = math.sin(math.atan2((self.player.center_y - self.walkingEnemy.center_y),
                                                             (self.player.center_x - self.walkingEnemy.center_x))) * 1
        if self.jumpingEnemy in self.jumpingEnemy_list and self.enemy == 3:
            self.jumpingEnemy.change_x = math.cos(math.atan2((self.player.center_y - self.jumpingEnemy.center_y),
                                                             (self.player.center_x - self.jumpingEnemy.center_x))) * 1
            self.jumpingEnemy.change_y = math.sin(math.atan2((self.player.center_y - self.jumpingEnemy.center_y),
                                                             (self.player.center_x - self.jumpingEnemy.center_x))) * 1

    # stops the enemies movement
    def enemy_stop(self):
        if self.shootingEnemy in self.shootingEnemy_list:
            self.shootingEnemy.change_x = 0
            self.shootingEnemy.change_y = 0
        if self.walkingEnemy in self.walkingEnemy_list:
            self.walkingEnemy.change_x = 0
            self.walkingEnemy.change_y = 0
        if self.jumpingEnemy in self.jumpingEnemy_list:
            self.jumpingEnemy.change_x = 0
            self.jumpingEnemy.change_y = 0

    # enemies will be removed if they hit each other or a wall
    def enemy_collision(self):
        if arcade.check_for_collision_with_list(sprite_list=self.shootingEnemy_list, sprite=self.shootingEnemy):
            # will play a sound when an enemy runs into another enemy
            arcade.play_sound(self.enemy_hit_sound)
            self.score = self.score + 300
            self.shootingEnemy.remove_from_sprite_lists()
        if arcade.check_for_collision_with_list(sprite_list=self.shootingEnemy_list, sprite=self.walkingEnemy):
            arcade.play_sound(self.enemy_hit_sound)
            self.score = self.score + 200
            self.shootingEnemy.remove_from_sprite_lists()
            self.walkingEnemy.remove_from_sprite_lists()
        if arcade.check_for_collision_with_list(sprite_list=self.shootingEnemy_list, sprite=self.jumpingEnemy):
            arcade.play_sound(self.enemy_hit_sound)
            self.score = self.score + 250
            self.shootingEnemy.remove_from_sprite_lists()
            self.jumpingEnemy.remove_from_sprite_lists()
        if arcade.check_for_collision_with_list(sprite_list=self.walkingEnemy_list, sprite=self.walkingEnemy):
            arcade.play_sound(self.enemy_hit_sound)
            self.score = self.score + 100
            self.walkingEnemy.remove_from_sprite_lists()
        if arcade.check_for_collision_with_list(sprite_list=self.walkingEnemy_list, sprite=self.jumpingEnemy):
            arcade.play_sound(self.enemy_hit_sound)
            self.score = self.score + 150
            self.walkingEnemy.remove_from_sprite_lists()
            self.jumpingEnemy.remove_from_sprite_lists()
        if arcade.check_for_collision_with_list(sprite_list=self.jumpingEnemy_list, sprite=self.jumpingEnemy):
            arcade.play_sound(self.enemy_hit_sound)
            self.score = self.score + 200
            self.jumpingEnemy.remove_from_sprite_lists()
        if self.currentMap == self.mapOne:
            if self.shootingEnemy in self.shootingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.shootingEnemy, sprite_list=self.mapOne_wall_list):
                    # will play a sound when an enemy runs into a wall
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 150
                    self.shootingEnemy.remove_from_sprite_lists()
            if self.walkingEnemy in self.walkingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.walkingEnemy, sprite_list=self.mapOne_wall_list):
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 50
                    self.walkingEnemy.remove_from_sprite_lists()
            if self.jumpingEnemy in self.jumpingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.jumpingEnemy, sprite_list=self.mapOne_wall_list):
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 100
                    self.jumpingEnemy.remove_from_sprite_lists()
        if self.currentMap == self.mapTwo:
            if self.shootingEnemy in self.shootingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.shootingEnemy, sprite_list=self.mapTwo_wall_list):
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 150
                    self.shootingEnemy.remove_from_sprite_lists()
            if self.walkingEnemy in self.walkingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.walkingEnemy, sprite_list=self.mapTwo_wall_list):
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 50
                    self.walkingEnemy.remove_from_sprite_lists()
            if self.jumpingEnemy in self.jumpingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.jumpingEnemy, sprite_list=self.mapTwo_wall_list):
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 100
                    self.jumpingEnemy.remove_from_sprite_lists()
        if self.currentMap == self.mapThree:
            if self.shootingEnemy in self.shootingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.shootingEnemy, sprite_list=self.mapThree_wall_list):
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 150
                    self.shootingEnemy.remove_from_sprite_lists()
            if self.walkingEnemy in self.walkingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.walkingEnemy, sprite_list=self.mapThree_wall_list):
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 50
                    self.walkingEnemy.remove_from_sprite_lists()
            if self.jumpingEnemy in self.jumpingEnemy_list:
                if arcade.check_for_collision_with_list(sprite=self.jumpingEnemy, sprite_list=self.mapThree_wall_list):
                    arcade.play_sound(self.enemy_hit_sound)
                    self.score = self.score + 100
                    self.jumpingEnemy.remove_from_sprite_lists()

    # updates the sprites while the game is running
    def on_update(self, delta_time):
        # updates the players and enemies animations in live time
        self.player.update_animation()
        self.shootingEnemy.update_animation()
        self.walkingEnemy.update_animation()
        self.jumpingEnemy.update_animation()
        # player is able to go to map two after completing map one
        if self.currentMap == self.mapOne:
            if self.player.center_x > 970 and self.score == 300:
                self.currentMap = self.mapTwo
                # removes any existing sprites before showing the next map
                if self.player_bullet in self.player_bullet_list:
                    self.player_bullet.remove_from_sprite_lists()
                if self.enemy_bullet in self.enemy_bullet_list:
                    self.enemy_bullet.remove_from_sprite_lists()
                # starts the randomly placed enemies out on map two
                self.map_two_enemies()
                # will play a sound when the player enters the next map
                arcade.play_sound(self.next_map_sound)
                # starts the player out on map two
                self.player.center_x = 15
        # player is able to go to map three after completing map one
        if self.currentMap == self.mapTwo and self.score == 600:
            if self.player.center_x > 970:
                self.currentMap = self.mapThree
                if self.player_bullet in self.player_bullet_list:
                    self.player_bullet.remove_from_sprite_lists()
                if self.enemy_bullet in self.enemy_bullet_list:
                    self.enemy_bullet.remove_from_sprite_lists()
                # starts the randomly placed enemies out on map three
                self.map_three_enemies()
                arcade.play_sound(self.next_map_sound)
                # starts the player out on map three
                self.player.center_x = 15
        self.player_collision()
        self.player_hit()
        # if the player loses all their lives, the player loses and will show a lose screen
        if self.lives == 0:
            self.currentMap = self.mapLoss
            # will play a sound when the player loses all their lives and loses
            arcade.play_sound(self.player_lose_sound)
            if self.shootingEnemy in self.shootingEnemy_list:
                self.shootingEnemy.remove_from_sprite_lists()
            if self.walkingEnemy in self.walkingEnemy_list:
                self.walkingEnemy.remove_from_sprite_lists()
            if self.jumpingEnemy in self.jumpingEnemy_list:
                self.jumpingEnemy.remove_from_sprite_lists()
            if self.player_bullet in self.player_bullet_list:
                self.player_bullet.remove_from_sprite_lists()
            if self.enemy_bullet in self.enemy_bullet_list:
                self.enemy_bullet.remove_from_sprite_lists()
            self.player.center_x = 480
            self.player.center_y = 480
            self.lives = self.lives - 1
        self.bullet_collision()
        self.enemy_shot()
        self.enemy_hit()
        # if the player 'shoots' all the enemies and clears all three maps, the player wins and will show a win screen
        if self.score == 900:
            self.currentMap = self.mapWon
            # will play a sound when the player passes all the maps and wins
            arcade.play_sound(self.player_win_sound)
            if self.player_bullet in self.player_bullet_list:
                self.player_bullet.remove_from_sprite_lists()
            if self.enemy_bullet in self.enemy_bullet_list:
                self.enemy_bullet.remove_from_sprite_lists()
            self.player.center_x = 480
            self.player.center_y = 480
            self.score = self.score + 1600
        self.enemy_collision()
        # both the players 'shot' and enemies 'shot' will disappear if they collide
        if self.player_bullet in self.player_bullet_list and self.enemy_bullet in self.enemy_bullet_list:
            if arcade.check_for_collision_with_list(sprite=self.player_bullet, sprite_list=self.enemy_bullet_list):
                # will play a sound when the players 'shot' and enemies 'shot' collide
                arcade.play_sound(self.bullet_collision_sound)
                self.player_bullet.remove_from_sprite_lists()
                self.enemy_bullet.remove_from_sprite_lists()
        # updates the sprites in live time
        self.player_list.update()
        self.shootingEnemy_list.update()
        self.walkingEnemy_list.update()
        self.jumpingEnemy_list.update()
        self.player_bullet_list.update()
        self.enemy_bullet_list.update()
        # networked multiplayer game
        pass


# networked multiplayer game
def setup_client_connection(client: ShaneHartProject3):
    client_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(client_event_loop)
    client_event_loop.create_task(communication_with_server(client, client_event_loop))
    client_event_loop.run_forever()


async def communication_with_server(client: ShaneHartProject3, event_loop):
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while True:
        udp_client_socket.sendto(client.server_address, Server.SERVER_PORT)
        data_packet = udp_client_socket.recvfrom(1024)
        data = data_packet[0]
        decoded_data: Player.GameState = Player.GameState.from_json(data)
        player_dict = decoded_data.player_states
        player_info: Player.Player = player_dict[client.ip_address]
        client.from_server = player_info.points
        client.player.center_x = player_info.x_location
        client.player.center_y = player_info.y_location


# main program that builds my Berserk style game
def main():
    # networked multiplayer game
    client_address = Server.find_ip_address()
    server_address = input("Please enter the IP address of the server: ")
    if server_address == Server.server_ip:
        game = ShaneHartProject3(server_address, client_address)
        game.setup()
        client_thread = threading.Thread(target=setup_client_connection, args=(game,), daemon=True)
        client_thread.start()
        arcade.run()
    else:
        print("Wrong IP address, access denied.")
        exit()


# runs main
if __name__ == "__main__":
    main()
