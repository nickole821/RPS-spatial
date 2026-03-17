a ideia aqui é desacoplar a vizinhança de interação da vizinhança de aprendizado. a vizinhança de interação é com quem o agente interage para somar payoff. a vizinhança de aprendizado é para quem o agente olha na hora de "imitar", ou seja, de mudar de estratégia. 

a pasta learning_diferente basicamente mantem a vizinhança de interação de todas as estratégias iguais (24 vizinhos, moore de 2), e modifica apenas a vizinhança de aprendizado. nesse caso, o aprendizado de O e B fica 24, igual a de interação, e a vizinhança de Y que vai sendo modificada para verificar o que ocorre com as frequências.

a pasta XXX basicamente mantem a vizinhança de interação de todas as estratégias iguais (24 vizinhos, moore de 2), e modifica apenas a vizinhança de aprendizado. se mantem a mesma vizinhança de aprendizado para todas as estratégias. além disso, da matriz de payoff:
       O      Y      B
O      1     0.5     2
Y     2-c     1     2-c
B     0.5     2      1

vou mudando o c e vendo o que ocorre com a frequência de Y.