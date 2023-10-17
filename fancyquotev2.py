import pyglet

import os
import glob
import time
import random

__version__ = 'v_20231017'


# 初始化窗口 / Initialize Window
window = pyglet.window.Window(width=1920, height=1080, resizable=True)
# window.set_fullscreen(True)

# 加载图像并缩放 / Load Image and Resize
fn = random.choice(glob.glob('./*.JPG'))
bg_image = pyglet.image.load(fn)
os.rename(fn, f'{fn}.disabled')
bg_texture = bg_image.get_texture()
pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
bg_texture.width = 1920
bg_texture.height = 1080


@window.event
def on_draw():
    # 渲染事件 / Render Event
    window.clear()
    bg_image.blit(0, 0)


@window.event
def on_mouse_press(x, y, button, modifiers):
    # 鼠标点击事件 / Mouse Press Event
    pyglet.app.exit()


@window.event
def on_resize(width, height):
    label_quote.x = window.width // 2
    label_quote.y = window.height // 2
    label_about.y = window.height
    bg_texture.width = window.width
    bg_texture.height = window.height


# 运行
pyglet.app.run()
