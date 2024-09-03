# Setup logging
def log(message):
    print(message)

log("Starting up...")

import random
import time

import accel
import rgb
import buttons


# Setup RGB
WIDTH, HEIGHT = 32, 19

#Setup accel
accel.init()


# Game variables
block_size = 1
block_x, block_y = WIDTH // 2 - block_size//2 -1, HEIGHT // 2 - block_size//2
sparkles = [[True for _ in range(WIDTH)] for _ in range(HEIGHT)]

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
    log("Writing KO-LAB...")

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
            if char != ' ':
                color = text_color  # Assign text color
            elif char == ' ':
                color = random_color(150) if random_background else (0,100,0,0xff)
            else:
                continue  # Other characters are also skipped (if any)

            # Check if the position is within the screen dimensions
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # Calculate the index in the linear data array
                index = (y) * WIDTH + (x)
                # Update the data array with the selected color
                (r, g, b, alpha) = color
                color_value = (r << 24) | (g << 16) | (b << 8) | alpha
                data[index] = color_value
    rgb.image(data, pos=(x_start, y_start), size=(img_width, img_height))

def draw_sparkles():
    write_kolab((150,0,0, 0xff), True)

def draw_block():
    for y in range(block_size):
        for x in range(block_size):
            set_pixel(block_x + x, block_y + y, 0, 0, 255)  # Red color

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
                sparkles[new_y + y][new_x + x] = False

        block_x, block_y = new_x, new_y

def test_image():
    data = [0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0x000000ff, 0x000000ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff, 0xffbf00ff]
    rgb.clear()
    rgb.image(data, pos=(12, 0), size=(8, 8))

def clear_display(button_is_down, button_name):
    print('BUTTON '+button_name+' Callback! down: '+ str(button_is_down))
    if button_is_down:
        rgb.clear()
        pass

def setup_button_callback():
     buttons.register(buttons.BTN_A, lambda down: clear_display(down, 'A'))
     buttons.register(buttons.BTN_B, lambda down: clear_display(down, 'B'))
     buttons.register(buttons.BTN_UP, lambda down: clear_display(down, 'UP'))
     buttons.register(buttons.BTN_DOWN, lambda down: clear_display(down, 'DOWN'))
     buttons.register(buttons.BTN_LEFT, lambda down: clear_display(down, 'LEFT'))
     buttons.register(buttons.BTN_RIGHT, lambda down: clear_display(down, 'RIGHT'))

def main():
    log("Entering main function")
    test_image()
    time.sleep(0.5)
    setup_button_callback()
    fill(50,100,50)
    write_kolab()
    time.sleep(0.5)
    loop_count = 0
    while True:
        draw_sparkles()
        update_block_position()
        draw_block()
        time.sleep(0.1)  # Add a small delay to prevent the loop from running too fast

        loop_count += 1
        if loop_count % 100 == 0:
            log(f"Main loop iteration: {loop_count}")

if __name__ == "__main__":
    log("Script started")
    main()
