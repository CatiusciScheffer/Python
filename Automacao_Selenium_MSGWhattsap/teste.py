import time
import random

# Gere um valor aleatório entre 5 e 6 segundos
tempo_variavel = random.uniform(5, 6)

# Use time.sleep para pausar o programa pelo tempo variável
time.sleep(tempo_variavel)

# O programa irá pausar por um período de tempo entre 5 e 6 segundos
print(tempo_variavel)
