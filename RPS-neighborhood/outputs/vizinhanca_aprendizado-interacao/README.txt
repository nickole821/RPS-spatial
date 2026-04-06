a ideia aqui é desacoplar a vizinhança de interação (IN) da vizinhança de aprendizado (LN). a vizinhança de interação é com quem o agente interage para somar payoff. a vizinhança de aprendizado é para quem o agente olha na hora de "imitar", ou seja, de mudar de estratégia. 

a pasta LN_diferente_Y basicamente mantem a vizinhança de interação de todas as estratégias iguais (24 vizinhos, moore de 2), e modifica apenas a vizinhança de aprendizado. nesse caso, o aprendizado de O e B fica 24, igual a de interação, e a vizinhança de Y que vai sendo modificada para verificar o que ocorre com as frequências.

	dentro dela, tem duas pastas: 
	matriz_1-c utiliza a matriz de payoff
	       O      Y      B
	O      1     0.5     2
	Y     1+c     1     1-c
	B     0.5     2      1

	e matriz_2-c utiliza a matriz:
	       O      Y      B
	O      1     0.5     2
	Y     2-c     1     2-c
	B     0.5     2      1

	dentro delas, tem os diferentes valores de LN e os 	diferentes valores de c atribuídos nas simulações.

a pasta LN_igual basicamente mantem a vizinhança de interação de todas as estratégias iguais (24 vizinhos, moore de 2), e modifica apenas a vizinhança de aprendizado. se mantem a mesma vizinhança de aprendizado para todas as estratégias. 

	as pastas internas são idênticas às da outra pasta