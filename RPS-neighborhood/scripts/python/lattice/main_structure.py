import numpy as np
import pandas as pd
import os
import time
from tqdm import tqdm, trange
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation

# variaveis
L = 500 # lado do lattice
n_lagartos = L**2 # lagartos que cabem no lattice
estrategias = ['O', 'Y', 'B'] # estratégias possíveis
a = 0.5
matriz_payoff = np.array([[1, 0.5, 2],
                          [2, 1, a],
                          [0.5, 2, 1]])
index_map = {'O': 0, 'Y': 1, 'B': 2}
n_geracoes = 100
n_pop = 100 # número de populações independentes
prob_mutacao = None # probabilidade de mutação a cada geração
valores = [4, 8, 24, 48, 80, 120] # número de vizinhos para cada lagarto

class Lagarto:
  def __init__(self, i, j, estrategia, fitness, n_vizinhos, coord_vizinhos, estrategia_vizinhos,
               coord_vizinhanca_extendida, estrategia_vizinhanca_extendida):
    self.i = i # linha
    self.j = j # coluna
    self.estrategia = estrategia
    self.fitness = 0 # inicia com 0 de fitness
    self.n_vizinhos = n_vizinhos
    self.coord_vizinhos = [] # lista vazia para adicionar as coordenadas dos vizinhos
    self.estrategia_vizinhos = [] # lista vazia para adicionar as estratégias dos vizinhos
    self.coord_vizinhanca_extendida = []
    self.estrategia_vizinhanca_extendida = []

  def calcular_coord_vizinhos(self, L): # obtém as coordenadas dos vizinhos
    n = self.n_vizinhos
    if n <= 0:
        print("Erro: n_vizinhos_interacao <= 0")
        return

    i0, j0 = self.i, self.j

    def moore(r):
        return {
            ((i0 + dx) % L, (j0 + dy) % L)
            for dx in range(-r, r + 1)
            for dy in range(-r, r + 1)
            if not (dx == 0 and dy == 0)
        }

    def von_neumann(r):
        return {
            ((i0 + dx) % L, (j0 + dy) % L)
            for dx in range(-r, r + 1)
            for dy in range(-r, r + 1)
            if (dx != 0 or dy != 0) and (abs(dx) + abs(dy) <= r)
        }
    
    r = int(np.ceil((np.sqrt(1 + n) - 1) / 2))

    vn_r = von_neumann(r)
    mo_r = moore(r)

    if n <= 2 * r * (r + 1):    # faixa Moore(r-1) -> VN(r)
        base = moore(r - 1) if r > 1 else set()
        pool = list(vn_r - base)
    else:                       # faixa VN(r) -> Moore(r)
        base = vn_r
        pool = list(mo_r - base)

    faltam = n - len(base)
    if faltam <= 0:
        extras = []
    else:
        idx = np.random.choice(len(pool), size=faltam, replace=False)
        extras = [pool[k] for k in idx]

    #print(f"Lagarto {self.estrategia} ({self.i}, {self.j}): vizinhos {list(base) + extras}")
    self.coord_vizinhos = list(base) + extras
    
  def obter_estrategia_vizinhos(self, matriz_posicao):
      self.estrategia_vizinhos = [matriz_posicao[ni, nj] for ni, nj in self.coord_vizinhos] # dadas as coordenadas, obtém a estratégia do lagarto que ocupa aquela posição

  def mutacao(self, prob_mutacao): # função de mutação
    if np.random.rand() < prob_mutacao: # sorteia um valor entre 0 e 1, se for menor que a probabilidade de mutação, o lagarto muda de estratégia
        estrategias_possiveis = [e for e in estrategias if e != self.estrategia] # obtém as estratégias possíveis, exceto a atual
        self.estrategia = np.random.choice(estrategias_possiveis) # escolhe uma nova estratégia aleatoriamente para mutar

  def calcular_n_vizinhos(self): # calcula o número de vizinhos
      return len(self.estrategia_vizinhos) + len(self.estrategia_vizinhanca_extendida)
  
  def calcular_fitness(self, matriz_payoff, index_map): # calcula o fitness do lagarto com base na matriz de payoff e nas estratégias dos vizinhos
    todos_vizinhos = self.estrategia_vizinhos
    payoff_total = 0
    for viz in todos_vizinhos:
        payoff_total += matriz_payoff[index_map[self.estrategia], index_map[viz]]
    self.fitness = payoff_total

def calcular_media_vizinhos(lagartos, estrategias):
    medias = []
    for e in estrategias:
        viz = [lag.n_vizinhos for lag in lagartos if lag.estrategia == e]
        medias.append(np.mean(viz) if len(viz) > 0 else 0)
    return medias # retorna a média de vizinhos para cada estratégia

def ajustar_vizinhos_reciprocos(lagartos): # garante que se A é vizinho de B, B também é vizinho de A, pois as interações são recíprocas
    mapa = {(l.i, l.j): l for l in lagartos} # dicionário pra acessar lagartos pela posição

    for l in lagartos:
        for (ni, nj) in l.coord_vizinhos: # vai em todos os vizinhos do lagarto atual (l)
            vizinho = mapa[(ni, nj)]
            # se o lagarto atual (l) não estiver na lista de vizinhos do vizinho, adiciona em vizinhanca_extendida
            if (l.i, l.j) not in vizinho.coord_vizinhos:
                vizinho.estrategia_vizinhanca_extendida.append(str(l.estrategia))
                vizinho.coord_vizinhanca_extendida.append((l.i, l.j))

def criar_lagartos(L):
    lista = []
    for i in range(L):
        for j in range(L):
            estrategia = np.random.choice(estrategias)
            n_vizinhos = vizinhanca
            lista.append(Lagarto(i, j, estrategia, 0, n_vizinhos, [], [], [], []))
    return lista

def calcular_freq(mat, estrategia):
    if estrategia == 'O':
        return np.sum(mat == 'O') / (L ** 2)
    elif estrategia == 'Y':
        return np.sum(mat == 'Y') / (L ** 2)
    elif estrategia == 'B':
        return np.sum(mat == 'B') / (L ** 2)

def atualizar_lagartos(lagartos): # função que atualiza as estratégias dos lagartos com base no fitness dos vizinhos
    novas_estrategias = {} # Dicionário para armazenar as novas estratégias

    mapa = {(l.i, l.j): l for l in lagartos} # dicionário para acessar lagartos pela posição

    for lagarto in lagartos:
        #print(f"Atualizando lagarto na posição ({lagarto.i}, {lagarto.j}) com estratégia {lagarto.estrategia} e fitness {lagarto.fitness}")
        melhor_estrategia = lagarto.estrategia # inicia com a própria estratégia
        maior_fitness = lagarto.fitness # verifica o fitness do próprio lagarto

        todos_vizinhos = set(lagarto.coord_vizinhos + lagarto.coord_vizinhanca_extendida)
        #print(f"Vizinhos do lagarto ({lagarto.i}, {lagarto.j}): {todos_vizinhos}")
        # verifica o fitness dos vizinhos normais
        for (ni, nj) in todos_vizinhos:
            vizinho = mapa[(ni, nj)] # usa o dicionário para achar o vizinho
            #print(f"Vizinho ({vizinho.i}, {vizinho.j}): {vizinho.estrategia}, Fitness: {vizinho.fitness}")
            if vizinho.fitness > maior_fitness: # se o fitness do vizinho for maior que o maior fitness atual
                #print(f"Vizinho ({vizinho.i}, {vizinho.j}) tem fitness maior")
                maior_fitness = vizinho.fitness # atualiza o maior fitness
                melhor_estrategia = vizinho.estrategia # atualiza a melhor estratégia
            elif vizinho.fitness == maior_fitness:
                #print(f"Vizinho ({vizinho.i}, {vizinho.j}) tem fitness igual ao maior")
                a = np.random.rand()
                if a < 0.5:
                    maior_fitness = vizinho.fitness # atualiza o maior fitness
                    melhor_estrategia = vizinho.estrategia # atualiza a melhor estratégia
                else:
                    pass
            else:
                pass
        
        #print(f"Melhor estratégia para lagarto ({lagarto.i}, {lagarto.j}): {melhor_estrategia} com fitness {maior_fitness}")
            
        novas_estrategias[(lagarto.i, lagarto.j)] = melhor_estrategia # armazena a nova estratégia no dicionário

    # atualiza as estratégias de todos os lagartos simultaneamente
    for lagarto in lagartos:
        lagarto.estrategia = novas_estrategias[(lagarto.i, lagarto.j)] # evita que a atualização de um lagarto influencie outro na mesma geração (sem sobreposição de geração)

    return lagartos

def simulacao(a, vizinhanca, L, matriz_payoff, index_map, n_pop, prob_mutacao = None, seed = None):
    resultados = []

    for pop in range(n_pop): # loop para cada população independente
      if seed is not None:
          np.random.seed(seed + pop) # coloca uma semente diferente pra cada pop, garantindo independência

      lista_lagartos = criar_lagartos(L) # cria os lagartos

      matriz_posicao = np.full((L, L), None) # cria uma matriz vazia com None
      for lagarto in lista_lagartos:
        matriz_posicao[lagarto.i, lagarto.j] = str(lagarto.estrategia) # cria a matriz de posições de acordo com os lagartos

      #print(matriz_posicao)
      
      freq_O = calcular_freq(matriz_posicao, 'O')
      freq_Y = calcular_freq(matriz_posicao, 'Y')
      freq_B = calcular_freq(matriz_posicao, 'B')

      resultados.append({
        "pop": pop,
        "t": -1,
        "freq_O": freq_O,
        "freq_Y": freq_Y,
        "freq_B": freq_B,
        "a": a,
        "vizinhanca": vizinhanca
      })

      for t in range(1, n_geracoes + 1): # loop para cada geração dentro da população
        # determinando os vizinhos
        for lagarto in lista_lagartos:
          lagarto.calcular_coord_vizinhos(L) # calcula as coordenadas dos vizinhos
          print(len(lagarto.coord_vizinhos))
          lagarto.obter_estrategia_vizinhos(matriz_posicao) # obtém as estratégias dos vizinhos
          lagarto.calcular_fitness(matriz_payoff, index_map) # calcula o fitness do lagarto de acordo com seus vizinhos e a matriz de fitness
          
        lista_lagartos = atualizar_lagartos(lista_lagartos) # atualiza as estratégias dos lagartos de acordo com o maior fitness dos vizinhos

        if prob_mutacao is not None:
          for lagarto in lista_lagartos:
            lagarto.mutacao(prob_mutacao) # aplica a mutação

        # atualiza a matriz de posição com as novas estratégias e com as mutações
        matriz_posicao = np.full((L, L), None)
        for lagarto in lista_lagartos:
          matriz_posicao[lagarto.i, lagarto.j] = str(lagarto.estrategia)
        
        #print(matriz_posicao)

        freq_O = calcular_freq(matriz_posicao, 'O')
        freq_Y = calcular_freq(matriz_posicao, 'Y')
        freq_B = calcular_freq(matriz_posicao, 'B')
        resultados.append({
          "pop": pop,
          "t": t,
          "freq_O": freq_O,
          "freq_Y": freq_Y,
          "freq_B": freq_B,
          "a": a,
          "vizinhanca": vizinhanca
        })

    return resultados

for vizinhanca in valores:
    df = simulacao(a, vizinhanca, L, matriz_payoff, index_map, n_pop, prob_mutacao = None, seed = 1)
    output_dir = f"C:/Unicamp/mestrado/simulacoes/main/RPS-neighborhood/outputs/null-model/matriz_1-a/n_vizinhos_{vizinhanca}/a_{a}/"
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, f"resultados_vizinhanca_{vizinhanca}.csv"), index=False)