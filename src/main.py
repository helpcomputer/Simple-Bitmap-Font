
import pyxel

WIDTH = 128
HEIGHT = 128
TITLE = "Simple Bitmap Font"
FPS = 30
IMAGE_FILE = "characters.png"
IMAGE_BANK = 0

# These should match the font image.
FONT_COLOUR = pyxel.COLOR_WHITE
FONT_TRANSPARENT_COLOUR = pyxel.COLOR_BLACK
FONT_CHAR_WIDTH = 5
FONT_CHAR_HEIGHT = 12
FONT_CHARS_PER_ROW = 20

ASCII_CHAR_SPACE = 32
FONT_CHAR_START = 0
FONT_CHAR_END = 95

TEST_TEXT = "The quick \nbrown fox \njumped over \nthe lazy dog!"

def draw_ascii_text(x, y, text, new_colour=None):
    """Draw ASCII text in chosen colour.

    This will draw ASCII character codes 32 (Space) to 127 (DEL).
    We set this to 0-95 to make it easier to work with.

    The only other character accepted is line break ('\n'),
    which will move down a line when found.
    """
    # Replace colour in pyxel palette with our new colour.
    if new_colour is not None:
        pyxel.pal(FONT_COLOUR, new_colour)

    u = 0
    v = 0
    xc = 0
    yc = 0
    for char in text:
        # If newline found then move down for next character.
        if char == '\n':
            xc = 0
            yc += FONT_CHAR_HEIGHT
        else:
            # Check that this is a valid ASCII character in our font.
            # Set to start from zero so it's easier to work with.
            c = ord(char) - ASCII_CHAR_SPACE
            if c >= FONT_CHAR_START and c <= FONT_CHAR_END:
                u = (c % FONT_CHARS_PER_ROW) * FONT_CHAR_WIDTH
                v = pyxel.floor(c / FONT_CHARS_PER_ROW) * FONT_CHAR_HEIGHT
                pyxel.blt(
                    x + xc, 
                    y + yc, 
                    IMAGE_BANK, 
                    u, v, 
                    FONT_CHAR_WIDTH, 
                    FONT_CHAR_HEIGHT,
                    FONT_TRANSPARENT_COLOUR
                )
                xc += FONT_CHAR_WIDTH

    # Reset the pyxel palette order.
    pyxel.pal()

class Application:
    def __init__(self):
        pyxel.init(
            WIDTH, 
            HEIGHT, 
            TITLE, 
            FPS,
        )

        self.text_colour = pyxel.COLOR_WHITE
        self.version_colour = pyxel.COLOR_WHITE
        self.pyxel_version_text = "Pyxel v{}".format(pyxel.PYXEL_VERSION)

        pyxel.image(0).load(0, 0, IMAGE_FILE)

        pyxel.run(self.update, self.draw)

    def update(self):
        # Every second we chose a random new colour to draw the text in.
        if pyxel.frame_count % FPS == 0:
            self.text_colour = pyxel.rndi(0, pyxel.NUM_COLORS-1)
            self.version_colour = pyxel.rndi(0, pyxel.NUM_COLORS-1)

    def draw(self):
        pyxel.cls(0)

        draw_ascii_text(
            FONT_CHAR_WIDTH, 
            FONT_CHAR_HEIGHT,
            TEST_TEXT, 
            self.text_colour
        )

        draw_ascii_text(
            WIDTH - len(self.pyxel_version_text) * FONT_CHAR_WIDTH, 
            HEIGHT - FONT_CHAR_HEIGHT, 
            self.pyxel_version_text, 
            self.version_colour
        )

Application()
