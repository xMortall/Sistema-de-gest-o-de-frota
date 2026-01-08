# @title Decorador de Log de Operações
# @version: 1.0
# @date: 2026-01-7
# @description:
# Define um decorador para registrar operações em métodos.
# @author: Emanuel Borges


from bibliotecas import datetime

def log_operacao(funcao):
    def wrapper(*args, **kwargs):
        agora = datetime.datetime.now()
        print(f"[{agora}] A executar: {funcao.__name__}")
        return funcao(*args, **kwargs)
    return wrapper
