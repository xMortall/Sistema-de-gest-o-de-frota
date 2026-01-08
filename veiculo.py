# @title Veículo e Carro Elétrico
# @version: 1.0
# @date: 2026-01-7
# @description:
# Define a classe Veiculo com atributos marca, preco e modelo
# e um método __str__ para representar o veículo como uma string.
# Define a classe CarroEletrico que herda de Veiculo, adicionando o atributo autonomia
# e sobrescrevendo o método __str__ para incluir a autonomia na representação.
# @author: Emanuel Borges

from bibliotecas import datetime


# classe Veiculo com atributos marca, preco e modelo
class Veiculo:
    def __init__ (self, marca, preco, modelo):
        self.marca = marca                      # define o atributo marca
        self.preco = preco                      # define o atributo preco
        self.modelo = modelo                    # define o atributo modelo
        self.data_adicao = datetime.datetime.now()    # define a data de adição do veículo
        self.com_desconto = False               # indica se o veículo tem desconto aplicado

    # método __str__ para representar o veículo como uma string
    def __str__(self):
        desconto = " [DESCONTO]" if self.com_desconto else ""
        data = self.data_adicao.strftime("%d/%m/%Y %H:%M")
        return f"{self.marca} | {self.modelo} | {self.preco:.2f}€ | {data}{desconto}"

# classe CarroEletrico que herda de Veiculo e adiciona o atributo autonomia
class CarroEletrico(Veiculo):
    def __init__(self, marca, preco, modelo, autonomia):
        super().__init__(marca, preco, modelo)  # chama o construtor da classe base Veiculo
        self.autonomia = autonomia              # define o atributo autonomia

    # sobrescreve o método __str__ para incluir a autonomia na representação
    def __str__(self):
        desconto = " [DESCONTO]" if self.com_desconto else ""
        data = self.data_adicao.strftime("%d/%m/%Y %H:%M")
        eletrico = " [ELÉTRICO]"  # marca elétrica
        return (
            f"{self.marca} | {self.modelo} | {self.preco:.2f}€ | "
            f"{self.autonomia} km | {data}{desconto}{eletrico}"
        )
