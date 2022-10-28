import pyglet

import requests

import os
import glob
import time
import random

__version__ = 'v_lithium_2_20221028'


def get_quote_ming() -> str:
    # 通过aa1接口获取激励语 / Get through aa1
    return requests.get('https://v.api.aa1.cn/api/api-wenan-mingrenmingyan/index.php?aa1=json').json[0]['mingrenmingyan']


def get_bg_bing_daily() -> None:
    # 获取每日一图 / Get Bing Daily
    with open('bg.jpeg', 'wb') as bg:
        bg.write(requests.get(
            'https://cn.bing.com' +
            str(requests.get(
                'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1').json()['images'][0]['urlbase']) +
            '_UHD.jpg').content)


def format_quote(quote: str) -> str:
    # 简单的中文格式化 / Simple Chinese Formation
    result = list(quote)
    # 奇怪的算法 / Fucking Ridiculous Algorithm
    offset = 0
    for index, item in enumerate(result.copy()):
        if item == '—':
            result.insert(index + offset, '\n\t\t')
            break
        elif item == '，' or item == '。':
            result.insert(index + 1 + offset, '\n')
            offset += 1
    return ''.join(result)


def get_music():
    if not os.path.exists('music'):
        return None, None
    try:
        _ = random.choice(glob.glob('music/*.mp3'))
        return pyglet.media.load(_), _
    except IndexError:
        return None, None


print('Download Background from Bing')
# 获取必应每日一图 / Get Bing Daily Image
get_bg_bing_daily()

# 初始化窗口 / Initialize Window
window = pyglet.window.Window(width=1920, height=1080)
window.set_fullscreen(True)

# 激励语标签 / Quote Label
label_quote = pyglet.text.Label(
    '爷是激励语',
    bold=True,
    font_name='Times New Roman',
    font_size=36,
    x=window.width // 2, y=window.height // 2,
    anchor_x='center', anchor_y='baseline',
    align='center',
    multiline=True,
    width=window.width - 250, height=window.height
)

label_about = pyglet.text.Label(
    f'5925御用\n本程序由woshishabi编写\n版本{__version__}\n屏幕左上保存激励语\n左下切换激励语\n右上打开项目主页\n右下抽取保存的激励语',
    font_name='Consolas',
    font_size=10,
    x=0, y=window.height,
    anchor_x='left', anchor_y='top',
    align='left',
    multiline=True,
    width=window.width, height=window.height,
    color=(169, 169, 169, 255)
)

label_log = pyglet.text.Label('', font_name='Consolas', y=10)

# 加载图像并缩放 / Load Image and Resize
bg_image = pyglet.image.load('bg.jpeg')
bg_texture = bg_image.get_texture()
pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
bg_texture.width = 1920
bg_texture.height = 1080

last_click = 0.0
log_time = 0.0
music_time = time.time()
log_flag = False


def log(dt):
    global log_time
    global log_flag
    if time.time() - log_time <= 5:
        log_flag = True
    else:
        log_flag = False
    if time.time() - music_time > 60:
        player.volume = 0


pyglet.clock.schedule_interval(log, .01)

bgm, bgm_fn = get_music()
player = pyglet.media.Player()
if bgm:
    player.queue(bgm)
    player.volume = 0.1
    print('Playing at', player.volume)
    player.play()
    label_log.text = f'Playing {bgm_fn}'
else:
    label_log.text = 'Media Not Found'
log_time = time.time()


@window.event
def on_draw():
    # 渲染事件 / Render Event
    global log_time
    window.clear()
    bg_image.blit(0, 0)
    label_quote.draw()
    label_about.draw()
    if log_flag:
        label_log.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    # 鼠标点击事件 / Mouse Press Event
    global last_click
    global log_time
    print('Click Event: ', x, y, button, modifiers)
    print(window.width, window.height)
    # 检查是否为双击 / Check If Double-Clicked
    if time.time() - last_click < 0.5:
        window.close()
    else:
        last_click = time.time()
    if x <= window.width // 2 and y <= window.height // 2:
        # 屏幕左下 -> 刷新激励语
        label_log.text = 'Getting Quote'
        log_time = time.time()
        _ = format_quote(get_quote_ming())
        label_quote.text = _
        print(_)
    elif x <= window.width // 2 and y >= window.height // 2:
        # 屏幕左上 -> 评分激励语
        print('Rating...')
        label_log.text = 'Rating'
        log_time = time.time()
        _ = requests.post('http://jgbsxx20130315.pythonanywhere.com/api/v1/quote/rated',
                          json={'content': label_quote.text})
        print(_)
    elif x >= window.width // 2 and y <= window.height // 2:
        # 屏幕右下 -> 优质激励语
        print('Getting Rated Quotes')
        label_log.text = 'Getting Rated Quote'
        log_time = time.time()
        q = requests.get('http://jgbsxx20130315.pythonanywhere.com/api/v1/quote/rated').json()['Items']
        _ = q[str(random.randint(1, len(q)))]
        print(_)
        label_quote.text = _
    else:
        # 屏幕右上 -> 停止音乐
        player.volume = 0


# 运行
pyglet.app.run()
