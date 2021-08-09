import re

class Criptografia_Vigenere(object):
    def __init__(self):
        self.tabela = self.Criar_tabela()

    def Criar_tabela(self):
        tabela = []

        for i in range(0, 26):
            linha = []
            for j in range(0, 26):
                cod_letra_atual = i+65+j
                if cod_letra_atual > 90:
                    cod_letra_atual -= 26
                letra_atual = chr(cod_letra_atual)
                linha.append(letra_atual)
            tabela.append(linha)

        return tabela

    def Encriptar(self, texto, chave):
        texto = self.Processar_texto(texto)
        chave_repetida = self.Repetir_chave(chave, len(texto))
        
        texto_cifrado = ''

        for i, letra in enumerate(texto):
            indice_letra = ord(letra.upper()) - 65
            indice_chave = ord(chave_repetida[i]) - 65

            letra_cifrada = self.tabela[indice_chave][indice_letra]

            texto_cifrado += letra_cifrada

        return texto_cifrado

    def Decriptar(self, texto, chave):
        chave_repetida = self.Repetir_chave(chave, len(texto))
        texto_decifrado = ''

        for i, letra in enumerate(texto):
            indice_chave = ord(chave_repetida[i]) - 65

            letra_decifrada = chr(self.tabela[indice_chave].index(letra) + 65)

            texto_decifrado += letra_decifrada
        return texto_decifrado
        
    def Processar_texto(self, texto):
        texto = texto.upper()
        texto = re.sub('[^A-Z]', '', texto)

        return texto
    def Repetir_chave(self, chave, tamanho):

        chave = chave.upper()
        chave_repetida = ''
        indice = 0

        for i in range(tamanho):
            chave_repetida += chave[indice]
            indice += 1
            if indice > len(chave) -1:
                indice = 0

        return chave_repetida
