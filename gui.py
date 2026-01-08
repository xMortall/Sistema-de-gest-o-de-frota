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

# Usado para logar ações da GUI
def log_acao(func):
    """Decorador para logar ações da GUI"""
    def wrapper(*args, **kwargs):
        print(f"[LOG] Executando: {func.__name__}")
        resultado = func(*args, **kwargs)
        return resultado
    return wrapper

# --- Função principal do GUI ---
def executar_gui():
    # --- Configurações da janela ---
    LARGURA, ALTURA = 950, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Gestão de Frota")
    fonte = pygame.font.SysFont(None, 24)
    
    frota = Frota()

    # --- Carregar inventário ---
    @log_acao
    def carregar_inventario():
        try:
            with open('inventario_frota.txt', 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    partes = linha.split('|')
                    marca = partes[0].strip()
                    modelo = partes[1].strip()
                    preco = float(partes[2].strip().replace('€','').replace('[DESCONTO]','').strip())
                    if '[ELÉTRICO]' in linha:
                        autonomia = int(partes[3].strip().split()[0])
                        veiculo = CarroEletrico(marca, preco, modelo, autonomia)
                    else:
                        veiculo = Veiculo(marca, preco, modelo)
                    if '[DESCONTO]' in linha:
                        veiculo.com_desconto = True
                    frota.veiculos.append(veiculo)
        except FileNotFoundError:
            pass

    carregar_inventario()

    # --- Variáveis ---
    campos = {                              # Campos de entrada
        "marca": {"rect": pygame.Rect(40, 40, 150, 30), "texto": "", "erro": ""},
        "modelo": {"rect": pygame.Rect(200, 40, 150, 30), "texto": "", "erro": ""},
        "preco": {"rect": pygame.Rect(360, 40, 100, 30), "texto": "", "erro": ""},
        "autonomia": {"rect": pygame.Rect(470, 40, 100, 30), "texto": "", "erro": ""},
    }
    campo_ativo = None                      # Guarda o campo atualmente ativo
    eletrico = False                        # Indica se o veículo é elétrico
    lista_botoes = []                       # Botões de remoção na lista
    lista_exibir = frota.veiculos.copy()    # Lista de veículos a exibir
    pop_up_ativo = False                    # Indica se o pop-up de filtro está ativo
    marca_filtro = ""                       # Marca para filtrar
    ultimo_adicionado = None                # Guarda referência do último veículo adicionado

    botoes = {                              # Botões da interface
        "Adicionar": pygame.Rect(720, 40, 120, 30),
        "Aplicar Desconto": pygame.Rect(40, 90, 150, 30),
        "Exportar": pygame.Rect(200, 90, 150, 30),
        "Mostrar Todos": pygame.Rect(360, 90, 150, 30),
        "Filtrar Marca": pygame.Rect(520, 90, 180, 30),
    }

    # --- Funções de desenho reutilizáveis ---
    def desenhar_texto(texto, pos, cor=(255, 255, 255)):
        tela.blit(fonte.render(texto, True, cor), pos)

    def desenhar_campo(nome, campo, ativo):
        cor = (0, 200, 0) if ativo == nome else (180, 180, 180)
        pygame.draw.rect(tela, cor, campo["rect"], 2, border_radius=5)
        desenhar_texto(nome.capitalize() + ":", (campo["rect"].x, campo["rect"].y - 20))
        desenhar_texto(campo["texto"], (campo["rect"].x + 5, campo["rect"].y + 5))
        if campo["erro"]:
            desenhar_texto(campo["erro"], (campo["rect"].x, campo["rect"].y + 35), (255, 100, 100))

    def desenhar_checkbox(eletrico):
        rect = pygame.Rect(580, 40, 20, 20)
        pygame.draw.rect(tela, (255, 255, 255), rect, 2)
        if eletrico:
            pygame.draw.line(tela, (0, 255, 0), (582, 50), (588, 58), 3)
            pygame.draw.line(tela, (0, 255, 0), (588, 58), (600, 40), 3)
        desenhar_texto("É elétrico", (610, 38))
        return rect

    def desenhar_botao(rect, texto):
        cor_base = (100, 160, 220)
        cor_hover = (70, 200, 250)
        cor = cor_hover if rect.collidepoint(pygame.mouse.get_pos()) else cor_base
        pygame.draw.rect(tela, cor, rect, border_radius=8)
        desenhar_texto(texto, (rect.x + 5, rect.y + 5), (0,0,0))

    def desenhar_lista():
        y = 150
        lista_botoes.clear()
        for v in lista_exibir[-10:]:
            ret_fundo = pygame.Rect(35, y - 2, 880, 28)
            pygame.draw.rect(tela, (50, 50, 50), ret_fundo, border_radius=5)
            desenhar_texto(str(v), (40, y))
            botao_x = pygame.Rect(860, y, 25, 25)
            pygame.draw.rect(tela, (200, 60, 60), botao_x, border_radius=5)
            desenhar_texto("X", (867, y))
            lista_botoes.append((botao_x, v))
            y += 30

    def desenhar_popup():
        nonlocal marca_filtro
        rect = pygame.Rect(300, 200, 350, 120)
        pygame.draw.rect(tela, (60, 60, 60), rect, border_radius=8)
        pygame.draw.rect(tela, (255, 255, 255), rect, 2, border_radius=8)
        desenhar_texto("Digite a marca para filtrar:", (310, 210))
        input_rect = pygame.Rect(310, 240, 330, 30)
        pygame.draw.rect(tela, (180, 180, 180), input_rect, 2, border_radius=5)
        desenhar_texto(marca_filtro, (input_rect.x + 5, input_rect.y + 5))
        return input_rect

    # --- Funções de ações ---
    @log_acao
    def adicionar_veiculo():
        nonlocal lista_exibir, ultimo_adicionado
        for c in campos.values():
            c["erro"] = ""
        if not campos["marca"]["texto"]:
            campos["marca"]["erro"] = "Marca obrigatória!"
            return
        if not campos["modelo"]["texto"]:
            campos["modelo"]["erro"] = "Modelo obrigatório!"
            return
        # Preço
        try:
            preco = float(campos["preco"]["texto"])
        except ValueError:
            campos["preco"]["erro"] = "Número inválido!"
            return
        # Autonomia se elétrico
        if eletrico:
            try:
                autonomia = int(campos["autonomia"]["texto"])
            except ValueError:
                campos["autonomia"]["erro"] = "Digite inteiro!"
                return
            veiculo = CarroEletrico(campos["marca"]["texto"], preco, campos["modelo"]["texto"], autonomia)
        else:
            veiculo = Veiculo(campos["marca"]["texto"], preco, campos["modelo"]["texto"])
        frota.adicionar_veiculo(veiculo)
        ultimo_adicionado = veiculo  # Guarda referência do último carro adicionado
        for c in campos.values():
            c["texto"] = ""
        lista_exibir = frota.veiculos.copy()

    @log_acao
    def aplicar_desconto():
        nonlocal lista_exibir
        if ultimo_adicionado:
            ultimo_adicionado.preco *= 0.9
            ultimo_adicionado.com_desconto = True
        lista_exibir = frota.veiculos.copy()

    @log_acao
    def exportar():
        frota.exportar_inventario()

    # --- Loop principal ---
    running = True
    while running:
        tela.fill((25, 25, 25))

        # Desenhar tudo
        for nome, campo in campos.items():
            desenhar_campo(nome, campo, campo_ativo)
        checkbox_rect = desenhar_checkbox(eletrico)
        for nome, rect in botoes.items():
            desenhar_botao(rect, nome)
        desenhar_lista()
        if pop_up_ativo:
            input_rect = desenhar_popup()

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            # Clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Ativar campo
                campo_ativo = None
                if pop_up_ativo and input_rect.collidepoint(evento.pos):
                    campo_ativo = "popup"
                else:
                    for nome, campo in campos.items():
                        if campo["rect"].collidepoint(evento.pos):
                            campo_ativo = nome
                            campo["erro"] = ""

                # Checkbox elétrico
                if checkbox_rect.collidepoint(evento.pos):
                    eletrico = not eletrico

                # Botões
                if botoes["Adicionar"].collidepoint(evento.pos):
                    adicionar_veiculo()
                if botoes["Aplicar Desconto"].collidepoint(evento.pos):
                    aplicar_desconto()
                if botoes["Exportar"].collidepoint(evento.pos):
                    exportar()
                if botoes["Mostrar Todos"].collidepoint(evento.pos):
                    lista_exibir = frota.veiculos.copy()
                if botoes["Filtrar Marca"].collidepoint(evento.pos):
                    pop_up_ativo = True
                    marca_filtro = ""

                # Remover veículo
                for botao_x, veiculo in lista_botoes:
                    if botao_x.collidepoint(evento.pos):
                        frota.remover_veiculo(veiculo)
                        lista_exibir = [v for v in lista_exibir if v != veiculo]
                        if veiculo == ultimo_adicionado:
                            ultimo_adicionado = None
                        break

            # Digitação de texto
            if evento.type == pygame.KEYDOWN:
                if campo_ativo == "popup":
                    if evento.key == pygame.K_RETURN:
                        lista_exibir = frota.listar_veiculos(marca_filtro)
                        pop_up_ativo = False
                        marca_filtro = ""
                        campo_ativo = None
                    elif evento.key == pygame.K_BACKSPACE:
                        marca_filtro = marca_filtro[:-1]
                    elif len(evento.unicode) == 1:
                        marca_filtro += evento.unicode
                elif campo_ativo in campos:
                    if evento.key == pygame.K_BACKSPACE:
                        campos[campo_ativo]["texto"] = campos[campo_ativo]["texto"][:-1]
                    elif len(evento.unicode) == 1:
                        campos[campo_ativo]["texto"] += evento.unicode

                    # Preencher automaticamente modelo
                    if campo_ativo == "marca":
                        marca_digitada = campos["marca"]["texto"]
                        modelos = [v.modelo for v in frota.veiculos if v.marca.lower() == marca_digitada.lower()]
                        if modelos:
                            campos["modelo"]["texto"] = modelos[-1]

    pygame.quit()
