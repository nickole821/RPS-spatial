nesse código, eu adiciono um custo fixo para as três estratégias para o aumento do raio de vizinhança (referente ao nome da pasta)

fitness = soma dos payoffs - (s * c * raio^2)

para O e B, s = 1, então sempre tem o custo associado à patrulha do território.

para Y, esse custo está associado não à patrulha, mas ao encontro com outros machos. se ele der sorte (parte estocástica, define a prob), ele consegue a fêmea e não paga custo nenhum (s = 0). se ele der azar, ele encontra um macho e paga o custo (s = 1). o custo de perambular está associado ao encontro ao não com outros machos, e isso depende de sorte.

prob = probabilidade de pagar o custo!!!