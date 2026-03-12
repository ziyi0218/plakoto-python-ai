import pygame
import sys

# --------------------------------------------
# 配置部分
# --------------------------------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FPS = 30

# 棋盘点位总数
NUM_POINTS = 24

# 颜色定义
COLOR_BACKGROUND = (0xDD, 0xBB, 0x88)     # 棋盘背景色
COLOR_LIGHT_POINT = (0xF0, 0xD9, 0xB5)   # 浅色尖（Point）
COLOR_DARK_POINT = (0xB5, 0x88, 0x63)    # 深色尖（Point）
COLOR_WHITE_PIECE = (255, 255, 255)      # 白棋颜色
COLOR_BLACK_PIECE = (0, 0, 0)            # 黑棋颜色
COLOR_BORDER = (0, 0, 0)                 # 线框颜色

# 每个尖的宽度与半高度（将棋盘分为上下两排尖）
POINT_WIDTH = WINDOW_WIDTH / NUM_POINTS
HALF_BOARD_HEIGHT = WINDOW_HEIGHT / 2

# 棋子半径：设置为尖宽度的 40% 再除以 2
PIECE_RADIUS = POINT_WIDTH * 0.4 / 2

# --------------------------------------------
# 初始化 Pygame
# --------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Backgammon 棋盘示例 (Pygame)")
clock = pygame.time.Clock()

# --------------------------------------------
# 函数：绘制棋盘上 24 个“尖”（Point）
# --------------------------------------------
def draw_board():
    # 先填充背景
    screen.fill(COLOR_BACKGROUND)

    for i in range(NUM_POINTS):
        # 计算当前点在 x 方向的起始与终止坐标
        x_start = i * POINT_WIDTH
        x_end = x_start + POINT_WIDTH

        # 奇偶索引切换颜色
        if i % 2 == 0:
            point_color = COLOR_DARK_POINT
        else:
            point_color = COLOR_LIGHT_POINT

        if i < 12:
            # 上半区：三角形顶端在 y=HALF_BOARD_HEIGHT，下端在 y=0
            triangle = [
                (x_start, 0),                            # 左上
                (x_end, 0),                              # 右上
                (x_start + POINT_WIDTH / 2, HALF_BOARD_HEIGHT)  # 中下
            ]
        else:
            # 下半区：三角形顶端在 y=HALF_BOARD_HEIGHT，下端在 y=WINDOW_HEIGHT
            triangle = [
                (x_start, WINDOW_HEIGHT),                        # 左下
                (x_end, WINDOW_HEIGHT),                          # 右下
                (x_start + POINT_WIDTH / 2, HALF_BOARD_HEIGHT)    # 中上
            ]

        # 实际绘制三角形
        pygame.draw.polygon(screen, point_color, triangle)
        # 绘制三角形边框
        pygame.draw.polygon(screen, COLOR_BORDER, triangle, 1)

    # 最外层边框（可选）
    pygame.draw.rect(screen, COLOR_BORDER, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 2)


# --------------------------------------------
# 函数：在指定点上堆叠 n 个棋子
#   参数：
#     point_index: 0~23，对应棋盘上的第 1~24 点
#     color: COLOR_WHITE_PIECE 或 COLOR_BLACK_PIECE
#     n: 棋子数量
# --------------------------------------------
def draw_stacked_pieces(point_index, color, n):
    # 先计算该 point 的中心 x 坐标
    x_center = point_index * POINT_WIDTH + POINT_WIDTH / 2

    # 如果是上半区（索引 0~11），棋子从上往下堆叠
    if point_index < 12:
        # y 从 HALF_BOARD_HEIGHT - piece_margin 依次往上排
        for j in range(n):
            # 每个棋子间隔一点缝隙（2 像素）
            y_center = (PIECE_RADIUS + 2) + j * (PIECE_RADIUS * 2 + 2)
            # 由于 y_origin=0 位于屏幕顶部，需要把棋子的中心放在 y_center
            # 但这些 y_center 不要超过 HALF_BOARD_HEIGHT - PIECE_RADIUS，否则越界
            if y_center + PIECE_RADIUS > HALF_BOARD_HEIGHT:
                # 如果堆叠高度超过，需要向下调整，让它顶着半板高度
                y_center = HALF_BOARD_HEIGHT - PIECE_RADIUS
                # 若过多，可依次重叠
            pygame.draw.circle(screen, color, (int(x_center), int(y_center)), int(PIECE_RADIUS))
            pygame.draw.circle(screen, COLOR_BORDER, (int(x_center), int(y_center)), int(PIECE_RADIUS), 1)
    else:
        # 下半区（索引 12~23），棋子从下往上堆叠
        for j in range(n):
            y_center = (WINDOW_HEIGHT - (PIECE_RADIUS + 2)) - j * (PIECE_RADIUS * 2 + 2)
            if y_center - PIECE_RADIUS < HALF_BOARD_HEIGHT:
                y_center = HALF_BOARD_HEIGHT + PIECE_RADIUS
            pygame.draw.circle(screen, color, (int(x_center), int(y_center)), int(PIECE_RADIUS))
            pygame.draw.circle(screen, COLOR_BORDER, (int(x_center), int(y_center)), int(PIECE_RADIUS), 1)


# --------------------------------------------
# 主循环
# --------------------------------------------
def main():
    while True:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 绘制棋盘
        draw_board()

        # 示例：在第 1 点（索引 0）堆叠 15 个白棋
        draw_stacked_pieces(point_index=0, color=COLOR_WHITE_PIECE, n=15)

        # 示例：在第 24 点（索引 23）堆叠 15 个黑棋
        draw_stacked_pieces(point_index=23, color=COLOR_BLACK_PIECE, n=15)

        # 如果需要，你可以在此处绘制其他点位上的初始棋子，例如：
        # draw_stacked_pieces(point_index=11, color=COLOR_BLACK_PIECE, n=2)
        # draw_stacked_pieces(point_index=12, color=COLOR_WHITE_PIECE, n=5)
        # 这些都可以根据规则或需求自行增删。

        # 刷新屏幕
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
