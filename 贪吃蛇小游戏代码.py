"""
游戏玩法：回车开始游戏；空格暂停游戏/继续游戏；方向键/wsad控制小蛇走向
思路：用列表存储蛇的身体；用浅色表示身体，深色背景将身体凸显出来；
蛇的移动：仔细观察，是：身体除头和尾不动、尾部消失，头部增加，所以，新添加的元素放在列表头部、删除尾部元素；
游戏结束判定策略：超出边界；触碰到自己的身体：蛇前进的下一格子为身体的一部分（即在列表中）。
"""
# 注：因为在列表中需要频繁添加和删除元素，所以用deque容器代替列表；是因为deque具有高效的插入和删除效率
# 初始化蛇，长度为3，放置在屏幕左上角；
# 导包
import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque
# 初始化pygame.mixer
pygame.mixer.init()

# 加载背景音乐
main_music = (pygame.mixer.music.load
              ("C:\\Users\\86135\\Desktop\\战一柔 - 空铃.MP3"))
pygame.mixer.music.play(-1)  # -1 表示无限循环播放
# 基础设置
Screen_Height = 500
Screen_Width = 800
Size = 20  # 小方格大小
Line_Width = 1
# 游戏区域的坐标范围
Area_x = (0, (Screen_Width * 0.625) // Size - 1)
Area_y = (2, Screen_Height // Size - 1)

# 食物的初步设置
Food_Style_List = [
    (10, (255, 100, 100)),  # 红色食物，分值为 10
    (20, (100, 255, 100)),  # 绿色食物，分值为 20
    (30, (100, 100, 255)),  # 蓝色食物，分值为 30
    (0, (0, 0, 0))  # 黑色食物（炸弹），分值为 0
]
Bomb_Food = (0, (0, 0, 0))  # 炸弹食物的标识
# 整体颜色设置
Light = (100, 100, 100)
Dark = (200, 200, 200)
Black = (0, 0, 0)
Red = (200, 30, 30)
Back_Ground = (30, 30, 50)
Purple = (128, 0, 128)  # 紫色的RGB值

# 加载炸弹图像
bomb_image = pygame.image.load("D:\pycharm文件\python课程实验\炸弹.webp")  # 假设炸弹图像文件名为 bomb.png
bomb_image = pygame.transform.scale(bomb_image, (Size, Size))  # 缩放炸弹图像到 Size x Size


# 文本输出格式设置
def Print_Txt(screen, font, x, y, text, fcolor=(255, 255, 255)):
    Text = font.render(text, True, fcolor)
    screen.blit(Text, (x, y))



# 初始化蛇
def init_snake():
    snake = deque()
    snake.append((2, Area_y[0]))
    snake.append((1, Area_y[0]))
    snake.append((0, Area_y[0]))
    return snake


# 食物设置
def Creat_Food(snake, food_list):
    food_x = random.randint(Area_x[0], Area_x[1])
    food_y = random.randint(Area_y[0], Area_y[1])
    while (food_x, food_y) in snake or (food_x, food_y) in food_list:
        food_x = random.randint(Area_x[0], Area_x[1])
        food_y = random.randint(Area_y[0], Area_y[1])
    return food_x, food_y

# 食物风格
def Food_Style():
    return random.choice(Food_Style_List)


# 每个模式的通关分数
PASS_SCORES = {
    'easy': 500,
    'medium': 300,
    'hard': 200
}

# 玩家的当前分数
PLAYER_SCORES = {
    'easy': 0,
    'medium': 0,
    'hard': 0
}


# 显示模式选择页面
def display_mode_selection(screen, font):
    screen.fill(Back_Ground)
    Print_Txt(screen, font, 150, 100, "选择游戏模式", (255, 255, 0))
    Print_Txt(screen, font, 50, 200, "1: 简单模式", (255, 255, 255))
    Print_Txt(screen, font, 50, 250, "2: 中等模式", (255, 255, 255))
    Print_Txt(screen, font, 50, 300, "3: 困难模式", (255, 255, 255))
    Print_Txt(screen, font, 50, 350, f"简单模式通关分数: {PASS_SCORES['easy']}",
              (255, 255, 255))
    Print_Txt(screen, font, 50, 400, f"中等模式通关分数: {PASS_SCORES['medium']}",
              (255, 255, 255))
    Print_Txt(screen, font, 50, 450, f"困难模式通关分数: {PASS_SCORES['hard']}",
              (255, 255, 255))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (K_1, K_KP1):
                    return 'easy', 0.5  # 简单模式速度
                elif event.key in (K_2, K_KP2):
                    return 'medium', 0.1  # 中等模式速度
                elif event.key in (K_3, K_KP3):
                    return 'hard', 0.05  # 困难模式速度
            elif event.type == KEYDOWN and  event.key == K_m:
                if event.key in (K_1, K_KP1):
                    return 'easy', 0.5  # 简单模式速度
                elif event.key in (K_2, K_KP2):
                    return 'medium', 0.1  # 中等模式速度
                elif event.key in (K_3, K_KP3):
                    return 'hard', 0.05  # 困难模式速度


# 游戏信息显示
def display_game_info(screen, font1, score, pass_score, elapsed_time):
    # 显示通关分数
    pass_score_text = f'通关分数: {pass_score}'
    Print_Txt(screen, font1, Screen_Width - 200, Area_y[0] * Size + 1, pass_score_text,
              (255, 255, 255))
    # 显示时间
    minutes, seconds = divmod(elapsed_time, 60)
    time_text = f'时间: {int(minutes):02d}:{int(seconds):02d}'
    Print_Txt(screen, font1, Screen_Width - 200, Area_y[0] * Size + 2 * Size + 1,
              time_text, (255, 255, 255))


# 显示游戏结束页面
def game_over_screen(screen, font1, font2, mode, score, elapsed_time, speed, game_won):
    screen.fill(Back_Ground)
    if game_won:
        message = 'GAME PASS'
        color = Red  # 使用红色字体显示通关信息
    else:
        message = 'GAME OVER'
        color = Red  # 使用红色字体显示游戏结束信息

    Print_Txt(screen, font2, (Screen_Width - font2.size(message)[0]) // 2,
              Screen_Height // 2 - 50, message, Red)
    Print_Txt(screen, font1, 50, Screen_Height // 2 + 50, "按 R 重来 或 Q 退出,按 M 返回主界面",
              (255, 255, 255))
    Print_Txt(screen, font1, 50, Screen_Height // 2 + 100, f"得分: {score}",
              (255, 255, 255))
    Print_Txt(screen, font1, 50, Screen_Height // 2 + 150,
              f"时间: {int(elapsed_time // 60):02d}:{int(elapsed_time % 60):02d}",
              (255, 255, 255))
    Print_Txt(screen, font1, 50, Screen_Height // 2 + 200, f"速度: {speed:.2f}",
              (255, 255, 255))
    if not game_won:
        pass_score = PASS_SCORES[mode]
        required_score = pass_score - PLAYER_SCORES[mode]
        Print_Txt(screen, font1, 50, Screen_Height // 2 + 250,
                  f"还需 {required_score} 分通关", (255, 255, 255))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return True  # 重来
                elif event.key == K_q:
                    return False  # 退出
                elif event.key == K_m:  # 按 M 返回主界面
                    return None  # 返回 None 表示返回主界面



def main():
    pygame.init()
    screen = pygame.display.set_mode((Screen_Width, Screen_Height))
    pygame.display.set_caption('贪吃蛇大冒险')
    font1 = pygame.font.SysFont('SimHei', 24)
    font3 = pygame.font.SysFont('SimHei', 14)
    mode, orispeed = display_mode_selection(screen, font1)
    font2 = pygame.font.SysFont(None, 72)
    fwidth, fheight = font2.size('GAME OVER')
    b = True
    snake = init_snake()  # 蛇
    food_list = []
    food_styles = []  # 食物
    normal_food_count = 0  # 正常食物计数
    for _ in range(5):
        food = Creat_Food(snake, food_list)
        food_list.append((food[0], food[1]))
        food_styles.append(Food_Style())
    pos = (1, 0)  # 方向控制
    game_over = True
    game_start = False
    score = PLAYER_SCORES[mode]
    speed = orispeed
    last_move_time = None
    start_time = time.time()  # 记录游戏开始时间
    pause = False
    game_won = False
    elapsed_time = 0  # 定义 elapsed_time 变量
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        game_over = False
                        game_start = True
                        b = True
                        snake = init_snake()
                        food_list = []
                        food_styles = []
                        normal_food_count = 0
                        for _ in range(10):
                            food = Creat_Food(snake, food_list)
                            food_list.append((food[0], food[1]))
                            food_styles.append(Food_Style())
                        pos = (1, 0)
                        score = PLAYER_SCORES[mode]
                        last_move_time = time.time()
                        start_time = time.time()  # 重置游戏开始时间
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                elif event.key in (K_UP, K_w):
                    if b and not pos[1]:
                        pos = (0, -1)
                        b = False
                elif event.key in (K_DOWN, K_s):
                    if b and not pos[1]:
                        pos = (0, 1)
                        b = False
                elif event.key in (K_LEFT, K_a):
                    if b and not pos[0]:
                        pos = (-1, 0)
                        b = False
                elif event.key in (K_RIGHT, K_d):
                    if b and not pos[0]:
                        pos = (1, 0)
                        b = False

        screen.fill(Back_Ground)
        for x in range(Size, Screen_Width, Size):
            pygame.draw.line(screen, Black, (x, Area_y[0] * Size),
                             (x, Screen_Height), Line_Width)
        for y in range(Area_y[0] * Size, Screen_Height, Size):
            pygame.draw.line(screen, Black, (0, y), (Screen_Width, y),
                             Line_Width)
            # 绘制屏障
        for y in range(Size * 2, Screen_Height + Size, Size):
            pygame.draw.line(screen, Purple, (Screen_Width * 0.625, y),
                             (Screen_Width, y), Line_Width)  # 右侧屏障

        if not game_over and game_start:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s in food_list:
                        food_index = food_list.index(next_s)
                        food_style = food_styles[food_index]
                        if food_style[0] == 0:  # 炸弹食物
                            game_over = True
                            if not game_over_screen(screen, font1, font2, mode, score,
                                                    elapsed_time, speed, game_won):
                                break
                        else:
                            snake.appendleft(next_s)
                            score += food_style[0]
                            speed = orispeed - 0.03 * (score // 100)
                            food_list.pop(food_index)
                            food_styles.pop(food_index)
                            normal_food_count += 1
                            if normal_food_count >= 3:  # 每吃掉三个正常食物，增加一个炸弹食物
                                normal_food_count = 0
                                bomb_food = Creat_Food(snake, food_list)
                                while bomb_food in food_list:  # 确保炸弹食物不与正常食物重复
                                    bomb_food = Creat_Food(snake, food_list)
                                food_list.append(bomb_food)
                                food_styles.append(Bomb_Food)
                                # 重新生成正常食物
                                for _ in range(3):
                                    food = Creat_Food(snake, food_list)
                                    food_list.append((food[0], food[1]))
                                    food_styles.append(Food_Style())
                    else:
                        # 在区域内
                        if (Area_x[0] <= next_s[0] <= Area_x[1] and
                                Area_y[0] <= next_s[1] <= Area_y[1] and next_s not in snake):
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True

                        if score >= PASS_SCORES[mode]:  # 检查是否达到通关分数
                            game_over = True
                            game_won = True
                        # 画食物
                    if not game_over:
                        for i, food in enumerate(food_list):
                            if food_styles[i][0] == 0:  # 炸弹食物
                                screen.blit(bomb_image, (food[0] * Size, food[1] * Size))  # 绘制炸弹图像
                            else:
                                pygame.draw.rect(screen, food_styles[i][1],
                                                 (food[0] * Size, food[1] * Size, Size, Size), 0)
                        # 画蛇
                    for s in snake:
                        pygame.draw.rect(screen, Dark, (
                            s[0] * Size + Line_Width, s[1] * Size + Line_Width, Size - Line_Width * 2,
                            Size - Line_Width * 2), 0)
                        # 显示得分和速度
                        Print_Txt(screen, font1, Screen_Width - 200, 7, f'得分: {score}')
                        Print_Txt(screen, font1, Screen_Width - 200, 120,
                                  f'速度: {orispeed - 0.03 * (score // 100):.2f}')
                    game_instructions1 = "回车开启贪吃蛇大冒险，空格暂停/继续"
                    game_instructions2 = "方向键/WASD操控小蛇灵活走位"
                    game_instructions3 = "红色美食，分值 10，助你成长"
                    game_instructions4 = "绿色珍馐，分值 20，加速前进"
                    game_instructions5 = "蓝色佳肴，分值 30，冲击高分"
                    Print_Txt(screen, font3, Screen_Width - 300, 200, game_instructions1)
                    Print_Txt(screen, font3, Screen_Width - 300, 250, game_instructions2)
                    Print_Txt(screen, font3, Screen_Width - 300, 300, game_instructions3)
                    Print_Txt(screen, font3, Screen_Width - 300, 350, game_instructions4)
                    Print_Txt(screen, font3, Screen_Width - 300, 400, game_instructions5)
                    display_game_info(screen, font1, score, PASS_SCORES[mode], time.time() - start_time)

                    # 画GameOver
                    if game_over:
                        elapsed_time = time.time() - start_time

                        restart = game_over_screen(screen, font1, font2, mode, score,
                                                   elapsed_time, speed, game_won)
                        if restart is None:  # 如果玩家选择返回主界面
                            mode, orispeed = display_mode_selection(screen, font1)  # 重新显示模式选择页面

                        elif not restart:  # 如果玩家选择退出
                            break  # 退出游戏循环
                        game_start = True
                        game_over = False
                        game_won = False  # 重置游戏通关状态
                        score = PLAYER_SCORES[mode]  # 重置分数
                        snake = init_snake()
                        food_list = []
                        food_styles = []
                        normal_food_count = 0
                        for _ in range(10):
                            food = Creat_Food(snake, food_list)
                            food_list.append((food[0], food[1]))
                            food_styles.append(Food_Style())
                        pos = (1, 0)
                        last_move_time = time.time()
                        start_time = time.time()  # 重置游戏开始时间
                        elapsed_time = 0  # 重置 elapsed_time
                    pygame.display.update()


if __name__ == '__main__':
    main()
