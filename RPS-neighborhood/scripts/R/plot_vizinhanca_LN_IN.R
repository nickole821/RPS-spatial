library(tidyverse)
library(ggtern)
library(cowplot)

data <- read_csv("outputs/vizinhanca_aprendizado-interacao/LN_igual/matriz_1-c/resultados_completos.csv")
head(data)
tail(data)

data$LN <- as.factor(data$LN)

campo_medio <- data.frame("freq_O" = c(1, 1, 0.338405, 0.517859, 0.490047, 0.467648, 0.45068, 0.437501, 0.426971, 0.418366, 0.411214, 0.405173, 0.399999),
                          "freq_Y" = c(0, 0, 0.445464, 0.299715, 0.301992, 0.306475, 0.309878, 0.312506, 0.314604, 0.316326, 0.317758, 0.318965, 0.32),
                          "freq_B" = c(0, 0, 0.216131, 0.555556, 0.207961, 0.225877, 0.239442, 0.249993, 0.258426, 0.265308, 0.271027, 0.275862, 0.28),
                          "custo" = c(-0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
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
  #geom_ribbon(aes(ymin = freq_Y_media - sd_Y, ymax = freq_Y_media + sd_Y), alpha = 0.3) +
  geom_line(data = campo_medio, aes(x = custo, y = freq_Y, colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio, aes(x = custo, y = freq_Y, colour = "Mean field"),
             shape = 3, inherit.aes = FALSE) +
  labs(x = "a", y = "Mean frequency of Y (t = 200)")+
  scale_color_manual(values = c("8" = "#ffe169", "24" = "#6c757d", 
                                "48" = "#dbb42c", "80" = "#a47e1b",
                                "120" = "#76520e", "Mean field" = "black"))+
  #scale_fill_manual(values = c("8" = "#ffe169", "24" = "#6c757d", 
                                #"48" = "#dbb42c", "80" = "#a47e1b",
                                #"120" = "#76520e", "Mean field" = "black"))+
  theme_minimal() +
  scale_y_continuous(limits = c(0,1))

plot_Y
ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_Y/matriz_1-c/plot_Y.png",
       plot_Y, width = 15, height = 10, units = "cm", dpi = 300)

plot_O <- filter(data_media, t == 200) %>%
  ggplot(aes(x = custo, y = freq_O_media, colour = LN)) +
  geom_line() +
  geom_point() +
  geom_line(data = campo_medio, aes(x = custo, y = freq_O, colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio, aes(x = custo, y = freq_O, colour = "Mean field"),
             shape = 3, inherit.aes = FALSE) +
  labs(x = "a", y = "Mean frequency of O (t = 200)")+
  scale_color_manual(values = c("8" = "#FFD8A8", "24" = "#6c757d", 
                                "48" = "#FFA94D", "80" = "#FF7A00",
                                "120" = "#8f250c",  "Mean field" = "black"))+
  theme_minimal() +
  scale_y_continuous(limits = c(0,1))

plot_O
ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_Y/matriz_1-c/plot_O.png",
       plot_O, width = 15, height = 10, units = "cm", dpi = 300)

plot_B <- filter(data_media, t == 200) %>%
  ggplot(aes(x = custo, y = freq_B_media, colour = LN)) +
  geom_line() +
  geom_point() +
  geom_line(data = campo_medio, aes(x = custo, y = freq_B, colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio, aes(x = custo, y = freq_B, colour = "Mean field"),
             shape = 3, inherit.aes = FALSE) +
  labs(x = "a", y = "Mean frequency of B (t = 200)")+
  scale_color_manual(values = c("8" = "#ADE1FB", "24" = "#6c757d", 
                                "80" = "#266CA9", "48" = "#48cae4",
                                "120" = "#284b63", "Mean field" = "black"))+
  theme_minimal() +
  scale_y_continuous(limits = c(0,1))

plot_B
ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_Y/matriz_1-c/plot_B.png",
       plot_B, width = 15, height = 10, units = "cm", dpi = 300)


data_media_long <- data_media %>%
  rename(freq_O = freq_O_media, freq_B = freq_B_media, freq_Y = freq_Y_media) 
data_media_long <- data_media_long %>%
  pivot_longer(
    cols = c(freq_O, sd_O,
             freq_B, sd_B,
             freq_Y, sd_Y),
    names_to = c(".value", "estrategia"),
    names_pattern = "(freq|sd)_(.*)")
data_media_long$estrategia <- as.factor(data_media_long$estrategia)

campo_medio_long <- campo_medio %>%
  pivot_longer(cols = c(freq_O, freq_Y, freq_B), 
               names_to = c(".value", "estrategia"),
               names_pattern = "(freq)_(.*)")

plot_grid <- data_media_long %>%
  filter(t == 200) %>%
  ggplot(aes(x = custo, y = freq, shape = LN, colour = LN))+
  geom_point() +
  geom_line() +
  geom_line(data = campo_medio_long, 
            aes(x = custo, y = freq, shape = "Mean field", colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio_long, 
             aes(x = custo, y = freq, shape = "Mean field", colour = "Mean field"),
             inherit.aes = FALSE)+
  facet_wrap(~estrategia) +
  scale_color_manual(values = c(
    "8" = "#fcab10",
    "24" = "#6c757d",
    "48" = "#f8333c",
    "80" = "#2b9eb3",
    "120" = "#a1cca5",
    "Mean field" = "black"
  )) +
  scale_shape_manual(values = c(
    "8" = 16,
    "24" = 17,
    "48" = 15,
    "80" = 18,
    "120" = 3,
    "Mean field" = 8
  )) +
  theme_minimal(base_size = 12) +
  labs(x = "a", y = "Mean frequency of strategy (t = 200)",
       colour = "Number of\nlearning neighbours", shape = "Number of\nlearning neighbours") +
  theme(
    axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1)
  )

plot_grid
ggsave("outputs/vizinhanca_aprendizado-interacao/LN_igual/matriz_1-c/plot_grid.png",
       plot_grid, width = 20, height = 10, units = "cm", dpi = 800)

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
  ggplot(aes(x = custo, y = media_permanencia, colour = LN, shape = LN)) +
  geom_line() +
  geom_point() +
  geom_line(data = campo_medio_permanencia, aes(x = custo, y = permanencia_estrat, 
                                                shape = "Mean field", colour = "Mean field"),
            inherit.aes = FALSE) +
  geom_point(data = campo_medio_permanencia, aes(x = custo, y = permanencia_estrat,
                                                 shape = "Mean field", colour = "Mean field"),
             inherit.aes = FALSE) +
  labs(x = "a", y = "Mean number os coexisting\nstrategies in t = 200",
       colour = "Number of\nlearning neighbours", shape = "Number of\nlearning neighbours")+
  scale_color_manual(values = c(
    "8" = "#fcab10",
    "24" = "#6c757d",
    "48" = "#f8333c",
    "80" = "#2b9eb3",
    "120" = "#a1cca5",
    "Mean field" = "black"
  )) +
  scale_shape_manual(values = c(
    "8" = 16,
    "24" = 17,
    "48" = 15,
    "80" = 18,
    "120" = 3,
    "Mean field" = 8
  )) +
  theme_minimal(base_size = 12) +
  scale_y_continuous(limits = c(0,3)) +
  theme(
    axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1)
  )

plot_permanencia

ggsave("outputs/vizinhanca_aprendizado-interacao/LN_igual/matriz_1-c/plot_permanencia.png",
       plot_permanencia, width = 20, height = 10, units = "cm", dpi = 800)
