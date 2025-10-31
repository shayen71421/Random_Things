import os
import time
import random

CYAN = '\033[36m'
RED = '\033[31m'
WHITE = '\033[97m'
YELLOW = '\033[33m'
END = '\033[0m'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_snowman():
    # Snowman designed to sit at the bottom center (ground)
    return [
        "       ___===___      ",
        "      /         \\     ",
        "     |   (o o)   |    ",
        "     |    \\_/    |    ",
        "      \\   ---   /     ",
        "       \\  ~~~  /      ",
        "      /       \\       ",
        "     /  O   O  \\      ",
        "    /    O      \\     ",
        "    \\___________/     "
    ]

def print_scene(snowmap, snowman, lyrics, lyric_pad=6, ground_level=0):
    """
    snowmap: height x width 2D list representing the falling and ground snow
    snowman: ASCII lines positioned at the ground
    lyrics : lines to display at right
    ground_level: where ground starts (row index, from the top)
    """
    height = len(snowmap)
    width = len(snowmap[0])

    # Prepare snowman to be printed at the bottom of snowmap
    snowman_start_row = height - len(snowman)
    lyric_start_row = snowman_start_row  # lyrics aligned with snowman

    for row in range(height):
        # Make snow line from map
        line = "".join(WHITE + "*" + END if snowmap[row][col] else " " for col in range(width))

        # Insert snowman and lyrics at the base
        if snowman_start_row <= row < height:
            sm_i = row - snowman_start_row
            s = snowman[sm_i]
            l = lyrics[sm_i] if sm_i < len(lyrics) else ""
            print(line + " " * lyric_pad + s + "   " + l)
        else:
            print(line)

def main():
    lyrics_src = [
        "I want you to know",
        "that I'm never leaving,",
        "'Cause I'm Mrs. Snow",
        "till death we'll be freezing, yeah.",
        "You are my home, my home for all seasons,",
        "So come on, let's go!",
        "Let's go below zero and hide from the sun",
        "I love you forever where we'll have some fun"
    ]

    # Dimensions for animation
    width = 48
    height = 22
    lyric_pad = 3

    # Snowman at ground
    snowman = get_snowman()

    # Snow state: map of 0 (air) or 1 (snow) for ground/falling
    snowmap = [[0]*width for _ in range(height)]

    # Snowfall (falling snowflakes positions)
    snowflakes = []
    for _ in range(38):
        col = random.randint(0, width-1)
        snowflakes.append([random.randint(0, height-11), col])

    total_words = [len(x.split()) for x in lyrics_src]
    current_line = 0
    current_word = 1
    lyrics_done = False

    while True:
        clear_console()
        # Drop snowflakes
        for flake in snowflakes:
            y, x = flake
            # Try to move down until hit ground (or snow already at that spot)
            if y < height-1 and snowmap[y+1][x] == 0:
                flake[0] += 1
            else:
                # Accumulate snow at that spot and respawn flake at top
                snowmap[y][x] = 1
                flake[0] = 0
                flake[1] = random.randint(0, width-1)

        # Animate lyrics (word by word, then freeze)
        if not lyrics_done:
            lyrics = []
            for i in range(len(lyrics_src)):
                if i < current_line:
                    lyrics.append(CYAN + lyrics_src[i] + END)
                elif i == current_line:
                    words = lyrics_src[i].split()
                    current = " ".join(words[:current_word])
                    lyrics.append(CYAN + current + END)
                else:
                    lyrics.append("")
        else:
            lyrics = [CYAN + l + END for l in lyrics_src]

        print_scene(snowmap, snowman, lyrics, lyric_pad=lyric_pad)
        time.sleep(0.15)

        # Progress lyric animation
        if not lyrics_done:
            current_word += 1
            if current_line < len(lyrics_src) and current_word > total_words[current_line]:
                current_line += 1
                current_word = 1
            if current_line >= len(lyrics_src):
                lyrics_done = True

if __name__ == "__main__":
    main()
