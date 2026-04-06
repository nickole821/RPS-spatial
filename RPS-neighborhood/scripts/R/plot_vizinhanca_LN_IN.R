library(tidyverse)
library(ggtern)

data <- read_csv("outputs/vizinhanca_aprendizado-interacao/LN_diferente_IN_homogeneo/resultados_completos.csv")
head(data)
tail(data)

data$LN <- as.factor(data$LN)

campo_medio <- data.frame("freq_O" = c(0, 0.0487805, 0.205128, 0.378378, 0.336485, 1, 1),
                             "freq_Y" = c(0.444444, 0.390244, 0.358974, 0.324324, 0.440939, 0, 0),
                             "freq_B" = c(0.555556, 0.560976, 0.435897, 0.297297, 0.222576, 0, 0),
                             "custo" = c(0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4))
campo_medio

data_media <- data %>%
  group_by(t, custo, LN) %>%
  summarise(freq_O_media = mean(freq_O), sd_O = sd(freq_O),
            freq_B_media = mean(freq_B), sd_B = sd(freq_B),
            freq_Y_media = mean(freq_Y), sd_Y = sd(freq_Y))

data_media_t200 <- data_media %>%
  filter(t == 200, custo == 1)

data_media_t200

plot_Y <- filter(data_media, t == 200) %>%
  ggplot(aes(x = custo, y = freq_Y_media, colour = LN)) +
  geom_line() +
  geom_point() +
  geom_line(data = campo_medio, aes(x = custo, y = freq_Y, colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio, aes(x = custo, y = freq_Y, colour = "Mean field"),
             shape = 3, inherit.aes = FALSE) +
  labs(x = "Custo", y = "Frequência média de Y entre simulações (t = 200)")+
  scale_color_manual(values = c("8" = "#ffe169", "24" = "#6c757d", 
                                "48" = "#dbb42c", "80" = "#a47e1b",
                                "120" = "#76520e", "Mean field" = "black"))+
  theme_minimal()

plot_Y
ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_IN_homogeneo/plot_Y.png",
       plot_Y, width = 15, height = 10, units = "cm", dpi = 300)

plot_O <- filter(data_media, t == 200) %>%
  ggplot(aes(x = custo, y = freq_O_media, colour = LN)) +
  geom_line() +
  geom_point() +
  geom_line(data = campo_medio, aes(x = custo, y = freq_O, colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio, aes(x = custo, y = freq_O, colour = "Mean field"),
            shape = 3, inherit.aes = FALSE) +
  labs(x = "Custo", y = "Frequência média de O entre simulações (t = 200)")+
  scale_color_manual(values = c("8" = "#FFD8A8", "24" = "#6c757d", 
                                "48" = "#FFA94D", "80" = "#FF7A00",
                                "120" = "#8f250c",  "Mean field" = "black"))+
  theme_minimal()

plot_O
ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_IN_homogeneo/plot_O.png",
       plot_O, width = 15, height = 10, units = "cm", dpi = 300)

plot_B <- filter(data_media, t == 200) %>%
  ggplot(aes(x = custo, y = freq_B_media, colour = LN)) +
  geom_line() +
  geom_point() +
  geom_line(data = campo_medio, aes(x = custo, y = freq_B, colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio, aes(x = custo, y = freq_B, colour = "Mean field"),
             shape = 3, inherit.aes = FALSE) +
  labs(x = "Custo", y = "Frequência média de B entre simulações (t = 200)")+
  scale_color_manual(values = c("8" = "#ADE1FB", "24" = "#6c757d", 
                                "80" = "#266CA9", "48" = "#48cae4",
                                "120" = "#284b63", "Mean field" = "black"))+
  theme_minimal()

plot_B
ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_IN_homogeneo/plot_B.png",
       plot_B, width = 15, height = 10, units = "cm", dpi = 300)

data_permanencia <- data %>%
  group_by(custo, LN, t, pop) %>%
  summarise(permanencia_Y = ifelse(freq_Y > 0, 1, 0),
            permanencia_B = ifelse(freq_B > 0, 1, 0),
            permanencia_O = ifelse(freq_O > 0, 1, 0))
data_permanencia

data_permanencia_t200 <- data_permanencia %>%
  filter(t == 200) %>%
  mutate(permanencia_estrat = permanencia_Y + permanencia_B + permanencia_O)
data_permanencia_t200

teste <- data_permanencia_t200 %>%
  filter(custo == 1, LN == 8)

data_permanencia_t200_media <- data_permanencia_t200 %>%
  group_by(LN, custo, t) %>%
  summarise(media_permanencia = mean(permanencia_estrat), 
            sd_permanencia = sd(permanencia_estrat))
data_permanencia_t200_media

data_permanencia_t200_media %>%
  filter(custo == 1)

campo_medio_permanencia <- campo_medio %>%
  mutate(permanencia_Y = ifelse(freq_Y > 0, 1, 0),
         permanencia_B = ifelse(freq_B > 0, 1, 0),
         permanencia_O = ifelse(freq_O > 0, 1, 0)) %>%
  mutate(permanencia_estrat = permanencia_Y + permanencia_B + permanencia_O)
campo_medio_permanencia

plot_permanencia <- data_permanencia_t200_media %>%
  ggplot(aes(x = custo, y = media_permanencia, colour = LN)) +
  geom_line() +
  geom_point() +
  geom_line(data = campo_medio_permanencia, aes(x = custo, y = permanencia_estrat, 
                                                colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio_permanencia, aes(x = custo, y = permanencia_estrat,
                                                 colour = "Mean field"),
             shape = 3, inherit.aes = FALSE) +
  labs(x = "Custo", y = "Número de estratégias coexistindo\npor simulação no t = 200 (média entre réplicas)")+
  scale_color_manual(values = c("80" = "#2b9eb3", "24" = "#6c757d", 
                                "48" = "#f8333c", "8" = "#fcab10", 
                                "120" = "#a1cca5", "Mean field" = "black"))+
  theme_minimal()

plot_permanencia

ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_IN_homogeneo/plot_permanencia.png",
       plot_permanencia, width = 15, height = 10, units = "cm", dpi = 300)

dados_estado_final <- data %>%
  filter(t == 200) %>%
  mutate(
    pres_O = freq_O > 0.01,
    pres_Y = freq_Y > 0.01,
    pres_B = freq_B > 0.01,
    n_presentes = pres_O + pres_Y + pres_B,
    
    estado_final = case_when(
      n_presentes == 1 & pres_O ~ "O",
      n_presentes == 1 & pres_Y ~ "Y",
      n_presentes == 1 & pres_B ~ "B",
      
      n_presentes == 2 & !pres_O ~ "B e Y",
      n_presentes == 2 & !pres_Y ~ "B e O",
      n_presentes == 2 & !pres_B ~ "Y e O",
      
      n_presentes == 3 ~ "O, Y e B",
      
      TRUE ~ "nenhuma"
    )
  ) %>%
  count(custo, LN, estado_final) %>%
  group_by(custo, LN) %>%
  mutate(prop = n / sum(n))

plot_estado_final <- ggplot(dados_estado_final,
       aes(x = custo, y = prop, color = estado_final)) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  facet_wrap(~LN) +
  labs(
    x = "Custo",
    y = "Probabilidade",
    color = "Estado final"
  ) +
  scale_color_manual(values = c("B" = "#072ac8", "B e Y" = "#2b9348", 
                                "Y" = "#ffdd00", "O" = "#ff7b00", 
                                "O, Y e B" = "#db00b6")) +
  theme_minimal()

ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_IN_homogeneo/plot_estado_final.png",
       plot_estado_final, width = 20, height = 15, units = "cm", dpi = 300)