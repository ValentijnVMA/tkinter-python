import tkinter as tk
import random

# Game setup
root = tk.Tk()
root.title("Mario Game")
root.resizable(False, False)

# Canvas setup
canvas = tk.Canvas(root, width=800, height=600, bg="skyblue")
canvas.pack()

# Player setup
player = canvas.create_rectangle(50, 540, 90, 580, fill="red")
player_velocity = [0, 0]  # [x_velocity, y_velocity]
on_ground = False

# Constants
gravity = 1
jump_strength = -15
move_speed = 10
fall_speed = 5

# Platforms
platforms = []

def create_platform(x, y, width=200, height=20):
    return canvas.create_rectangle(x, y, x + width, y + height, fill="brown")

def initialize_platforms():
    for i in range(5):
        x = random.randint(0, 600)
        y = 580 - i * 150
        platforms.append(create_platform(x, y))

initialize_platforms()

# Enemies
enemies = []

def create_enemy():
    x = random.randint(0, 760)
    y = random.randint(-600, 0)
    enemy = canvas.create_rectangle(x, y, x + 40, y + 40, fill="black")
    enemies.append(enemy)

def initialize_enemies():
    for _ in range(5):
        create_enemy()

initialize_enemies()

# Move player
def move_player():
    global on_ground
    on_ground = False

    # Apply gravity
    player_velocity[1] += gravity

    # Move player by velocity
    canvas.move(player, player_velocity[0], player_velocity[1])

    # Check for collision with ground
    player_coords = canvas.coords(player)
    if player_coords[3] >= 580:
        canvas.coords(player, player_coords[0], 540, player_coords[2], 580)
        player_velocity[1] = 0
        on_ground = True

    # Check for collision with platforms
    for platform in platforms:
        platform_coords = canvas.coords(platform)
        if (player_coords[2] > platform_coords[0] and player_coords[0] < platform_coords[2] and
            player_coords[3] > platform_coords[1] and player_coords[1] < platform_coords[3]):
            if player_velocity[1] > 0:
                canvas.coords(player, player_coords[0], platform_coords[1] - 40, player_coords[2], platform_coords[1])
                player_velocity[1] = 0
                on_ground = True

    # Move platforms and enemies down if player goes higher
    if player_coords[1] < 300:
        canvas.move(player, 0, fall_speed)
        for platform in platforms:
            canvas.move(platform, 0, fall_speed)
        for enemy in enemies:
            canvas.move(enemy, 0, fall_speed)

        # Reposition platforms that are out of the screen
        for platform in platforms:
            if canvas.coords(platform)[1] > 600:
                canvas.coords(platform, random.randint(0, 600), random.randint(-200, 0), random.randint(0, 600) + 200, random.randint(-200, 0) + 20)

        # Reposition enemies that are out of the screen
        for enemy in enemies:
            if canvas.coords(enemy)[1] > 600:
                canvas.coords(enemy, random.randint(0, 760), random.randint(-600, 0), random.randint(0, 760) + 40, random.randint(-600, 0) + 40)

    # Check for collision with enemies
    for enemy in enemies:
        enemy_coords = canvas.coords(enemy)
        if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and
            player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
            game_over()

    # Move enemies
    for enemy in enemies:
        canvas.move(enemy, 0, fall_speed)

    # Loop this function
    root.after(20, move_player)

# Restart game function
def restart_game():
    global player_velocity, on_ground, platforms, enemies

    # Reset player position and variables
    canvas.coords(player, 50, 540, 90, 580)
    player_velocity = [0, 0]
    on_ground = False

    # Reposition platforms and enemies
    for platform in platforms:
        canvas.coords(platform, random.randint(0, 600), random.randint(-200, 580), random.randint(0, 600) + 200, random.randint(-200, 580) + 20)

    for enemy in enemies:
        canvas.coords(enemy, random.randint(0, 760), random.randint(-600, 0), random.randint(0, 760) + 40, random.randint(-600, 0) + 40)

    # Rebind keys
    root.bind("<Left>", move_left)
    root.bind("<Right>", move_right)
    root.bind("<space>", jump)
    root.bind("<KeyRelease-Left>", stop_move)
    root.bind("<KeyRelease-Right>", stop_move)

    # Restart the game loop
    move_player()

# Game over function
def game_over():
    canvas.create_text(400, 300, text="GAME OVER", font=("Arial", 32), fill="red")
    root.unbind("<Left>")
    root.unbind("<Right>")
    root.unbind("<space>")
    root.unbind("<KeyRelease-Left>")
    root.unbind("<KeyRelease-Right>")

    # Show message box to ask if the player wants to play again
    if tk.messagebox.askyesno("Game Over", "Wil je opnieuw spelen?"):
        restart_game()
    else:
        root.destroy()

# Key bindings
def move_left(event):
    player_velocity[0] = -move_speed

def move_right(event):
    player_velocity[0] = move_speed

def jump(event):
    if on_ground:
        player_velocity[1] = jump_strength

def stop_move(event):
    player_velocity[0] = 0

# Bind keys to functions
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<space>", jump)
root.bind("<KeyRelease-Left>", stop_move)
root.bind("<KeyRelease-Right>", stop_move)

# Start the game
move_player()

# Run the Tkinter main loop
root.mainloop()
