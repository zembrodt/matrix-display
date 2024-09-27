import os
import sys
from rgbmatrix import graphics

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))


def _get_font_path(font_name: str) -> str:
    return f'resources/fonts/{font_name}.bdf'


xs = graphics.Font()
xs.LoadFont(_get_font_path('4x6'))

sm = graphics.Font()
sm.LoadFont(_get_font_path('5x8'))

md = graphics.Font()
md.LoadFont(_get_font_path('6x13'))

md_bold = graphics.Font()
md_bold.LoadFont(_get_font_path('6x13B'))

lg = graphics.Font()
lg.LoadFont(_get_font_path('7x13'))

lg_bold = graphics.Font()
lg_bold.LoadFont(_get_font_path('7x13B'))

xl = graphics.Font()
xl.LoadFont(_get_font_path('8x13'))

xl_bold = graphics.Font()
xl_bold.LoadFont(_get_font_path('8x13B'))
