# @title Gestão da Frota
# @version: 1.0
# @date: 2026-01-7
# @description:
# Define a classe frota com métodos para adicionar veículos.
# @author: Emanuel Borges


from decorador import log_operacao

# Classe frota para gerenciar veículos
class frota:
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
    
    def aplicar_descontos(self, percentagem):
        desconto = lambda preco: preco * (1 - percentagem / 100)  # Função lambda para calcular o preço com desconto
        for v in self.veiculos:
            v.preco = desconto(v.preco)                           # Aplica o desconto ao preço de cada veículo na frota

    def exportar_inventario(self):
        with open('inventario_frota.txt', 'w') as f:
            for v in self.veiculos:
                f.write(str(v) + '\n')                            # Exporta o inventário da frota para um arquivo de texto