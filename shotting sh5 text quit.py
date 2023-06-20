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
    #전투기 충돌
    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 미사일 객체
class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Missile, self).__init__()
        self.image = pygame.image.load(os.path.join(assets_path,'missile.png'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    # 미사일 업데이트
    def update(self):
        self.rect.y = self.rect.y -  self.speed
        if self.rect.y + self.rect.height < 0 :
            self.kill()

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
# 암석 객체
class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        self.image = pygame.image.load(os.path.join(assets_path,'rock10.png')) #pygame.image.load(choice_rock_path)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    # 암석 업데이트
    def update(self):
        self.rect.y += self.speed

    # 암석 게임 화면
    def out_of_screen(self):
        if self.rect.y > SCREEN_HEIGHT:
            return True

#게임 객체
class Game():
    def __init__(self):
        self.fighter = Fighter()

        self.missiles = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()

        self.shot_count = 0

    def display_frame(self,screen):
        screen.blit(background_image, background_image.get_rect()) #배경이미지를 이쪽으로 위치함
        self.fighter.update()
        self.fighter.draw(screen)
        # 미사일 추가
        self.missiles.update()
        self.missiles.draw(screen)
        # 암석 추가
        self.rocks.update()
        self.rocks.draw(screen)
        # shot count 출력
        font = pygame.font.SysFont('malgungothic', 30)
        text = font.render(" 점수 : " + str(self.shot_count), True, (255, 255, 255))
        screen.blit(text, (0, 0))

    def run_logic(self, screen):
        # 랜덤 확률의 빈도로 수행
        if random.randint(1, 50) == 1:
            # 운석 생성 및 생성된 운석만큼 점수 증가i
            rock = Rock(random.randint(0, SCREEN_WIDTH - 30), 0, 1) #speed=1
            self.rocks.add(rock)

        for missile in self.missiles:
            rock = missile.collide(self.rocks) #missile collide 추가
            if rock:
                self.shot_count+=1
                print(self.shot_count)
                missile.kill()
                rock.kill()

        for rock in self.rocks:
            if rock.out_of_screen():
                rock.kill()
        #암석 출돌시 끝남
        if self.fighter.collide(self.rocks):   # fighter collide 추가
            sleep(1)
            pygame.quit()

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
                elif event.key == pygame.K_SPACE:   # 미사일 발사 이벤트
                    missile = Missile(self.fighter.rect.centerx, self.fighter.rect.y, 10)
                    self.missiles.add(missile)

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
    # 암석 런로직
    game.run_logic(screen)

    # 화면 업데이트
    pygame.display.flip()

    #초당 60 프레임으로 업데이트
    clock.tick(FPS)

pygame.quit()