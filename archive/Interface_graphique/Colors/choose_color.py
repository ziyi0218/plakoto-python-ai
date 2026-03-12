import pygame
import math
import sys

# —————— 配置参数 ——————
CARDS_PER_ROW = 8       # 每行显示多少个颜色
CARD_SIZE     = 80      # 每个色块（正方形）的边长
PADDING       = 10      # 色块之间，以及色块与窗口边缘之间的间距
TEXT_HEIGHT   = 20      # 色块下方显示文字所占高度
FONT_SIZE     = 14      # 颜色名称的字体大小

# 窗口（视口）大小：你可以根据屏幕分辨率自行调整
VIEWPORT_WIDTH  = 800
VIEWPORT_HEIGHT = 600

pygame.init()
# 准备字体
font = pygame.font.SysFont("consolas", FONT_SIZE)

# 把所有预定义颜色拉成列表
all_colors = list(pygame.color.THECOLORS.items())
num_colors  = len(all_colors)

# 计算内容（Content）图层的宽高
rows = math.ceil(num_colors / CARDS_PER_ROW)
content_width  = CARDS_PER_ROW * (CARD_SIZE + PADDING) + PADDING
content_height = rows * (CARD_SIZE + TEXT_HEIGHT + PADDING) + PADDING

# 创建一个比窗口大的 Surface，用于把所有色块一次性画在上面
content_surf = pygame.Surface((content_width, content_height))
content_surf.fill((30, 30, 30))  # 深灰背景，方便看彩色方块

# 在 content_surf 上绘制所有色块和名称
for idx, (name, rgba) in enumerate(all_colors):
    row = idx // CARDS_PER_ROW
    col = idx %  CARDS_PER_ROW

    x = PADDING + col * (CARD_SIZE + PADDING)
    y = PADDING + row * (CARD_SIZE + TEXT_HEIGHT + PADDING)

    # 1) 绘制色块
    rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
    pygame.draw.rect(content_surf, rgba[:3], rect)

    # 2) 绘制名称文字（白色），水平居中，放在色块下方
    text_surf = font.render(name, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + CARD_SIZE/2, y + CARD_SIZE + TEXT_HEIGHT/2))
    content_surf.blit(text_surf, text_rect)

# 创建主窗口（视口）
screen = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
pygame.display.set_caption("可拖拽查看的 Pygame 预定义颜色表")

# 当前 content_surf 相对视口窗口左上角的偏移量（offset_x, offset_y）
offset_x = 0
offset_y = 0

# 用于鼠标拖拽的状态
dragging = False
last_mouse_x = 0
last_mouse_y = 0

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 鼠标按下：开启拖拽，并记录起始鼠标坐标
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键按下开始拖拽
                dragging = True
                last_mouse_x, last_mouse_y = event.pos

        # 鼠标抬起：结束拖拽
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        # 鼠标移动：如果正在拖拽，则根据移动距离更新偏移量
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            dx = mouse_x - last_mouse_x
            dy = mouse_y - last_mouse_y

            # 反向平移：向右拖，偏移量应减少内容的 x；向下拖，偏移量应减少内容的 y
            offset_x -= dx
            offset_y -= dy

            # 限制 offset 范围，不能拖出内容边界（左上不小于 0，右下不超过内容-视口）
            max_offset_x = max(0, content_width - VIEWPORT_WIDTH)
            max_offset_y = max(0, content_height - VIEWPORT_HEIGHT)
            if offset_x < 0:
                offset_x = 0
            elif offset_x > max_offset_x:
                offset_x = max_offset_x

            if offset_y < 0:
                offset_y = 0
            elif offset_y > max_offset_y:
                offset_y = max_offset_y

            last_mouse_x, last_mouse_y = mouse_x, mouse_y

    # 每帧把 content_surf 上的对应区域 blit 到 screen
    screen.fill((0, 0, 0))  # 先填充黑色背景
    screen.blit(content_surf, (-offset_x, -offset_y))

    pygame.display.flip()
    clock.tick(60)  # 限制在 60 FPS

pygame.quit()
sys.exit()
