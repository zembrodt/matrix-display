from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
from utils import fonts


class Canvas:
    def __init__(self, rows: int, cols: int, brightness: int = 100, show_refresh: bool = False,
                 slowdown_gpio: int = 1):
        self._led_rows = rows
        self._led_cols = cols
        self._led_brightness = brightness
        self._show_refresh = show_refresh
        self._led_slowdown_gpio = slowdown_gpio

        options = RGBMatrixOptions()
        options.rows = self._led_rows
        options.cols = self._led_cols
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = self._led_brightness
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = 'RGB'
        options.pixel_mapper_config = ''
        options.panel_type = ''
        options.gpio_slowdown = self._led_slowdown_gpio
        if self._show_refresh:
            options.show_refresh_rate = 1

        self._matrix = RGBMatrix(options=options)
        self._canvas = self._matrix.CreateFrameCanvas()

    def draw_text_xs(self, x: int, y: int, text: str, text_color: graphics.Color) -> int:
        return self._draw_text(x, y, text, text_color, fonts.xs)

    def draw_text_sm(self, x: int, y: int, text: str, text_color: graphics.Color) -> int:
        return self._draw_text(x, y, text, text_color, fonts.sm)

    def draw_text_md(self, x: int, y: int, text: str, text_color: graphics.Color) -> int:
        return self._draw_text(x, y, text, text_color, fonts.md)

    def draw_text_md_bold(self, x: int, y: int, text: str, text_color: graphics.Color) -> int:
        return self._draw_text(x, y, text, text_color, fonts.md_bold)

    def draw_text_lg(self, x: int, y: int, text: str, text_color: graphics.Color) -> int:
        return self._draw_text(x, y, text, text_color, fonts.lg)

    def draw_text_lg_bold(self, x: int, y: int, text: str, text_color: graphics.Color) -> int:
        return self._draw_text(x, y, text, text_color, fonts.lg_bold)

    def draw_text_xl(self, x: int, y: int, text: str, text_color: graphics.Color) -> int:
        return self._draw_text(x, y, text, text_color, fonts.xl)

    def draw_text_xl_bold(self, x: int, y: int, text: str, text_color: graphics.Color) -> int:
        return self._draw_text(x, y, text, text_color, fonts.xl_bold)

    def _draw_text(self, x: int, y: int, text: str, text_color: graphics.Color, font: graphics.Font) -> int:
        return graphics.DrawText(self._canvas, font, x, y, text_color, text)

    def draw_image(self, x: int, y: int, image: Image):
        self._canvas.SetImage(image, offset_x=x, offset_y=y)

    def draw_circle(self, x: int, y: int, radius: int, color: graphics.Color):
        graphics.DrawCircle(self._canvas, x, y, radius, color)

    def draw_diamond(self, x: int, y: int, length: int, color: graphics.Color):
        _length = length - 1
        if length == 1:
            self.draw_line(x, y, x, y, color)
        elif length == 2:
            self.draw_line(x, y + 1, x + 1, y, color)
            self.draw_line(x + 1, y + 2, x + 2, y + 1, color)
        else:
            # Top left edge
            self.draw_line(x, y + _length, x + _length, y, color)
            # Top right edge
            self.draw_line(x + _length, y, x + (_length * 2), y + _length, color)
            # Bottom right edge
            self.draw_line(x + (_length * 2), y + _length, x + _length, y + (_length * 2), color)
            # Bottom left edge
            self.draw_line(x + _length, y + (_length * 2), x, y + _length, color)

    def draw_line(self, x_start: int, y_start: int, x_end: int, y_end: int, color: graphics.Color):
        graphics.DrawLine(self._canvas, x_start, y_start, x_end, y_end, color)

    def clear(self):
        self._canvas.Clear()

    def swap_on_vsync(self):
        self._canvas = self._matrix.SwapOnVSync(self._canvas)

    @property
    def led_rows(self) -> int:
        return self._led_rows

    @property
    def led_cols(self) -> int:
        return self._led_cols

    @property
    def led_brightness(self) -> int:
        return self._led_brightness
