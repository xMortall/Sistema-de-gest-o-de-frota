# @title Interface Gráfica para Gestão de Frota
# @version: 1.1
# @date: 2026-01-14
# @description:
# Faz a gestão de uma frota de veículos através de uma interface gráfica usando Pygame, agora com filtro por marca.
# @author: Emanuel Borges

from bibliotecas import pygame
from frota import Frota
from veiculo import Veiculo, CarroEletrico

pygame.init()


# ---------------- DECORATOR ----------------
def validar_campos(*campos_requeridos):
    """
    Decorator que verifica se os campos obrigatórios não estão vazios.
    Se algum estiver vazio, seta erro e interrompe a função.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for k in campos_requeridos:
                if self.texto[k] == "":
                    self.erro[k] = "Obrigatório"
                    return
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


# ---------------- CLASSE PRINCIPAL ----------------
class GestaoGUI:
    def __init__(self):
        # Janela
        self.LARGURA, self.ALTURA = 950, 550
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Gestão de Frota")
        self.fonte = pygame.font.SysFont(None, 24)

        # Dados
        self.frota = Frota()
        self.frota.carregar_inventario()
        self.lista_exibir = self.frota.veiculos

        # Campos
        self.campos = {
            "marca": pygame.Rect(40, 40, 150, 30),
            "modelo": pygame.Rect(200, 40, 150, 30),
            "preco": pygame.Rect(360, 40, 100, 30),
            "autonomia": pygame.Rect(470, 40, 100, 30),
        }
        self.texto = {k: "" for k in self.campos}
        self.erro = {k: "" for k in self.campos}
        self.campo_ativo = None
        self.eletrico = False
        self.desconto = False

        # Botões
        self.btao_add = pygame.Rect(600, 40, 140, 30)
        self.btao_exportar = pygame.Rect(750, 40, 140, 30)
        self.btao_filtrar = pygame.Rect(600, 90, 300, 30)

        # Filtro de marca
        self.filtro_ativo = False
        self.filtro_marca = ""

        # Lambdas para desenho
        self.desenhar_campo = lambda nome, rect: (
            pygame.draw.rect(self.tela, (200, 200, 200), rect, 2),
            self.escrever(nome.capitalize(), rect.x, rect.y - 18),
            self.escrever(self.texto[nome], rect.x + 5, rect.y + 5),
            self.escrever(self.erro[nome], rect.x, rect.y + 35, (255, 0, 0)) if self.erro[nome] else None
        )
        self.toggle_checkbox = lambda rect, estado, e: not estado if e.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(pygame.mouse.get_pos()) else estado

    # ---------------- FUNÇÕES ----------------
    def escrever(self, txt, x, y, cor=(255, 255, 255)):
        self.tela.blit(self.fonte.render(txt, True, cor), (x, y))

    def desenhar_checkbox(self, rect, ativo, label):
        pygame.draw.rect(self.tela, (255, 255, 255), rect, 2)
        if ativo:
            pygame.draw.line(self.tela, (0, 255, 0), (rect.x + 3, rect.y + 10), (rect.x + 10, rect.y + 17), 3)
            pygame.draw.line(self.tela, (0, 255, 0), (rect.x + 10, rect.y + 17), (rect.x + 22, rect.y + 3), 3)
        self.escrever(label, rect.x + 30, rect.y + 2)

    @validar_campos("marca", "modelo", "preco")
    def adicionar_veiculo(self):
        # Reset erros
        for k in self.erro:
            self.erro[k] = ""

        try:
            preco = float(self.texto["preco"])
        except:
            self.erro["preco"] = "Número inválido"
            return

        if self.eletrico:
            try:
                autonomia = int(self.texto["autonomia"])
            except:
                self.erro["autonomia"] = "Obrigatório (número)"
                return
            if self.desconto:
                autonomia = int(autonomia * 1.1)
            v = CarroEletrico(self.texto["marca"], preco, self.texto["modelo"], autonomia)
        else:
            v = Veiculo(self.texto["marca"], preco, self.texto["modelo"])

        if self.desconto:
            v.preco *= 0.9
            v.com_desconto = True

        self.frota.adicionar_veiculo(v)
        for k in self.texto:
            self.texto[k] = ""

        self.filtrar_por_marca()  # Atualiza a lista caso algum filtro esteja ativo

    # filtra a lista de veículos pela marca
    def filtrar_por_marca(self):
        if self.filtro_marca.strip() == "":
            self.lista_exibir = self.frota.veiculos
        else:
            self.lista_exibir = [v for v in self.frota.veiculos if v.marca.lower() == self.filtro_marca.lower()]

    # desenha a lista de veículos na tela
    def desenhar_lista(self):
        y = 200
        for v in self.lista_exibir[-10:]:
            self.escrever(str(v), 40, y)
            botao_x = pygame.Rect(880, y, 25, 25)
            pygame.draw.rect(self.tela, (200, 60, 60), botao_x)
            self.escrever("X", 888, y)
            yield botao_x, v
            y += 30

    # ---------------- LOOP PRINCIPAL ----------------
    def run(self):
        running = True
        while running:
            self.tela.fill((30, 30, 30))

            # Desenhar campos
            for nome, rect in self.campos.items():
                self.desenhar_campo(nome, rect)

            # Checkboxes
            chk_eletrico = pygame.Rect(40, 90, 20, 20)
            chk_desconto = pygame.Rect(200, 90, 20, 20)
            self.desenhar_checkbox(chk_eletrico, self.eletrico, "Elétrico")
            self.desenhar_checkbox(chk_desconto, self.desconto, "Desconto 10%")

            # Botões
            pygame.draw.rect(self.tela, (100, 160, 220), self.btao_add)
            self.escrever("Adicionar", self.btao_add.x + 20, self.btao_add.y + 8)
            pygame.draw.rect(self.tela, (100, 160, 220), self.btao_exportar)
            self.escrever("Exportar", self.btao_exportar.x + 25, self.btao_exportar.y + 8)
            pygame.draw.rect(self.tela, (100, 160, 220), self.btao_filtrar)
            self.escrever("Filtrar por Marca", self.btao_filtrar.x + 10, self.btao_filtrar.y + 8)

            # Campo de filtro ativo
            if self.filtro_ativo:
                filtro_rect = pygame.Rect(600, 130, 200, 30)
                pygame.draw.rect(self.tela, (200, 200, 200), filtro_rect, 2)
                self.escrever(self.filtro_marca, filtro_rect.x + 5, filtro_rect.y + 5)
                self.escrever("Digite a marca e pressione Enter", filtro_rect.x, filtro_rect.y - 20, (180, 180, 180))

            # Lista de veículos
            botoes_x = list(self.desenhar_lista())

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                # Clique do mouse
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.campo_ativo = None
                    for k, r in self.campos.items():
                        if r.collidepoint(e.pos):
                            self.campo_ativo = k

                    self.eletrico = self.toggle_checkbox(chk_eletrico, self.eletrico, e)
                    self.desconto = self.toggle_checkbox(chk_desconto, self.desconto, e)

                    if self.btao_add.collidepoint(e.pos):
                        self.adicionar_veiculo()

                    if self.btao_exportar.collidepoint(e.pos):
                        self.frota.exportar_inventario()
                        print("Inventário exportado com sucesso!")

                    if self.btao_filtrar.collidepoint(e.pos):
                        self.filtro_ativo = True
                        self.filtro_marca = ""

                    for bx, v in botoes_x:
                        if bx.collidepoint(e.pos):
                            self.frota.remover_veiculo(v)
                            self.filtrar_por_marca()

                # Digitação
                if e.type == pygame.KEYDOWN:
                    if self.filtro_ativo:
                        if e.key == pygame.K_RETURN:
                            self.filtro_ativo = False
                            self.filtrar_por_marca()
                        elif e.key == pygame.K_BACKSPACE:
                            self.filtro_marca = self.filtro_marca[:-1]
                        else:
                            self.filtro_marca += e.unicode
                    elif self.campo_ativo:
                        if e.key == pygame.K_BACKSPACE:
                            self.texto[self.campo_ativo] = self.texto[self.campo_ativo][:-1]
                        else:
                            self.texto[self.campo_ativo] += e.unicode

        pygame.quit()