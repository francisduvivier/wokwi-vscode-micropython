# Setup logging
def log(message):
    print(message)

log("Starting up...")

import random
import time

import accel
import rgb



# Setup RGB
WIDTH, HEIGHT = 32, 19


# Game variables
block_size = 1
block_x, block_y = WIDTH // 2 - block_size//2 -1, HEIGHT // 2 - block_size//2
block_locations = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

def set_pixel(x, y, r, g, b):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        rgb.pixel((r, g, b),(x, y))

def fill(r, g, b):
    rgb.background((r, g, b))

def random_color(max=255):
    if random.randint(0,5) != 0:
        return (0,0,0,0)

    return (random.randint(0,max), random.randint(0,max), random.randint(0,max), 0xff)

def write_kolab(text_color=(255, 000, 000, 0xff), random_background=False):
    message = """
|IIIIIIIIIIIIIIIIIIIIIIIIIIIIII|
|                              |
| K   K  OOO     L    AA  BBB  |
| K  K  O   O    L   A  A B  B |
| KKK   O   O -- L   AAAA BBB  |
| K  K  O   O    L   A  A B  B |
| K   K  OOO     LLL A  A BBB  |
|                              |
|IIIIIIIIIIIIIIIIIIIIIIIIIIIIII|"""

    letter_height = 8

    x_start = 0
    y_start = (HEIGHT - letter_height) // 2
    img_width = len(message.split('\n')[1:][0])
    img_height = len(message.split('\n')[1:])
    # Initialize the data array to store color values for each pixel
    data = [0] * (img_width * img_height)  # Initialize all pixels to black

    # Update the data array based on the message
    for y, row in enumerate(message.split('\n')[1:]):  # Skip the first newline character
        for x, char in enumerate(row):
            index_in_img = (y) * img_width + (x)
            global_y = y + y_start
            global_x = x + x_start
            if char == ' ':
                if block_locations[global_y][global_x]:
                    color = (0,0,0,255) # Turn off places where the block as been
                else:
                    color = random_color(150) if random_background else (0,100,0,0xff)
            else:
                if block_locations[global_y][global_x]:
                    color = (0,255,0,255)
                else:
                    color = text_color  # Assign text color

            (r, g, b, alpha) = color
            color_value = (r << 24) | (g << 16) | (b << 8) | alpha
            data[index_in_img] = color_value

    rgb.image(data, pos=(x_start, y_start), size=(img_width, img_height))

def draw_sparkles():
    write_kolab((255,0,0, 0xff), True)

def draw_block():
    for y in range(block_size):
        for x in range(block_size):
            set_pixel(block_x + x, block_y + y, 255, 255, 255)  # Red color

def update_block_position():
    global block_x, block_y

    if accel:
        ax, ay, _ = accel.get_xyz()
        # Adjust sensitivity as needed
        # print('ax', ax)

        dx = int(ax)
        dy = int(ay)
        # print('dx', dx)

        new_x = max(0, min(WIDTH - block_size, block_x + dx))
        new_y = max(0, min(HEIGHT - block_size, block_y + dy))

        # Update sparkles
        for y in range(block_size):
            for x in range(block_size):
                if not block_locations[new_y + y][new_x + x]:
                    print('marking block location: '+str(new_y + y)+', '+str(new_x + x))
                    block_locations[new_y + y][new_x + x] = True

        block_x, block_y = new_x, new_y

def main():
    accel.init()
    log("[START] main()")
    startup_sequence()
    loop_count = 0
    while True:
        game_loop_once()
        loop_count += 1
        if loop_count % 100 == 0:
            log(f"Main loop iteration: {loop_count}")


def game_loop_once():
    draw_sparkles()
    update_block_position()
    draw_block()
    time.sleep(0.1)  # Add a small delay to prevent the loop from running too fast


def startup_sequence():
    fill(50, 100, 50)
    write_kolab()
    time.sleep(0.5)
    draw_block()


if __name__ == "__main__":
    log("Script started")
    main()
