import Cifra_vigenere
import os

def Encriptar_mensagem():
    print('\t-----------------')
    print("\tCifra de Vigenere")
    print('\t-----------------\n')

    texto_entrada = input('Digite o texto que deve ser cifrado: ')
    chave_entrada = input('Digite a chave que quer usar para cifrar esse texto: ')

    viginere = Cifra_vigenere.Criptografia_Vigenere()

    texto_cifrado = viginere.Encriptar(texto_entrada, chave_entrada)
    print('O texto da entrada:')
    print('\t', texto_entrada)
    print('O texto encriptado:')
    print('\t', texto_cifrado)

    input("Pressione ENTER para continuar")

def Decriptar_mensagem():
    print('\t-----------------')
    print("\tCifra de Vigenere")
    print('\t-----------------\n')

    texto_entrada = input('Digite o texto que deve ser decifrado: ')
    chave_entrada = input('Digite a chave que quer usar para decifrar esse texto: ')

    viginere = Cifra_vigenere.Criptografia_Vigenere()

    texto_decifrado = viginere.Decriptar(texto_entrada, chave_entrada)
    print('O texto encriptado:')
    print('\t', texto_entrada)
    print('O texto de saida:')
    print('\t', texto_decifrado)
    
    input("Pressione ENTER para continuar")

def Atacar_mensagem():
    print('\t-----------------')
    print("\tCifra de Vigenere")
    print('\t-----------------\n')

    texto_entrada = input('Digite o texto que deve ser decifrado: ')

    texto_decifrado = ''
    print('O texto encriptado:')
    print('\t', texto_entrada)
    print('O texto de saida:')
    print('\t', texto_decifrado)

#main
while(True):
    print('\t-----------------')
    print("\tCifra de Vigenere")
    print('\t-----------------\n')
    
    print('Selecione a opcao:')
    print('1 - Encriptar mensagem com chave')
    print('2 - Decriptar mensagem com chave')
    print('3 - Atacar chave com mensagem')
    print('4 - Sair')

    op = input()

    os.system('cls' if os.name == 'nt' else 'clear')

    if op == '1':
        Encriptar_mensagem()
    elif op == '2':
        Decriptar_mensagem()
    elif op == '4':
        exit()            