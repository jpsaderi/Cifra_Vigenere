import re, string
from constantes import DESCONSIDERAR

MAX_KEY_LENGTH_GUESS = 20

alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Array containing the relative frequency of each letter in the English language
english_frequences = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
					  0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
					  0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
					  0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

# Returns the Index of Councidence for the "section" of ciphertext given
def get_index_c(ciphertext):
	
	N = float(len(ciphertext))
	frequency_sum = 0.0

	# Using Index of Coincidence formula
	for letter in alphabet:
		frequency_sum+= ciphertext.count(letter) * (ciphertext.count(letter)-1)

	# Using Index of Coincidence formula
	ic = frequency_sum/(N*(N-1))
	return ic

# Returns the key length with the highest average Index of Coincidence
def get_key_length(ciphertext):
	ic_table=[]

	# Splits the ciphertext into sequences based on the guessed key length from 0 until the max key length guess (20)
	# Ex. guessing a key length of 2 splits the "12345678" into "1357" and "2468"
	# This procedure of breaking ciphertext into sequences and sorting it by the Index of Coincidence
	# The guessed key length with the highest IC is the most porbable key length
	for guess_len in range(MAX_KEY_LENGTH_GUESS):
		ic_sum=0.0
		avg_ic=0.0
		for i in range(guess_len):
			sequence=""
			# breaks the ciphertext into sequences
			for j in range(0, len(ciphertext[i:]), guess_len):
				sequence += ciphertext[i+j]
			ic_sum+=get_index_c(sequence)
		# obviously don't want to divide by zero
		if not guess_len==0:
			avg_ic=ic_sum/guess_len
		ic_table.append(avg_ic)

	# returns the index of the highest Index of Coincidence (most probable key length)
	best_guess = ic_table.index(sorted(ic_table, reverse = True)[0])
	second_best_guess = ic_table.index(sorted(ic_table, reverse = True)[1])

	# Since this program can sometimes think that a key is literally twice itself, or three times itself, 
	# it's best to return the smaller amount.
	# Ex. the actual key is "dog", but the program thinks the key is "dogdog" or "dogdogdog"
	# (The reason for this error is that the frequency distribution for the key "dog" vs "dogdog" would be nearly identical)
	if best_guess % second_best_guess == 0:
		return second_best_guess
	else:
		return best_guess

# Performs frequency analysis on the "sequence" of the ciphertext to return the letter for that part of the key
# Uses the Chi-Squared Statistic to measure how similar two probability distributions are. 
# (The two being the ciphertext and regular english distribution)
def freq_analysis(sequence):
	all_chi_squareds = [0] * 26

	for i in range(26):

		chi_squared_sum = 0.0

		#sequence_offset = [(((seq_ascii[j]-97-i)%26)+97) for j in range(len(seq_ascii))]
		sequence_offset = [chr(((ord(sequence[j])-97-i)%26)+97) for j in range(len(sequence))]
		v = [0] * 26
		# count the numbers of each letter in the sequence_offset already in ascii
		for l in sequence_offset:
			v[ord(l) - ord('a')] += 1
		# divide the array by the length of the sequence to get the frequency percentages
		for j in range(26):
			v[j] *= (1.0/float(len(sequence)))

		# now you can compare to the english frequencies
		for j in range(26):
			chi_squared_sum+=((v[j] - float(english_frequences[j]))**2)/float(english_frequences[j])

		# add it to the big table of chi squareds
		all_chi_squareds[i] = chi_squared_sum

	# return the letter of the key that it needs to be shifted by
	# this is found by the smallest chi-squared statistic (smallest different between sequence distribution and 
	# english distribution)
	shift = all_chi_squareds.index(min(all_chi_squareds))

	# return the letter
	return chr(shift+97)

def get_key(ciphertext, key_length):
	key = ''

	# Calculate letter frequency table for each letter of the key
	for i in range(key_length):
		sequence=""
		# breaks the ciphertext into sequences
		for j in range(0,len(ciphertext[i:]), key_length):
			sequence+=ciphertext[i+j]
		key+=freq_analysis(sequence)

	return key

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
        texto = self.Processar_texto_ascii(texto)

        chave_repetida = self.Repetir_chave(chave, len(texto))
        
        texto_cifrado = ''

        contador = 0
        for i, letra in enumerate(texto):
            if letra in DESCONSIDERAR:
                texto_cifrado += letra
                contador += 1
            else:
                indice_letra = ord(letra.upper()) - 65
                indice_chave = ord(chave_repetida[i-contador]) - 65

                letra_cifrada = self.tabela[indice_chave][indice_letra]

                texto_cifrado += letra_cifrada

        return texto_cifrado

    def Decriptar(self, texto, chave):
        texto = self.Processar_texto_ascii(texto)
        chave_repetida = self.Repetir_chave(chave, len(texto))
        texto_decifrado = ''

        contador = 0
        for i, letra in enumerate(texto):
            if letra in DESCONSIDERAR:
                texto_decifrado += letra
                contador += 1
            else:
                indice_chave = ord(chave_repetida[i-contador]) - 65

                letra_decifrada = chr(self.tabela[indice_chave].index(letra) + 65)

                texto_decifrado += letra_decifrada
        return texto_decifrado

    def Processar_texto_ascii(self, texto):
        texto = texto.upper()
        texto = re.sub(rf'[^A-Z{DESCONSIDERAR}]', '', texto)
    
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
    
# Returns the Index of Councidence for the "section" of ciphertext given
def get_index_c(ciphertext):
	
	N = float(len(ciphertext))
	frequency_sum = 0.0

	# Using Index of Coincidence formula
	for letter in alphabet:
		frequency_sum+= ciphertext.count(letter) * (ciphertext.count(letter)-1)

	# Using Index of Coincidence formula
	ic = frequency_sum/(N*(N-1))
	return ic

# Returns the key length with the highest average Index of Coincidence
def get_key_length(ciphertext):
	ic_table=[]

	# Splits the ciphertext into sequences based on the guessed key length from 0 until the max key length guess (20)
	# Ex. guessing a key length of 2 splits the "12345678" into "1357" and "2468"
	# This procedure of breaking ciphertext into sequences and sorting it by the Index of Coincidence
	# The guessed key length with the highest IC is the most porbable key length
	for guess_len in range(MAX_KEY_LENGTH_GUESS):
		ic_sum=0.0
		avg_ic=0.0
		for i in range(guess_len):
			sequence=""
			# breaks the ciphertext into sequences
			for j in range(0, len(ciphertext[i:]), guess_len):
				sequence += ciphertext[i+j]
			ic_sum+=get_index_c(sequence)
		# obviously don't want to divide by zero
		if not guess_len==0:
			avg_ic=ic_sum/guess_len
		ic_table.append(avg_ic)

	# returns the index of the highest Index of Coincidence (most probable key length)
	best_guess = ic_table.index(sorted(ic_table, reverse = True)[0])
	second_best_guess = ic_table.index(sorted(ic_table, reverse = True)[1])

	# Since this program can sometimes think that a key is literally twice itself, or three times itself, 
	# it's best to return the smaller amount.
	# Ex. the actual key is "dog", but the program thinks the key is "dogdog" or "dogdogdog"
	# (The reason for this error is that the frequency distribution for the key "dog" vs "dogdog" would be nearly identical)
	if best_guess % second_best_guess == 0:
		return second_best_guess
	else:
		return best_guess

# Performs frequency analysis on the "sequence" of the ciphertext to return the letter for that part of the key
# Uses the Chi-Squared Statistic to measure how similar two probability distributions are. 
# (The two being the ciphertext and regular english distribution)
def freq_analysis(sequence):
	all_chi_squareds = [0] * 26

	for i in range(26):

		chi_squared_sum = 0.0

		#sequence_offset = [(((seq_ascii[j]-97-i)%26)+97) for j in range(len(seq_ascii))]
		sequence_offset = [chr(((ord(sequence[j])-97-i)%26)+97) for j in range(len(sequence))]
		v = [0] * 26
		# count the numbers of each letter in the sequence_offset already in ascii
		for l in sequence_offset:
			v[ord(l) - ord('a')] += 1
		# divide the array by the length of the sequence to get the frequency percentages
		for j in range(26):
			v[j] *= (1.0/float(len(sequence)))

		# now you can compare to the english frequencies
		for j in range(26):
			chi_squared_sum+=((v[j] - float(english_frequences[j]))**2)/float(english_frequences[j])

		# add it to the big table of chi squareds
		all_chi_squareds[i] = chi_squared_sum

	# return the letter of the key that it needs to be shifted by
	# this is found by the smallest chi-squared statistic (smallest different between sequence distribution and 
	# english distribution)
	shift = all_chi_squareds.index(min(all_chi_squareds))

	# return the letter
	return chr(shift+97)

def get_key(ciphertext, key_length):
	key = ''

	# Calculate letter frequency table for each letter of the key
	for i in range(key_length):
		sequence=""
		# breaks the ciphertext into sequences
		for j in range(0,len(ciphertext[i:]), key_length):
			sequence+=ciphertext[i+j]
		key+=freq_analysis(sequence)

	return key
