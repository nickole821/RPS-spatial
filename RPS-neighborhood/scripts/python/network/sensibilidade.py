import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import networkx as nx
import copy

# ==============================
# PARÂMETROS GERAIS
# ==============================

L = 100
n_lagartos = L**2
estrategias = ['O', 'Y', 'B']

b = 2
c = 0.5

matriz_payoff = np.array([[1, c, b],
                          [b, 1, c],
                          [c, b, 1]])

index_map = {'O': 0, 'Y': 1, 'B': 2}

n_geracoes = 500
n_pop = 1
z_O_inicial = int(input("Número de vizinhos inicial para O (5x): "))
z_Y_inicial = int(input("Número de vizinhos inicial para Y (5x): "))
z_B = 8
sobreposicao = "n"
fermi = "s"
if fermi.lower() == 's':
    K = 0.001
    A = None
    wO = None
    wB = None
    wY = None
else:
    K = None
    A = float(input("Valor de A: "))
    wO = float(input("Valor de wO: "))
    wB = float(input("Valor de wB: "))
    wY = float(input("Valor de wY: "))


output_dir = f"C:/Unicamp/mestrado/simulacoes/main/RPS-neighborhood/outputs/network/sensibility/"
os.makedirs(output_dir, exist_ok=True)

# ==============================
# CLASSE LAGARTO
# ==============================

class Lagarto:
    def __init__(self, i, j, estrategia, fitness,
                 coord_vizinhos, n_vizinhos):
        self.i = i
        self.j = j
        self.estrategia = estrategia
        self.fitness = 0.0
        self.coord_vizinhos = []
        self.n_vizinhos = n_vizinhos


    def calcular_coord_vizinhos(self, L):
        n = self.n_vizinhos
        if n <= 0:
            print("Erro: n_vizinhos <= 0")
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

        self.coord_vizinhos = list(base) + extras

    def mortalidade(self, A, w):
        return 1 / (1 + A * np.exp(w * self.fitness))

    def calcular_fitness_rede(self, G):
        fitness_total = 0.0
        for vizinho in vizinhos_unicos_rede(G, self):
            fitness_total += matriz_payoff[index_map[self.estrategia], index_map[vizinho.estrategia]]
        self.fitness = fitness_total

    def atualizar_links_lagarto(self, G, L, mapa):
        G.remove_edges_from(list(G.out_edges(self)))

        self.calcular_coord_vizinhos(L)

        for (ni, nj) in self.coord_vizinhos:
            vizinho = mapa[(ni, nj)]
            G.add_edge(self, vizinho)

    def fermi_update(self, G, K):
        lista_vizinhos = vizinhos_unicos_rede(G, self)
        if len(lista_vizinhos) == 0:
            return self.estrategia, self.n_vizinhos

        vizinho_escolhido = np.random.choice(lista_vizinhos)
        vizinho_escolhido.calcular_fitness_rede(G)
        #print(f"Vizinho escolhido: {vizinho_escolhido.i}, {vizinho_escolhido.j}, {vizinho_escolhido.estrategia} com fitness {vizinho_escolhido.fitness}")
        
        prob_adotar = 1 / (1 + np.exp(- (vizinho_escolhido.fitness - self.fitness) / K))
        #print(f"Probabilidade de adotar: {prob_adotar:.4f}")

        if np.random.rand() < prob_adotar:
            #print(f"Adotou a estratégia do vizinho")
            return vizinho_escolhido.estrategia, vizinho_escolhido.n_vizinhos
        return self.estrategia, self.n_vizinhos

# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def vizinhos_unicos_rede(G, no):
    return list(set(G.predecessors(no)).union(set(G.successors(no))))

def criar_lagartos():
    lista = []
    for i in range(L):
        for j in range(L):
            estrategia = np.random.choice(estrategias)
            if estrategia == 'O':
                n_vizinhos = z_O
            elif estrategia == 'Y':
                n_vizinhos = z_Y
            elif estrategia == 'B':
                n_vizinhos = z_B
            lista.append(Lagarto(i, j, estrategia, 0, [], n_vizinhos))
    return lista

def calcular_freq_rede(G, estrategias):
    n = G.number_of_nodes()
    if n == 0:
        return np.zeros(len(estrategias), dtype=float)

    contagem = {e: 0 for e in estrategias}
    for lagarto in G.nodes:
        contagem[lagarto.estrategia] += 1

    return np.array([contagem[e] / n for e in estrategias], dtype=float)

def grau_unico(G, l):
    return len(set(G.predecessors(l)).union(set(G.successors(l))))

def media_vizinhos_rede(G, lista_lagartos):
    graus = [grau_unico(G, l) for l in lista_lagartos]
    return np.mean(graus) if len(graus) > 0 else np.nan

def media_vizinhos_por_estrategia_rede(G, lista_lagartos):
    medias = []
    for e in estrategias:
        graus = [grau_unico(G, l) for l in lista_lagartos if l.estrategia == e]
        medias.append(np.mean(graus) if len(graus) > 0 else np.nan)
    return medias


# ==============================
# SIMULAÇÃO
# ==============================

def simulacao(z_O, z_Y, z_B, fermi, K, sobreposicao, seed=None):
    resultados = []

    for pop in range(n_pop):
        if seed is not None:
            np.random.seed(seed + pop)
            
        G = nx.DiGraph()

        lista_lagartos = criar_lagartos()
        mapa = {(l.i, l.j): l for l in lista_lagartos}

        for lagarto in lista_lagartos:
            G.add_node(lagarto)

        for lagarto in lista_lagartos:
            lagarto.atualizar_links_lagarto(G, L, mapa)

        redes_geracoes = [copy.deepcopy(G)]
        
        matriz_posicao = np.empty((L, L), dtype=object)
        for l in lista_lagartos:
            matriz_posicao[l.i, l.j] = l.estrategia

        freq = calcular_freq_rede(G, estrategias)
        vizinhos_mean = media_vizinhos_rede(G, lista_lagartos)
        r_por_estrat = media_vizinhos_por_estrategia_rede(G, lista_lagartos)

        resultados.append({
            "pop": pop,
            "t": -1,
            "freq_O": freq[0],
            "freq_Y": freq[1],
            "freq_B": freq[2],
            "vizinhos_mean": vizinhos_mean,
            "z_O": z_O,
            "z_Y": z_Y,
            "z_B": z_B,
            "z_O_efetivo": r_por_estrat[0],
            "z_Y_efetivo": r_por_estrat[1],
            "z_B_efetivo": r_por_estrat[2],
            "sobreposicao": sobreposicao,
            "fermi": fermi,
            "K": K
        })

        for t in range(n_geracoes):
            print(f"População {pop+1} - Geração {t+1}/{n_geracoes}")

            mudancas = []
            for lagarto in lista_lagartos:
                lagarto.calcular_fitness_rede(G)
                estrategia_escolhida, vizinhanca_escolhida = lagarto.fermi_update(G, K)
                mudancas.append((lagarto, estrategia_escolhida, vizinhanca_escolhida))
            
            for lagarto, estrategia_escolhida, vizinhanca_escolhida in mudancas:
                    lagarto.estrategia = estrategia_escolhida
                    lagarto.n_vizinhos = vizinhanca_escolhida
                    lagarto.atualizar_links_lagarto(G, L, mapa)
            
            redes_geracoes.append(copy.deepcopy(G))

            for l in lista_lagartos:
                matriz_posicao[l.i, l.j] = l.estrategia

            freq = calcular_freq_rede(G, estrategias)
            vizinhos_mean = media_vizinhos_rede(G, lista_lagartos)
            r_por_estrat = media_vizinhos_por_estrategia_rede(G, lista_lagartos)

            resultados.append({
            "pop": pop,
            "t": t,
            "freq_O": freq[0],
            "freq_Y": freq[1],
            "freq_B": freq[2],
            "vizinhos_mean": vizinhos_mean,
            "z_O": z_O,
            "z_Y": z_Y,
            "z_B": z_B,
            "z_O_efetivo": r_por_estrat[0],
            "z_Y_efetivo": r_por_estrat[1],
            "z_B_efetivo": r_por_estrat[2],
            "sobreposicao": sobreposicao,
            "fermi": fermi,
            "K": K
            })

    return pd.DataFrame(resultados)

# ==============================
# RODAR
# ==============================

for z_O in range(z_O_inicial, z_O_inicial+5):
    for z_Y in range(z_Y_inicial, z_Y_inicial+5):
        df = simulacao(z_O=z_O, z_Y=z_Y, z_B=z_B, fermi=fermi, K=K, sobreposicao=sobreposicao, seed=1)
        df.to_csv(os.path.join(output_dir, f"results_zO{z_O}_zY{z_Y}.csv"), index=False)