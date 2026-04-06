essa pasta testa a sensibilidade do modelo aos diferentes números de vizinhos das estratégias.

vizinhosY_e_B testa a sensibilidade mudando o números de vizinhos de Y e B. o número de vizinhos de 8 fica fixo em 8 em todas as simulações. são rodadas 100 simulações (verificar) até o tempo t = 100, para verificar as frequências finais médias (arquivo frequencias_sensibilidades_vizinhosY_e_B.csv).

	além disso, eu também calculei quantas estratégias eram 	mantidas na geração t = 100 na média para as 100 simulações 	(manutencao_media_todas.csv). e também calculei a 	probabilidade de ter 3 estratégias no tempo t = 100 (pela 	frequência que isso acontece nas 100 simulações). por fim, 	eu calculei qual a proporção de simulações que mantinha 	cada estratégia (por exemplo, 100% das simulações y = 1 e b 	= 1 mantinham Y e B na população). 

	é importante frisar que os valores do nº de vizinhos foram 	estabelecidos no início da simulação, porém, como as 	interações são recíprocas, eles podem ser levemente 	diferentes dos estabelecidos (especialmente para 	estratégias com o menor número de vizinhos). 

vizinhosY_e_O faz o mesmo porém mantendo B = 8 e modificando Y e O.