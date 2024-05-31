import tkinter as tk
import random

# Game setup
root = tk.Tk()
root.title("Eenvoudig Shooter Game")
root.resizable(False, False)

# Canvas setup
canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

# Player setup
player = canvas.create_rectangle(370, 550, 430, 580, fill="blue")

# Player movement
player_speed = 20
def move_left(event):
    canvas.move(player, -player_speed, 0)
def move_right(event):
    canvas.move(player, player_speed, 0)

# Bullet setup
bullets = []
bullet_speed = 10
def shoot(event):
    x1, y1, x2, y2 = canvas.coords(player)
    bullet = canvas.create_rectangle(x1 + 27, y1 - 10, x2 - 27, y1, fill="yellow")
    bullets.append(bullet)

# Enemy setup
enemies = []
enemy_speed = 2
def create_enemy():
    x = random.randint(50, 750)
    enemy = canvas.create_rectangle(x, 50, x + 50, 100, fill="red")
    enemies.append(enemy)
    root.after(2000, create_enemy)  # Create a new enemy every 2 seconds

# Move bullets
def move_bullets():
    for bullet in bullets:
        canvas.move(bullet, 0, -bullet_speed)
        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
    root.after(50, move_bullets)

# Move enemies
def move_enemies():
    for enemy in enemies:
        canvas.move(enemy, 0, enemy_speed)
        if canvas.coords(enemy)[3] > 600:
            canvas.delete(enemy)
            enemies.remove(enemy)
        else:
            for bullet in bullets:
                if check_collision(bullet, enemy):
                    canvas.delete(bullet)
                    bullets.remove(bullet)
                    canvas.delete(enemy)
                    enemies.remove(enemy)
                    break
    root.after(50, move_enemies)

# Check collision
def check_collision(bullet, enemy):
    bullet_coords = canvas.coords(bullet)
    enemy_coords = canvas.coords(enemy)
    if (bullet_coords[2] >= enemy_coords[0] and bullet_coords[0] <= enemy_coords[2] and
        bullet_coords[3] >= enemy_coords[1] and bullet_coords[1] <= enemy_coords[3]):
        return True
    return False

# Key bindings
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<space>", shoot)

# Start the game
create_enemy()
move_bullets()
move_enemies()

# Run the Tkinter main loop
root.mainloop()
