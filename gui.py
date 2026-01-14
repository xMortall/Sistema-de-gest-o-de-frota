# @title Interface Gráfica para Gestão de Frota
# @version: 1.0
# @date: 2026-01-8
# @description:
# Faz a gestão de uma frota de veículos através de uma interface gráfica usando Pygame.
# @author: Emanuel Borges

from bibliotecas import pygame
from frota import Frota
from veiculo import Veiculo, CarroEletrico

pygame.init()

# ---------------- JANELA ----------------
LARGURA, ALTURA = 950, 550
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Gestão de Frota")
fonte = pygame.font.SysFont(None, 24)

# ---------------- DADOS ----------------
frota = Frota()
frota.carregar_inventario()     # LÊ O FICHEIRO AO INICIAR
lista_exibir = frota.veiculos

# ---------------- CAMPOS ----------------
campos = {
    "marca": pygame.Rect(40, 40, 150, 30),
    "modelo": pygame.Rect(200, 40, 150, 30),
    "preco": pygame.Rect(360, 40, 100, 30),
    "autonomia": pygame.Rect(470, 40, 100, 30),
}

texto = {k: "" for k in campos}
erro = {k: "" for k in campos}

campo_ativo = None
eletrico = False
desconto = False

# ---------------- BOTÕES ----------------
btao_add = pygame.Rect(600, 40, 140, 30)
btao_exportar = pygame.Rect(750, 40, 140, 30)

# ---------------- FUNÇÕES ----------------
def escrever(txt, x, y, cor=(255,255,255)):
    tela.blit(fonte.render(txt, True, cor), (x, y))

def desenhar_checkbox(rect, ativo, label):
    pygame.draw.rect(tela, (255,255,255), rect, 2)
    if ativo:
        pygame.draw.line(tela, (0,255,0), (rect.x+3, rect.y+10), (rect.x+10, rect.y+17), 3)
        pygame.draw.line(tela, (0,255,0), (rect.x+10, rect.y+17), (rect.x+22, rect.y+3), 3)
    escrever(label, rect.x + 30, rect.y + 2)

def adicionar_veiculo():
    global texto, erro

    for k in erro:
        erro[k] = ""

    if texto["marca"] == "":
        erro["marca"] = "Obrigatório"
        return

    if texto["modelo"] == "":
        erro["modelo"] = "Obrigatório"
        return

    try:
        preco = float(texto["preco"])
    except:
        erro["preco"] = "Número inválido"
        return

    if eletrico:
        try:
            autonomia = int(texto["autonomia"])
        except:
            erro["autonomia"] = "Obrigatório (número)"
            return

        # CÁLCULO DA AUTONOMIA
        if desconto:
            autonomia = int(autonomia * 1.1)

        v = CarroEletrico(texto["marca"], preco, texto["modelo"], autonomia)
    else:
        v = Veiculo(texto["marca"], preco, texto["modelo"])

    if desconto:
        v.preco *= 0.9
        v.com_desconto = True

    frota.adicionar_veiculo(v)

    for k in texto:
        texto[k] = ""

def desenhar_lista():
    y = 150
    for v in lista_exibir[-10:]:
        escrever(str(v), 40, y)
        botao_x = pygame.Rect(880, y, 25, 25)
        pygame.draw.rect(tela, (200,60,60), botao_x)
        escrever("X", 888, y)
        yield botao_x, v
        y += 30

# ---------------- LOOP ----------------
running = True
while running:
    tela.fill((30,30,30))

    # Campos
    for nome, rect in campos.items():
        pygame.draw.rect(tela, (200,200,200), rect, 2)
        escrever(nome.capitalize(), rect.x, rect.y - 18)
        escrever(texto[nome], rect.x + 5, rect.y + 5)
        if erro[nome]:
            escrever(erro[nome], rect.x, rect.y + 35, (255,0,0))

    # Checkboxes
    chk_eletrico = pygame.Rect(40, 90, 20, 20)
    chk_desconto = pygame.Rect(200, 90, 20, 20)
    desenhar_checkbox(chk_eletrico, eletrico, "Elétrico")
    desenhar_checkbox(chk_desconto, desconto, "Desconto 10%")

    # Botões
    pygame.draw.rect(tela, (100,160,220), btao_add)
    escrever("Adicionar", btao_add.x + 20, btao_add.y + 8)

    pygame.draw.rect(tela, (100,160,220), btao_exportar)
    escrever("Exportar", btao_exportar.x + 25, btao_exportar.y + 8)

    # Lista
    botoes_x = list(desenhar_lista())

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            campo_ativo = None
            for k, r in campos.items():
                if r.collidepoint(e.pos):
                    campo_ativo = k

            if chk_eletrico.collidepoint(e.pos):
                eletrico = not eletrico

            if chk_desconto.collidepoint(e.pos):
                desconto = not desconto

            if btao_add.collidepoint(e.pos):
                adicionar_veiculo()

            if btao_exportar.collidepoint(e.pos):
                frota.exportar_inventario()

            for bx, v in botoes_x:
                if bx.collidepoint(e.pos):
                    frota.remover_veiculo(v)

        if e.type == pygame.KEYDOWN and campo_ativo:
            if e.key == pygame.K_BACKSPACE:
                texto[campo_ativo] = texto[campo_ativo][:-1]
            else:
                texto[campo_ativo] += e.unicode

pygame.quit()
