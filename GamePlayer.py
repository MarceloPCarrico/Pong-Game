import pygame
from pygame.locals import *

pygame.init()

LARGURA, ALTURA = 1200, 800

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Pong Game')

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

font = pygame.font.SysFont(None, 55)

# definir imagem e tamanho da bola
bola_raio = 20
bola_imagem = pygame.image.load("bola2.png")
bola_imagem = pygame.transform.scale(bola_imagem, (bola_raio * 2, bola_raio * 2))
bola_mask = pygame.mask.from_surface(bola_imagem)
bola_pos = [600, 400]
bola_velocidade = [10, 10]

velocidade = 10
# definir circulo e linha do centro do campo
centro_campo = [600, 400]
centro_campoRaio = 25
meio_campo = pygame.Rect(600, 50, 5, 700)

# Carregar imagens dos jogadores
blue_player = pygame.image.load("BluePlayer.png")
green_player = pygame.image.load("GreenPlayer.png")
blue_player = pygame.transform.scale(blue_player, (100, 100))
green_player = pygame.transform.scale(green_player, (100, 100))

# Defina a posição inicial dos jogadores
posicao_blue_player = pygame.Rect(1100, 600, 100, 100)
posicao_green_player = pygame.Rect(25, 50, 100, 100)

# Inicialize os pontos do score para ambos os jogadores
score_branco = 0
score_vermelho = 0

rodando = True
golo = False
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # definir teclas de jogo
    teclas = pygame.key.get_pressed()
    if teclas[K_i] and posicao_blue_player.top > 0:
        posicao_blue_player.y -= velocidade
    if teclas[K_k] and posicao_blue_player.bottom < 800:
        posicao_blue_player.y += velocidade
    if teclas[K_w] and posicao_green_player.top > 0:
        posicao_green_player.y -= velocidade
    if teclas[K_s] and posicao_green_player.bottom < 800:
        posicao_green_player.y += velocidade

    # atualizar posição da bola
    bola_pos[0] += bola_velocidade[0]
    bola_pos[1] += bola_velocidade[1]

    # verificar colisão com limites da tela
    if bola_pos[1] - bola_raio <= 0 or bola_pos[1] + bola_raio >= 800:
        bola_velocidade[1] = -bola_velocidade[1]

    # Verificar colisão com os jogadores
    blue_player_mask = pygame.mask.from_surface(blue_player)
    green_player_mask = pygame.mask.from_surface(green_player)
    
    # colisão bola com jogadores
    if blue_player_mask.overlap(bola_mask, (int(bola_pos[0] - bola_raio - posicao_blue_player.x), int(bola_pos[1] - bola_raio - posicao_blue_player.y))):
        bola_velocidade[0] = -bola_velocidade[0]
    if green_player_mask.overlap(bola_mask, (int(bola_pos[0] - bola_raio - posicao_green_player.x), int(bola_pos[1] - bola_raio - posicao_green_player.y))):
        bola_velocidade[0] = -bola_velocidade[0]

    if bola_pos[0] - bola_raio <= 0:
        # Jogador vermelho marcou ponto
        score_vermelho += 1
        golo = True
    elif bola_pos[0] + bola_raio >= 1200:
        # Jogador branco marcou ponto
        score_branco += 1
        golo = True

    if golo:
        mensagem = font.render("GOLOOOO!", True, BRANCO)
        tela.blit(mensagem, (LARGURA // 2 - mensagem.get_width() // 2, ALTURA // 2 - mensagem.get_height() // 2))

        # Resetar a posição da bola após um golo e retomar o jogo
        bola_pos = [LARGURA // 2, ALTURA // 2]
        bola_velocidade = [10, 10]
        pygame.display.flip()
        pygame.time.delay(1000)  # Espera 1 segundo antes de continuar

        golo = False  # Reinicia o estado de golo

    tela.fill(PRETO)
    tela.blit(bola_imagem, (int(bola_pos[0] - bola_raio), int(bola_pos[1] - bola_raio)))

    pygame.draw.circle(tela, BRANCO, centro_campo, centro_campoRaio)
    pygame.draw.rect(tela, BRANCO, meio_campo)
    tela.blit(blue_player, (posicao_blue_player.x, posicao_blue_player.y))
    tela.blit(green_player, (posicao_green_player.x, posicao_green_player.y))

    # Exibir o placar no topo da tela
    texto_score = font.render(f"{score_branco} - {score_vermelho}", True, BRANCO)
    tela.blit(texto_score, (LARGURA // 2 - texto_score.get_width() // 2, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
