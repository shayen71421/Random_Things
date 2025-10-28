import os
import time
import random


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def render_tree(tree, star_colors=None, trunk_colors=None):
    colors = {
        'R': '\033[31m',  # Red
        'G': '\033[32m',  # Green
        'Y': '\033[33m',  # Yellow
        'B': '\033[34m',  # Blue
        'P': '\033[35m',  # Purple
        '*': '\033[93m',  # Bright Yellow for top star
        '|': '\033[90m',  # Default grey (fallback)
        'END': '\033[0m'  # Reset
    }

    if star_colors is None:
        star_colors = {}
    if trunk_colors is None:
        trunk_colors = {}

    lines = []
    for r, row in enumerate(tree):
        output = ""
        for c, ch in enumerate(row):
            if ch == '*':
                if (r, c) in star_colors:
                    color_code = colors.get(star_colors[(r, c)], colors['G'])
                    output += color_code + '*' + colors['END']
                else:
                    if r == 0:
                        output += colors['*'] + '*' + colors['END']
                    else:
                        output += colors['G'] + '*' + colors['END']
            elif ch == '|':
                if (r, c) in trunk_colors:
                    color_code = colors.get(trunk_colors[(r, c)], colors['|'])
                    output += color_code + '|' + colors['END']
                else:
                    output += colors['|'] + '|' + colors['END']
            else:
                output += ch
        lines.append(output)
    return lines


def random_star_colors(tree):
    positions = []
    for r, row in enumerate(tree):
        for c, ch in enumerate(row):
            if ch == '*' and r != len(tree) - 1:
                positions.append((r, c))
    if not positions:
        return {}
    color_choices = ['R', 'G', 'Y', 'B', 'P']
    return {pos: random.choice(color_choices) for pos in positions}


def random_trunk_colors(tree):
    positions = []
    for r, row in enumerate(tree):
        for c, ch in enumerate(row):
            if ch == '|':
                positions.append((r, c))
    if not positions:
        return {}
    color_choices = ['R', 'G', 'Y', 'B', 'P']
    return {pos: random.choice(color_choices) for pos in positions}


def main():
    lyrics = [
        "A face on a lover",
        "With a fire in his heart",
        "A man undercover",
        "But you tore me apart",
        "oh oh",
        "oh oh",
        "Now I've found a real love",
        "You'll never fool me again"
    ]

    tree = [
        "       *      ",
        "      ***     ",
        "     *****    ",
        "    *******   ",
        "   *********  ",
        "  *********** ",
        " *************",
        "      |||     "
    ]

    max_rows = len(tree)
    lyric_lines = lyrics[:max_rows]
    lyric_column_width = max((len(s) for s in lyric_lines), default=0) + 2

    frame_delay = 0.15
    lyric_delay = 2.3
    frames_per_line = max(1, int(round(lyric_delay / frame_delay)))
    total_frames = frames_per_line * len(lyric_lines) + 40

    tree_indent = 2

    try:
        for frame in range(total_frames):
            star_colors = random_star_colors(tree)
            trunk_colors = random_trunk_colors(tree)
            clear_console()
            tree_lines = render_tree(tree, star_colors, trunk_colors)

            # Calculate how many lines to show fully
            full_visible_lines = min(len(lyric_lines), frame // frames_per_line)
            # Characters to show in typing for the current line
            chars_in_current_line = (frame % frames_per_line) * (lyric_column_width // frames_per_line)

            for idx, tline in enumerate(tree_lines):
                if idx < full_visible_lines:
                    # Show full lyric line
                    lline = lyric_lines[idx]
                elif idx == full_visible_lines and full_visible_lines < len(lyric_lines):
                    # Show lyric partially for typing effect
                    lline = lyric_lines[full_visible_lines][:chars_in_current_line]
                else:
                    lline = ""

                print((' ' * tree_indent) + tline + "   " + lline.ljust(lyric_column_width))

            time.sleep(frame_delay)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
