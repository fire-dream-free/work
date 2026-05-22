# 优先在终端中运行pip install pygame
# 等待它出现：Successfully installed pygame就搞定了！
import pygame
import random

# 初始化
pygame.init()
WIDTH, HEIGHT = 640, 960
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python打飞机")
clock = pygame.time.Clock()

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)


# 玩家飞机
class Player:
    def __init__(self):
        self.x = WIDTH // 2 - 20
        self.y = HEIGHT - 80
        self.w = 40
        self.h = 40
        self.speed = 6

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(0, min(WIDTH - self.w, self.x))
        self.y = max(0, min(HEIGHT - self.h, self.y))

    def draw(self):
        pygame.draw.rect(screen, CYAN, (self.x, self.y, self.w, self.h))


# 子弹
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 6
        self.h = 15
        self.speed = 8

    def update(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.w, self.h))


# 敌机
class Enemy:
    def __init__(self, speed_multiplier=1.0):
        self.x = random.randint(0, WIDTH - 35)
        self.y = -40
        self.w = 35
        self.h = 35
        self.speed = random.uniform(2, 4) * speed_multiplier

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.w, self.h))


# 碰撞检测
def collide(a, b):
    return (a.x < b.x + b.w and
            a.x + a.w > b.x and
            a.y < b.y + b.h and
            a.y + a.h > b.y)


def main():
    player = Player()
    bullets = []
    enemies = []
    score = 0
    shoot_timer = 0
    enemy_timer = 0
    running = True
    game_over = False
    base_bullet_count = 1
    base_enemy_spawn = 1

    while running:
        screen.fill(BLACK)
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.KEYDOWN:
                main()

        if not game_over:
            # 按键控制
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1
            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1
            player.move(dx, dy)

            # 计算当前弹道数量（每500分增加1个弹道）
            bullet_count = base_bullet_count + score // 500

            # 计算敌机速度倍数（每500分提高50%）
            speed_multiplier = 1.0 + (score // 500) * 0.5

            #计算每次生成的敌机数量
            enemy_spawn_count = base_enemy_spawn + (score // 500) * 2

            # 自动发射子弹
            shoot_timer += dt
            if shoot_timer > 250:
                # 根据弹道数量发射多发子弹
                if bullet_count == 1:
                    bullets.append(Bullet(player.x + 17, player.y))
                elif bullet_count == 2:
                    bullets.append(Bullet(player.x + 7, player.y))
                    bullets.append(Bullet(player.x + 27, player.y))
                elif bullet_count == 3:
                    bullets.append(Bullet(player.x + 17, player.y))
                    bullets.append(Bullet(player.x + 7, player.y))
                    bullets.append(Bullet(player.x + 27, player.y))
                else:
                    # 更多弹道时均匀分布
                    spacing = player.w / bullet_count
                    for i in range(bullet_count):
                        offset_x = player.x + spacing * i + (spacing - 6) / 2
                        bullets.append(Bullet(offset_x, player.y))
                shoot_timer = 0

            # 生成敌机
            enemy_timer += dt
            if enemy_timer > 800:
                for _ in range(enemy_spawn_count):
                    enemies.append(Enemy(speed_multiplier))
                enemy_timer = 0

            # 更新子弹
            for b in bullets[:]:
                b.update()
                if b.y < 0:
                    bullets.remove(b)

            # 更新敌机
            for e in enemies[:]:
                e.update()
                if e.y > HEIGHT:
                    enemies.remove(e)

            # 子弹击中敌机
            for b in bullets[:]:
                for e in enemies[:]:
                    if collide(b, e):
                        bullets.remove(b)
                        enemies.remove(e)
                        score += 20
                        break

            # 玩家撞敌机
            for e in enemies:
                if collide(player, e):
                    game_over = True
                    break

            # 绘制
            player.draw()
            for b in bullets:
                b.draw()
            for e in enemies:
                e.draw()

            # 分数和弹道信息
            font = pygame.font.Font(None, 30)
            text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(text, (10, 10))
            text2 = font.render(f"Bullets: {bullet_count}", True, WHITE)
            screen.blit(text2, (10, 40))
            text3 = font.render(f"Speed: {speed_multiplier:.1f}x", True, WHITE)
            screen.blit(text3, (10, 70))
            text4 = font.render(f"Enemies: {enemy_spawn_count}", True, WHITE)
            screen.blit(text4, (10, 100))
        else:
            font = pygame.font.Font(None, 40)
            tip1 = font.render(f"Game Over Score: {score}", True, WHITE)
            tip2 = font.render("Press any key to restart", True, WHITE)
            screen.blit(tip1, (40, 250))
            screen.blit(tip2, (40, 300))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
