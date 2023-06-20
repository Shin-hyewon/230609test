import pygame
import os
import sys
import random
from time import sleep

# 게임 스크린 크기
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 전역 변수
FPS = 60

# pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption('Shooting Game SHW')

# 스크린 정의
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

#assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

#배경 이미지 로드
background_image= pygame.image.load(os.path.join(assets_path, 'background.png'))

# 전투기 객체
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super(Fighter, self).__init__()
        self.image = pygame.image.load(os.path.join(assets_path, 'fighter.png'))
        self.rect=self.image.get_rect()
        self.reset()

    # 전투기 리셋
    def reset(self):
        self.rect.x = int(SCREEN_WIDTH / 2) # 전투기의  x 위치를 가로사이즈의 1/2 지점으로
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0

    # 전투기 업데이트
    def update(self):
        self.rect.x = self.rect.x + self.dx
        self.rect.y = self.rect.y + self.dy

        if self.rect.x < 0 or self.rect.x + self.rect.width > SCREEN_WIDTH:
            self.rect.x -= self.dx

        if self.rect.y < 0 or self.rect.y + self.rect.height > SCREEN_HEIGHT:
            self.rect.y -= self.dy

    # 전투기 그리기
    def draw(self, screen):
        screen.blit(self.image, self.rect)

#게임 객체
class Game():
    def __init__(self):
        self.fighter = Fighter()
    def display_frame(self,screen):
        screen.blit(background_image, background_image.get_rect()) #배경이미지를 이쪽으로 위치함
        self.fighter.update()
        self.fighter.draw(screen)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if  event.key == pygame.K_LEFT:
                    self.fighter.dx =self.fighter.dx-1
                elif event.key == pygame.K_RIGHT:
                    self.fighter.dx =self.fighter.dx+1
                elif event.key == pygame.K_UP:
                    self.fighter.dy =self.fighter.dy-1
                elif event.key == pygame.K_DOWN:
                    self.fighter.dy =self.fighter.dy+1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    self.fighter.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                    self.fighter.dy = 0

game=Game()

# 게임 종료 전까지 반복
done = False
while not done:
    #이벤트 반복 구간
    done = game.process_events()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    #게임 로직 구간
    game.display_frame(screen)

    #배경 이미지 그리기
    #screen.blit(background_image, background_image.get_rect())

    # 화면 업데이트
    pygame.display.flip()

    #초당 60 프레임으로 업데이트
    clock.tick(FPS)

pygame.quit()