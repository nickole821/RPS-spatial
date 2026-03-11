ocorre sobreposição das gerações. ao invés de ir lagarto por lagarto na matriz, sorteia um e faz as ações com ele:
- calcula vizinhos
- calcula fitness com base nos vizinhos
- morre ou não a depender do fitness
	1 / (1 + A * np.exp(w * fitness))
- se morrer, ocupa qualquer vizinho

depois, sorteia outro lagarto (pode ser inclusive o da mesma posição. faz isso L^2 vezes.

tem um problema nesse código:
	se as vizinhanças não são iguais, eu não consigo manter a reciprocidade das interações. se eu sorteio um lagarto, eu sei quem são os seus vizinhos. mas como eu não sorteei outros lagartos ainda, eu não sei se um lagarto fora do raio de vizinhança tem esse lagarto focal como vizinho. 

RESOLVERIA USAR REDES??