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


def render_lyrics_typed_by_word(lyric, num_words, chars_in_current_word, colors):
    words = lyric.split()
    result = ""
    color_choices = ['G', 'R']

    # Render fully visible words
    for w in range(num_words):
        for ch in words[w]:
            color_code = colors.get(random.choice(color_choices), colors['G'])
            result += color_code + ch + colors['END']
        result += " "

    # Render partially visible next word (if any)
    if num_words < len(words):
        partial_word = words[num_words][:chars_in_current_word]
        for ch in partial_word:
            color_code = colors.get(random.choice(color_choices), colors['G'])
            result += color_code + ch + colors['END']

    return result

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

    frame_delay = 0.15
    lyric_delay = 2.3
    frames_per_line = max(1, int(round(lyric_delay / frame_delay)))
    total_frames = frames_per_line * len(lyric_lines) + 40

    tree_indent = 2

    colors = {
        'R': '\033[31m',  # Red
        'G': '\033[32m',  # Green
        'END': '\033[0m'  # Reset
    }

    # Calculate max lyric line length for padding
    lyric_column_width = max(len(s) for s in lyric_lines) + 2

    try:
        for frame in range(total_frames):
            star_colors = random_star_colors(tree)
            trunk_colors = random_trunk_colors(tree)
            clear_console()
            tree_lines = render_tree(tree, star_colors, trunk_colors)

            full_visible_lines = min(len(lyric_lines), frame // frames_per_line)

            for idx, tline in enumerate(tree_lines):
                if idx < full_visible_lines:
                    # show full line in twinkle colors word-by-word (all words fully)
                    lline = render_lyrics_typed_by_word(lyric_lines[idx], len(lyric_lines[idx].split()), 0, colors)
                elif idx == full_visible_lines and full_visible_lines < len(lyric_lines):
                    # calculate which word and partial chars for current typing
                    words_in_line = lyric_lines[full_visible_lines].split()
                    total_words = len(words_in_line)
                    # progress through words over frames_per_line frames
                    word_progress = frames_per_line * 2  # speed adjustment, you can tweak this
                    # map frame progress to word count + partial char count
                    progress_ratio = (frame % frames_per_line) / frames_per_line

                    num_words = int(progress_ratio * total_words)
                    chars_in_word = int((progress_ratio * total_words - num_words) * len(words_in_line[min(num_words, total_words - 1)])) if num_words < total_words else 0

                    lline = render_lyrics_typed_by_word(lyric_lines[full_visible_lines], num_words, chars_in_word, colors)
                else:
                    lline = ""

                print((' ' * tree_indent) + tline + "   " + lline.ljust(lyric_column_width + 10))

            time.sleep(frame_delay)
    except KeyboardInterrupt:
        pass

   
   

if __name__ == "__main__":
    main()
