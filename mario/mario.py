import tkinter as tk

# Game setup
root = tk.Tk()
root.title("Mario Game")
root.resizable(False, False)

# Canvas setup
canvas = tk.Canvas(root, width=800, height=600, bg="skyblue")
canvas.pack()

# Ground and platforms
ground = canvas.create_rectangle(0, 580, 800, 600, fill="green")
platforms = [
    canvas.create_rectangle(100, 500, 300, 520, fill="brown"),
    canvas.create_rectangle(400, 400, 600, 420, fill="brown"),
    canvas.create_rectangle(200, 300, 400, 320, fill="brown")
]

# Player setup
player = canvas.create_rectangle(50, 540, 90, 580, fill="red")
player_velocity = [0, 0]  # [x_velocity, y_velocity]
on_ground = False

# Constants
gravity = 1
jump_strength = -15
move_speed = 10

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

    # Loop this function
    root.after(20, move_player)

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
