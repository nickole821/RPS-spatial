import numpy as np
import pandas as pd
import os
import time
from tqdm import tqdm, trange
import sys
import matplotlib.pyplot as plt
import pickle
import random
import math

# variaveis
L = 100 # lado do lattice
n_lagartos = L**2 # lagartos que cabem no lattice
estrategias = ['O', 'Y', 'B'] # estratégias possíveis
index_map = {'O': 0, 'Y': 1, 'B': 2}
n_geracoes = 200
n_pop = 100 # número de populações independentes
prob_mutacao = None # probabilidade de mutação a cada geração
vizinho_aprendizado_Y = 4

output_dir = f"C:/Unicamp/mestrado/simulacoes/RPS-python/RPS-POO/outputs/vizinhanca_aprendizado-interacao/learning_diferente/vizinho_aprendizado_Y_{str(vizinho_aprendizado_Y)}/"
os.makedirs(output_dir, exist_ok=True)

class Lagarto:
  def __init__(self, i, j, estrategia, fitness, coord_vizinhos_interacao, estrategia_vizinhos_interacao, coord_vizinhos_aprendizado, estrategia_vizinhos_aprendizado, t, n_vizinhos_interacao, n_vizinhos_aprendizado):
    self.i = i # linha
    self.j = j # coluna
    self.estrategia = estrategia
    self.fitness = 0 # inicia com 0 de fitness
    self.coord_vizinhos_interacao = [] # lista vazia para adicionar as coordenadas dos vizinhos
    self.estrategia_vizinhos_interacao = [] # lista vazia para adicionar as estratégias dos vizinhos
    self.coord_vizinhos_aprendizado = []
    self.estrategia_vizinhos_aprendizado = []
    self.t = t  # determina a geracao do lagarto
    self.n_vizinhos_interacao = n_vizinhos_interacao # número de vizinhos que o lagarto efetivamente joga
    self.n_vizinhos_aprendizado = n_vizinhos_aprendizado # número de vizinhos que o lagarto olha para aprender

  def calcular_coord_vizinhos(self, L, tipo):
    if tipo == 'interacao':
        # Calcula o menor raio necessário para abranger pelo menos n_vizinhos
        n_vizinhos = self.n_vizinhos_interacao
        raio = math.ceil((math.sqrt(n_vizinhos + 1) - 1) / 2)
        vizinhos = []
        for dx in range(-raio, raio + 1):
            for dy in range(-raio, raio + 1):
                if dx == 0 and dy == 0:
                    continue
                ni = (self.i + dx) % L
                nj = (self.j + dy) % L
                vizinhos.append((ni, nj))
        vizinhos = list(set(vizinhos))
        if len(vizinhos) < n_vizinhos:
            raise ValueError(f"Não há vizinhos suficientes: pedido={n_vizinhos}, disponíveis={len(vizinhos)}")
        selecionados = random.sample(vizinhos, n_vizinhos)
        self.coord_vizinhos_interacao = selecionados

    elif tipo == 'aprendizado':
        n_vizinhos = self.n_vizinhos_aprendizado
        raio = math.ceil((math.sqrt(n_vizinhos + 1) - 1) / 2)
        vizinhos = []
        for dx in range(-raio, raio + 1):
            for dy in range(-raio, raio + 1):
                if dx == 0 and dy == 0:
                    continue
                ni = (self.i + dx) % L
                nj = (self.j + dy) % L
                vizinhos.append((ni, nj))
        vizinhos = list(set(vizinhos))
        if len(vizinhos) < n_vizinhos:
            raise ValueError(f"Não há vizinhos suficientes: pedido={n_vizinhos}, disponíveis={len(vizinhos)}")
        selecionados = random.sample(vizinhos, n_vizinhos)
        self.coord_vizinhos_aprendizado = selecionados
    
  def obter_estrategia_vizinhos(self, matriz_posicao):
      self.estrategia_vizinhos_interacao = [matriz_posicao[ni, nj] for ni, nj in self.coord_vizinhos_interacao] # dadas as coordenadas, obtém a estratégia do lagarto que ocupa aquela posição
      self.estrategia_vizinhos_aprendizado = [matriz_posicao[ni, nj] for ni, nj in self.coord_vizinhos_aprendizado] # dadas as coordenadas, obtém a estratégia do lagarto que ocupa aquela posição

  def mutacao(self, prob_mutacao): # função de mutação
    if np.random.rand() < prob_mutacao: # sorteia um valor entre 0 e 1, se for menor que a probabilidade de mutação, o lagarto muda de estratégia
        estrategias_possiveis = [e for e in estrategias if e != self.estrategia] # obtém as estratégias possíveis, exceto a atual
        self.estrategia = np.random.choice(estrategias_possiveis) # escolhe uma nova estratégia aleatoriamente para mutar

  def adicionar_vizinhos_inicial(self, vizinho_aprendizado_Y):
      if self.estrategia == 'Y':
          #n_vizinhos_interacao = np.random.randint(1, 9)
          n_vizinhos_interacao = 24
          self.n_vizinhos_interacao = n_vizinhos_interacao
          #n_vizinhos_aprendizado = np.random.randint(1, 9)
          n_vizinhos_aprendizado = vizinho_aprendizado_Y
          self.n_vizinhos_aprendizado = n_vizinhos_aprendizado
      elif self.estrategia == 'O':
          #n_vizinhos_interacao = np.random.randint(1, 9)
          n_vizinhos_interacao = 24
          self.n_vizinhos_interacao = n_vizinhos_interacao
          #n_vizinhos_aprendizado = np.random.randint(1, 9)
          n_vizinhos_aprendizado = 24
          self.n_vizinhos_aprendizado = n_vizinhos_aprendizado
      elif self.estrategia == 'B':
          #n_vizinhos_interacao = np.random.randint(1, 9)
          n_vizinhos_interacao = 24
          self.n_vizinhos_interacao = n_vizinhos_interacao
          #n_vizinhos_aprendizado = np.random.randint(1, 9)
          n_vizinhos_aprendizado = 24
          self.n_vizinhos_aprendizado = n_vizinhos_aprendizado

def calcular_media_vizinhos(lagartos, estrategias, tipo):
    if tipo == 'interacao':
        medias_interacao = []
        for e in estrategias:
            #viz = [lag.n_vizinhos_realizado for lag in lagartos if lag.estrategia == e]
            viz = [lag.n_vizinhos_interacao for lag in lagartos if lag.estrategia == e]
            medias_interacao.append(np.mean(viz) if len(viz) > 0 else 0)
        return medias_interacao # retorna a média de vizinhos para cada estratégia

    elif tipo == 'aprendizado':
        medias_aprendizado = []
        for e in estrategias:
            viz = [lag.n_vizinhos_aprendizado for lag in lagartos if lag.estrategia == e]
            medias_aprendizado.append(np.mean(viz) if len(viz) > 0 else 0)
        return medias_aprendizado # retorna a média de vizinhos para cada estratégia
    

def criar_lagartos(n_lagartos, L, estrategias): # define as posições e estratégias dos lagartos no t = 0
  lista_lagartos = []

  # posições iniciais aleatórias
  all_positions = [(i, j) for i in range(L) for j in range(L)] # forma todas as posições possíveis em um lattice
  unique_positions_indices = np.random.choice(len(all_positions), n_lagartos, replace=False) # determina o índice de onde vai ficar cada posição
  unique_positions = [all_positions[i] for i in unique_positions_indices] # basicamente, ele embaralhou as posições

  for g in range(n_lagartos):
    i, j = unique_positions[g] # posição na matriz
    estrategia = np.random.choice(estrategias) # sorteia a estrategia
    lista_lagartos.append(Lagarto(i, j, estrategia, 0, [], [], [], [], 0, 0, 0)) # cria o lagarto
  return lista_lagartos

def calcular_fitness(lagarto, index_map, matriz_posicao): # função para calcular o fitness do lagarto
    fitness_total = 0 # inicia no 0

    b = 2
    c = 1.5

    matriz_payoff = np.array([[1, b-c, b],
                              [b, 1, b-c],
                              [b-c, b, 1]])
    
    vizinhos_interacao = set(lagarto.coord_vizinhos_interacao)
    for ni, nj in vizinhos_interacao:
        vizinho_estrat = matriz_posicao[ni, nj] # pega a estratégia do vizinho dadas as suas coordenadas
        if vizinho_estrat is not None:
            fitness_total += matriz_payoff[index_map[lagarto.estrategia], index_map[vizinho_estrat]] # calcula o payoff do lagarto contra o vizinho de acordo com a matriz de payoff e soma ao fitness total
    lagarto.fitness = fitness_total # adiciona ruído gaussiano ao fitness
    return fitness_total

calcular_freq = lambda mat: np.array([np.sum(mat == s) / (L ** 2) for s in ['O', 'Y', 'B']]) # calcula a frequência de cada estratégia no lattice na ordem O, Y, B

def atualizar_lagartos(lagartos): # função que atualiza as estratégias dos lagartos com base no fitness dos vizinhos
    novas_estrategias = {} # Dicionário para armazenar as novas estratégias
    novas_vizinhancas_aprendizado = {} # Dicionário para armazenar as novas vizinhanças de aprendizado
    novas_vizinhancas_interacao = {} # Dicionário para armazenar as novas vizinhanças de interação

    mapa = {(l.i, l.j): l for l in lagartos} # dicionário para acessar lagartos pela posição

    for lagarto in lagartos:
        melhor_estrategia = lagarto.estrategia # inicia com a própria estratégia
        maior_fitness = lagarto.fitness # verifica o fitness do próprio lagarto
        melhor_vizinhanca_aprendizado = lagarto.n_vizinhos_aprendizado
        melhor_vizinhanca_interacao = lagarto.n_vizinhos_interacao
            
        # verifica o fitness dos vizinhos
        for (ni, nj) in lagarto.coord_vizinhos_aprendizado:
            vizinho = mapa[(ni, nj)] # usa o dicionário para achar o vizinho
            if vizinho.fitness > maior_fitness: # se o fitness do vizinho for maior que o maior fitness atual
                maior_fitness = vizinho.fitness # atualiza o maior fitness
                melhor_estrategia = vizinho.estrategia # atualiza a melhor estratégia
                melhor_vizinhanca_aprendizado = vizinho.n_vizinhos_aprendizado # atualiza a melhor vizinhança
                melhor_vizinhanca_interacao = vizinho.n_vizinhos_interacao
            if vizinho.fitness == maior_fitness:
                a = np.random.rand()
                if a < 0.5:
                    maior_fitness = vizinho.fitness # atualiza o maior fitness
                    melhor_estrategia = vizinho.estrategia # atualiza a melhor estratégia
                    melhor_vizinhanca_aprendizado = vizinho.n_vizinhos_aprendizado # atualiza a melhor vizinhança
                    melhor_vizinhanca_interacao = vizinho.n_vizinhos_interacao
                else:
                    pass
                # se houver empate de fitness ou for menor, mantém a estratégia atual (não muda)

        novas_estrategias[(lagarto.i, lagarto.j)] = melhor_estrategia # armazena a nova estratégia no dicionário
        novas_vizinhancas_aprendizado[(lagarto.i, lagarto.j)] = melhor_vizinhanca_aprendizado # armazena a nova vizinhança no dicionário
        novas_vizinhancas_interacao[(lagarto.i, lagarto.j)] = melhor_vizinhanca_interacao # armazena a nova vizinhança no dicionário

     # atualiza as estratégias de todos os lagartos simultaneamente
    for lagarto in lagartos:
        lagarto.estrategia = novas_estrategias[(lagarto.i, lagarto.j)]  # atualiza estratégia
        # Garantir tamanhos fixos para O e B; somente Y herda vizinhança adaptativa
        #if lagarto.estrategia == 'O':
            #lagarto.n_vizinhos = 24
        #elif lagarto.estrategia == 'B':
            #lagarto.n_vizinhos = 8
        #else:  # 'Y'
        lagarto.n_vizinhos_aprendizado = novas_vizinhancas_aprendizado[(lagarto.i, lagarto.j)]
        lagarto.n_vizinhos_interacao = novas_vizinhancas_interacao[(lagarto.i, lagarto.j)]
    
    return lagartos

# iniciando a simulação
def simulacao(n_geracoes, L, n_lagartos, estrategias, index_map, n_pop, sigma, prob_mutacao = None, seed = None):
    
    matriz_frequencias = np.full((n_geracoes + 1, n_pop, len(estrategias)), np.nan, dtype=float) # cria uma matriz para armazenar as frequências em cada instante dos loops
    matriz_n_vizinhos_aprendizado_media = np.full((n_geracoes + 1, n_pop, len(estrategias)), np.nan, dtype=float) # cria uma matriz para armazenar vizinhos
    n_vizinhos_aprendizado_individual = []  
    matriz_n_vizinhos_interacao_media = np.full((n_geracoes + 1, n_pop, len(estrategias)), np.nan, dtype=float) # cria uma matriz para armazenar vizinhos
    n_vizinhos_interacao_individual = [] 
    historico_estrategias = []

    for pop in range(n_pop): # loop para cada população independente
        if seed is not None:
          np.random.seed(seed + pop) # coloca uma semente diferente pra cada pop, garantindo independência e reproducibilidade

        frequencias = [] # vai armazenar as frequências ao longo das gerações para essa população
        matriz_posicao = np.full((L, L), None) # cria uma matriz vazia com None
        historico_estrategias_pop = []
        n_vizinhos_aprendizado_pop = []
        n_vizinhos_interacao_pop = []

        lista_lagartos = criar_lagartos(n_lagartos, L, estrategias) # cria os lagartos
        for lagarto in lista_lagartos:
            lagarto.adicionar_vizinhos_inicial(vizinho_aprendizado_Y) # adiciona o número de vizinhos iniciais de acordo com a estratégia
            matriz_posicao[lagarto.i, lagarto.j] = str(lagarto.estrategia) # cria a matriz de posições de acordo com os lagartos

        frequencias.append(calcular_freq(matriz_posicao)) # calcula a frequência inicial
        n_vizinhos_aprendizado_pop.append([lagarto.n_vizinhos_aprendizado for lagarto in lista_lagartos])  # geração inicial
        n_vizinhos_interacao_pop.append([lagarto.n_vizinhos_interacao for lagarto in lista_lagartos])  # geração inicial
        historico_estrategias_pop.append([lagarto.estrategia for lagarto in lista_lagartos])  # histórico de estratégias
        matriz_n_vizinhos_aprendizado_media[0, pop, :] = calcular_media_vizinhos(lista_lagartos, estrategias, 'aprendizado')
        matriz_n_vizinhos_interacao_media[0, pop, :] = calcular_media_vizinhos(lista_lagartos, estrategias, 'interacao')

        for t in range(1, n_geracoes + 1): # loop para cada geração dentro da população
          # determinando os vizinhos
          for lagarto in lista_lagartos:
            lagarto.calcular_coord_vizinhos(L, 'interacao') # calcula as coordenadas dos vizinhos
            lagarto.calcular_coord_vizinhos(L, 'aprendizado') # calcula as coordenadas dos vizinhos
            lagarto.obter_estrategia_vizinhos(matriz_posicao) # obtém as estratégias dos vizinhos

          # calculando o fitness
          for lagarto in lista_lagartos:
            calcular_fitness(lagarto, index_map, matriz_posicao) # calcula o fitness do lagarto de acordo com seus vizinhos e a matriz de fitness

          lista_lagartos = atualizar_lagartos(lista_lagartos) # atualiza as estratégias dos lagartos de acordo com o maior fitness dos vizinhos

          if prob_mutacao is not None:
            for lagarto in lista_lagartos:
              lagarto.mutacao(prob_mutacao) # aplica a mutação

          # atualiza a matriz de posição com as novas estratégias e com as mutações
          matriz_posicao = np.full((L, L), None)
          for lagarto in lista_lagartos:
            matriz_posicao[lagarto.i, lagarto.j] = str(lagarto.estrategia)
          #print(matriz_posicao)

          n_vizinhos_aprendizado_geracao = [lagarto.n_vizinhos_aprendizado for lagarto in lista_lagartos]
          n_vizinhos_aprendizado_pop.append(n_vizinhos_aprendizado_geracao)
          n_vizinhos_interacao_geracao = [lagarto.n_vizinhos_interacao for lagarto in lista_lagartos]
          n_vizinhos_interacao_pop.append(n_vizinhos_interacao_geracao)
          matriz_n_vizinhos_aprendizado_media[t, pop, :] = calcular_media_vizinhos(lista_lagartos, estrategias, 'aprendizado') # calcula a média de vizinhos para cada estratégia e armazena na matriz n_vizinhos
          matriz_n_vizinhos_interacao_media[t, pop, :] = calcular_media_vizinhos(lista_lagartos, estrategias, 'interacao') # calcula a média de vizinhos para cada estratégia e armazena na matriz n_vizinhos
          #print(matriz_n_vizinhos[t, pop, :]) # debug
          historico_estrategias_pop.append([lagarto.estrategia for lagarto in lista_lagartos])  # histórico de estratégias
          frequencias.append(calcular_freq(matriz_posicao)) # calcula a frequência dessa geração e armazena em frequencias

          for lagarto in lista_lagartos:
              lagarto.t += 1 # incrementa a geração do lagarto
          
        frequencias = np.array(frequencias)
        n_vizinhos_aprendizado_individual.append(n_vizinhos_aprendizado_pop)
        n_vizinhos_interacao_individual.append(n_vizinhos_interacao_pop)
        historico_estrategias.append(historico_estrategias_pop)
        for t in range(n_geracoes + 1):
          matriz_frequencias[t, pop, :] = frequencias[t]

          # >>>>> SALVAR OS DADOS DESTA POPULAÇÃO <<<<<
        with open(os.path.join(output_dir, f"pop_{pop}_n_vizinhos_aprendizado_individual.pkl"), "wb") as f:
          pickle.dump(n_vizinhos_aprendizado_pop, f)
        with open(os.path.join(output_dir, f"pop_{pop}_n_vizinhos_interacao_individual.pkl"), "wb") as f:
          pickle.dump(n_vizinhos_interacao_pop, f)
        with open(os.path.join(output_dir, f"pop_{pop}_historico_estrategias.pkl"), "wb") as f:
          pickle.dump(historico_estrategias_pop, f)
        np.save(os.path.join(output_dir, f"pop_{pop}_matriz_frequencias.npy"), frequencias)
        np.save(os.path.join(output_dir, f"pop_{pop}_matriz_n_vizinhos_aprendizado_media.npy"), matriz_n_vizinhos_aprendizado_media[:, pop, :])
        np.save(os.path.join(output_dir, f"pop_{pop}_matriz_n_vizinhos_interacao_media.npy"), matriz_n_vizinhos_interacao_media[:, pop, :])
            # >>>>> FIM DO SALVAMENTO <<<<<

    return matriz_frequencias, matriz_n_vizinhos_aprendizado_media, matriz_n_vizinhos_interacao_media, n_vizinhos_aprendizado_individual, n_vizinhos_interacao_individual, historico_estrategias

freq, n_vizinhos_aprendizado, n_vizinhos_interacao, n_vizinhos_aprendizado_individual, n_vizinhos_interacao_individual, historico_estrategias = simulacao(n_geracoes, L, n_lagartos, estrategias, index_map, n_pop, prob_mutacao = prob_mutacao, seed = 1)

# transforma freq em DataFrame formato tidy
linhas = []
for t in range(freq.shape[0]):             # gerações
    for pop in range(freq.shape[1]):       # populações
        for idx, strategy in enumerate(estrategias):  # estratégias
            linhas.append({
                "t": t, # coluna 1: geração
                "pop": pop, # coluna 2: população
                "estrategia": strategy, # coluna 3: estrategia
                "frequencia": freq[t, pop, idx] # coluna 4: frequência da estratégia naquela geração, naquela população
            })

df_long = pd.DataFrame(linhas)

# salvar como CSV
df_long.to_csv(os.path.join(output_dir, "frequencias.csv"), index=False)

cores = {"O": "#FD9800", "B": "#0047B3", "Y": "#FFF237"}

plt.figure(figsize=(12, 6))
for strategy in estrategias:
    subset = df_long[df_long["estrategia"] == strategy]
    media = subset.groupby("t")["frequencia"].mean()
    desvio = subset.groupby("t")["frequencia"].std()
    plt.plot(media.index, media.values, label=strategy, color=cores[strategy])
    plt.fill_between(media.index, media - desvio, media + desvio, color=cores[strategy], alpha=0.2)

plt.title("Frequências das estratégias ao longo do tempo")
plt.xlabel("Gerações")
plt.ylabel("Frequência")
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(output_dir, "plot_freq.png"), dpi = 300, bbox_inches='tight')
plt.show()


import matplotlib.animation as animation
import matplotlib.pyplot as plt

def simulacao_gif(n_geracoes, L, n_lagartos, estrategias, index_map, prob_mutacao = None, seed = None):

    matrizes_posicao_hist = [] # lista para armazenar as matrizes de posição de cada geração
    matrizes_fitness_hist = []
    matrizes_vizinhanca_interacao_hist = []
    matrizes_vizinhanca_aprendizado_hist = []

    if seed is not None:
        np.random.seed(seed) # coloca uma semente diferente pra cada pop

    # criando a matriz inicial
    matriz_posicao = np.full((L, L), None) # cria uma matriz vazia com None
    matriz_fitness = np.full((L, L), 0.0) # cria uma matriz vazia com 0
    matriz_vizinhanca_interacao = np.full((L, L), 0.0)
    matriz_vizinhanca_aprendizado = np.full((L, L), 0.0)

    lista_lagartos = criar_lagartos(n_lagartos, L, estrategias) # cria os lagartos
    for lagarto in lista_lagartos:
        lagarto.adicionar_vizinhos_inicial(vizinho_aprendizado_Y) # adiciona o número de vizinhos iniciais de acordo com a estratégia
        matriz_posicao[lagarto.i, lagarto.j] = str(lagarto.estrategia) # cria a matriz de posições de acordo com os lagartos
        matriz_vizinhanca_interacao[lagarto.i, lagarto.j] = lagarto.n_vizinhos_interacao
        matriz_vizinhanca_aprendizado[lagarto.i, lagarto.j] = lagarto.n_vizinhos_aprendizado

    matrizes_posicao_hist.append(matriz_posicao.copy()) # junta as matrizes em uma lista
    matrizes_fitness_hist.append(matriz_fitness.copy())
    matrizes_vizinhanca_interacao_hist.append(matriz_vizinhanca_interacao.copy())
    matrizes_vizinhanca_aprendizado_hist.append(matriz_vizinhanca_aprendizado.copy())

    for t in range(1, n_geracoes + 1):
    # criando os vizinhos
      print(f"Geração {t}")
      for lagarto in lista_lagartos:
          lagarto.calcular_coord_vizinhos(L, 'interacao') # calcula as coordenadas dos vizinhos
          lagarto.calcular_coord_vizinhos(L, 'aprendizado') # calcula as coordenadas dos vizinhos
          lagarto.obter_estrategia_vizinhos(matriz_posicao) # obtém as estratégias dos vizinhos

        # calculando o fitness
      for lagarto in lista_lagartos:
          calcular_fitness(lagarto, index_map, matriz_posicao) # calcula o fitness do lagarto de acordo com seus vizinhos e a matriz de fitness

      matriz_fitness = np.full((L, L), 0.0)
      for lagarto in lista_lagartos:
        matriz_fitness[lagarto.i, lagarto.j] = float(lagarto.fitness) # coloca os fitness nas posições
        matriz_vizinhanca_aprendizado[lagarto.i, lagarto.j] = lagarto.n_vizinhos_aprendizado
        matriz_vizinhanca_interacao[lagarto.i, lagarto.j] = lagarto.n_vizinhos_interacao
      #print(matriz_fitness)

      lista_lagartos = atualizar_lagartos(lista_lagartos)

      # atualiza a matriz de posição com as novas estratégias e com as mutações
      matriz_posicao = np.full((L, L), None)
      for lagarto in lista_lagartos:
        matriz_posicao[lagarto.i, lagarto.j] = str(lagarto.estrategia)

      for lagarto in lista_lagartos:
            lagarto.t += 1
      
      #print(matriz_posicao)

      matrizes_posicao_hist.append(matriz_posicao.copy()) # Append updated matrix position
      matrizes_fitness_hist.append(matriz_fitness.copy())
      matrizes_vizinhanca_interacao_hist.append(matriz_vizinhanca_interacao.copy())
      matrizes_vizinhanca_aprendizado_hist.append(matriz_vizinhanca_aprendizado.copy())

    return matrizes_posicao_hist, matrizes_fitness_hist, matrizes_vizinhanca_interacao_hist, matrizes_vizinhanca_aprendizado_hist # Return both frequencies and matrix history

matrizes_posicao_hist, matrizes_fitness_hist, matrizes_vizinhanca_interacao_hist, matrizes_vizinhanca_aprendizado_hist = simulacao_gif(n_geracoes, L, n_lagartos, estrategias, index_map, prob_mutacao=prob_mutacao, seed=1)

# gerando o GIF das posições

import matplotlib.colors as mcolors

cores_grid = {"O": "#FD9800", "B": "#0047B3", "Y": "#FFF237"}

def matriz_para_rgb(matriz):
    # Converte hex para RGB normalizado (0-1)
    return np.array([[mcolors.to_rgb(cores_grid.get(cell, "#FFFFFF")) for cell in row] for row in matriz])

# Crie a figura
fig, ax = plt.subplots(figsize=(6, 6))

def update(frame):
    ax.clear()
    ax.imshow(matriz_para_rgb(matrizes_posicao_hist[frame]))
    ax.set_title(f"Geração {frame}")
    ax.axis('off')

ani = animation.FuncAnimation(
    fig, update, frames=len(matrizes_posicao_hist), interval=100, repeat=False
)


# Salvar como GIF
ani.save(os.path.join(output_dir, f"simulacao_grid.gif"), writer='pillow', fps=10)
ani.save(os.path.join(output_dir, f"simulacao_grid.mp4"), writer='ffmpeg', fps=10)
plt.close()