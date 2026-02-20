import re
import secrets
import string
from random import shuffle
from typing import Tuple


class PasswordService:

    @staticmethod
    def gerar_senha(tamanho: int=10,
                    maiusculas: bool=True,
                    minusculas: bool=True,
                    digitos: bool=True,
                    simbolos: bool=True,
                    remover_confusos: bool=True) -> str:
        espaco = ""
        senha = []
        if maiusculas:
            valores = string.ascii_uppercase if not remover_confusos\
                                            else "ABCDEFGHJKLMNPRSTUVWXYZ"
            espaco += valores
            senha.append(secrets.choice(valores))
            tamanho -= 1
        if minusculas:
            valores = string.ascii_lowercase if not remover_confusos\
                                             else "abcdefghjkmnpqrstuvwxyz"
            espaco += valores
            senha.append(secrets.choice(valores))
            tamanho -= 1
        if digitos:
            valores = "0123456789" if not remover_confusos\
                                   else "23456789"
            espaco += valores
            senha.append(secrets.choice(valores))
            tamanho -= 1
        if simbolos:
            valores = string.punctuation if not remover_confusos \
                                         else "@#$%&*-+=[]^:?/"
            espaco += valores
            senha.append(secrets.choice(valores))
            tamanho -= 1
        for _ in range(tamanho):
            senha.append(secrets.choice(espaco))
        shuffle(senha)
        return "".join(senha)

    @staticmethod
    def validar_complexidade_senha(senha: str = None,
                                   tamanho: int = 8,
                                   maiusculas: bool = True,
                                   minusculas: bool = True,
                                   digitos: bool = True,
                                   simbolos: bool = True) -> Tuple[bool, str]:
        """
        Valida a complexidade de uma senha de acordo com critérios especificados.

        A função verifica se a senha atende a requisitos mínimos de comprimento e presença
        de diferentes tipos de caracteres (maiúsculas, minúsculas, dígitos e símbolos).

        Args:
            senha (str): A senha a ser validada.
            tamanho (int): Comprimento mínimo exigido para a senha (default: 8).
            maiusculas (bool): Se True, exige ao menos uma letra maiúscula (default: True).
            minusculas (bool): Se True, exige ao menos uma letra minúscula (default: True).
            digitos (bool): Se True, exige ao menos um número (default: True).
            simbolos (bool): Se True, exige ao menos um caractere não alfanumérico (default: True).

        Returns:
            bool: True se a senha atender a todos os critérios especificados, False caso contrário.
        """
        valida = True
        mensagens = []
        valida = valida and (len(senha) >= tamanho)
        if tamanho > 0:
            mensagens.append(f"tamanho mínimo de {tamanho} caracteres")
        if maiusculas:
            mensagens.append("pelo menos uma letra maiúscula")
            valida = valida and (re.search(r'[A-Z]', senha) is not None)
        if minusculas:
            mensagens.append("pelo menos uma letra minúscula")
            valida = valida and (re.search(r'[a-z]', senha) is not None)
        if digitos:
            mensagens.append("pelo menos um número")
            valida = valida and (re.search(r'\d', senha) is not None)
        if simbolos:
            mensagens.append("pelo menos um símbolo")
            valida = valida and (re.search(r'\W', senha) is not None)
            if simbolos:
                mensagens.append("pelo menos um símbolo")
                valida = valida and (re.search(r'\W', senha) is not None)

        mensagem = "Sua senha deve conter " + ", ".join(mensagens) + "."
        return valida, mensagem