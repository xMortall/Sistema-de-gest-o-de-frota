# @title Gestão da Frota
# @version: 1.0
# @date: 2026-01-7
# @description:
# Define a classe frota com métodos para adicionar veículos.
# @author: Emanuel Borges


from decorador import log_operacao
from veiculo import Veiculo, CarroEletrico

# Classe frota para gerenciar veículos
class Frota:
    def __init__(self):
        self.veiculos = []              # Lista para armazenar os veículos na frota


    # adiciona veículo à frota
    @log_operacao
    def adicionar_veiculo(self, veiculo):
        self.veiculos.append(veiculo)  # Adiciona um veículo à frota


    # remove veículo da frota
    @log_operacao
    def remover_veiculo(self, veiculo):
        self.veiculos.remove(veiculo)  # Remove um veículo da frota

    # lista veículos por marca
    def listar_veiculos(self, marca):
        return [v for v in self.veiculos if v.marca.lower() == marca.lower()]         # Retorna a lista de veículos na frota
    
    # aplica desconto a todos os veículos
    def aplicar_descontos(self, percentagem):
        desconto = lambda preco: preco * (1 - percentagem / 100)  # Função lambda para calcular o preço com desconto
        for v in self.veiculos:
            v.preco = desconto(v.preco)                           # Aplica o desconto ao preço de cada veículo na frota
            v.com_desconto = True                                 # Marca o veículo como tendo desconto aplicado

    # função para exportar inventário para um arquivo
    def exportar_inventario(self):
        with open('inventario_frota.txt', 'w') as f:
            for v in self.veiculos:
                f.write(str(v) + '\n')                            # Exporta o inventário da frota para um arquivo de texto

    # função para carregar inventário de um arquivo
    def carregar_inventario(self):
        try:
            with open('inventario_frota.txt', 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    # Exemplo de linha: Marca | Modelo | 15000.00€ | 400 km | 08/01/2026 14:22 [DESCONTO] [ELÉTRICO]
                    partes = linha.split('|')
                    marca = partes[0].strip()
                    modelo = partes[1].strip()
                    preco = float(partes[2].strip().replace('€','').replace('[DESCONTO]','').strip())
                    
                    # Verificar se é elétrico e pegar autonomia
                    if '[ELÉTRICO]' in linha:
                        # autonomia está na terceira parte: 400 km
                        autonomia = int(partes[4].strip().split()[0])
                        veiculo = CarroEletrico(marca, preco, modelo, autonomia)
                    else:
                        veiculo = Veiculo(marca, preco, modelo)
                    
                    # Verificar desconto
                    if '[DESCONTO]' in linha:
                        veiculo.com_desconto = True
                    
                    self.veiculos.append(veiculo)
        except FileNotFoundError:
            # Se não existir arquivo, começa vazio
            pass
