library(tidyverse)
library(ggpubr)
library(readxl)

data=readxl::read_xlsx("genedata.xlsx")
data_long <- data %>%
  pivot_longer(-1, names_to = "Resistance_Category", values_to = "Frequency") %>%
  rename(Serotype = 1) %>%
  mutate(Avg_Frequency = Frequency)  # 如果没有平均值列，暂用原始值替代上色

data_long$Resistance_Category <- factor(data_long$Resistance_Category, levels = unique(colnames(data)[-1]))
data_long$Serotype <- factor(data_long$Serotype, levels = rev(unique(data_long$Serotype)))

ggplot(data_long, aes(x = Resistance_Category, y = Serotype)) + 
  geom_point(
    aes(
      size = Frequency,
      fill = Frequency,
      alpha = Frequency > 0  # 关键：0 值气泡透明
    ),
    shape = 21,
    color = "black"
  ) +
  scale_alpha_manual(values = c("TRUE" = 1, "FALSE" = 0), guide = "none") +  # 只显示非0的
  scale_size_continuous(
    range = c(1, 10),
    breaks = pretty(data_long$Frequency),
    guide = guide_legend(title = "Frequency")
  ) +
  scale_fill_distiller(palette = "Blues", direction = 1) +
  theme_bw() +
  theme(
    panel.background = element_blank(),
    panel.grid = element_blank(),
    panel.border = element_blank(),
    axis.line.x = element_line(color = "black", size = 0.8),
    axis.line.y = element_line(color = "black", size = 0.8),
    axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5, color = "black", size = 20),
    axis.text.y = element_text(color = "black", size = 15),
    axis.title = element_blank(),
    legend.title = element_text(size = 15),
    legend.text = element_text(size = 13)
  ) +
  labs(
    fill = "Frequency",
    size = "Frequency",
  )
library(svglite)
ggsave("C:/Users/93966/Desktop/genebubble_heatmap.svg", width = 12, height = 8, device = svglite)

