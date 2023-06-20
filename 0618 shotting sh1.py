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

#배경 음악 로드
#pygame.mixer.music.load(os.path.join(assets_path, 'music.wav'))
#pygame.mixer.music.play(-1) #무한반복 재생

#효과음 로드
#sound = pygame.mixer.Sound(os.path.join(assets_path, 'missile.wav'))

# 게임 종료 전까지 반복
done = False
while not done:
    #이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #배경 이미지 그리기
    screen.blit(background_image, background_image.get_rect())

    # 화면 업데이트
    pygame.display.flip()

    #초당 60 프레임으로 업데이트
    clock.tick(FPS)

pygame.quit()