library(tidyverse)

data = read_csv("outputs/vizinhanca_aprendizado-interacao/LN_diferente_IN_homogeneo/resultados_completos.csv")
head(data)
tail(data)

data$LN <- as.factor(data$LN)

data_media <- data %>%
  group_by(t, custo, LN) %>%
  summarise(freq_O_media = mean(freq_O), sd_O = sd(freq_O),
            freq_B_media = mean(freq_B), sd_B = sd(freq_B),
            freq_Y_media = mean(freq_Y), sd_Y = sd(freq_Y))
data_media

plot <- filter(data_media, t == 200) %>%
  ggplot(aes(x = custo, y = freq_Y_media, colour = LN)) +
  geom_line() +
  geom_point() +
  labs(x = "Custo", y = "Frequência final de Y (t = 200)")+
  scale_color_manual(values = c("8" = "darkred", "24" = "black", 
                                "48" = "darkorange", "80" = "darkcyan", "120" = "purple"))+
  theme_minimal()

ggsave("outputs/vizinhanca_aprendizado-interacao/LN_diferente_IN_homogeneo/plot.png",
       plot, width = 15, height = 10, units = "cm", dpi = 300)
