# set working directory
# setwd("/Users/Brian/Desktop/ds-project/Heart-Failure-Prediction")

# load data
library(readr)
heart_failure <- read_csv("heart_failure_clinical_records_dataset.csv")
# characteristics of data frame
summary(heart_failure)
# verify NA values
na_counts <- colSums(is.na(heart_failure))
print(na_counts)

# correlation matrix for "DEATH_EVENT"
correlation_matrix <- cor(heart_failure)
print(correlation_matrix)
installed.packages("corrplot")
library(corrplot)
corrplot(correlation_matrix, method = "color", type = "full", tl.srt = 45, 
         addCoef.col = "black", number.cex = 0.5, tl.cex = 0.8, 
         outline = TRUE)

summary(heart_failure$age)
summary(heart_failure$age[heart_failure$DEATH_EVENT == 0])
summary(heart_failure$age[heart_failure$DEATH_EVENT == 1])
# Grouped box plot of "age" for different death events 
library(ggplot2)
heart_failure$DEATH_EVENT <- as.factor(heart_failure$DEATH_EVENT)
ggplot(heart_failure, aes(x = DEATH_EVENT, y = age)) +
  geom_boxplot() +
  labs(title = "Grouped Box Plot of Age for Different Death Events",
       x = "Death Event",
       y = "Age") +
  theme_minimal()

# Grouped bar plot of "age" for different death events
heart_failure$DEATH_EVENT <- factor(heart_failure$DEATH_EVENT, labels = c("Alive", "Dead"))
heart_failure |>
  ggplot(aes(x = age)) +
  geom_bar(aes(fill = DEATH_EVENT), position = "dodge") +
  scale_fill_manual(values = c("blue", "red")) +
  labs(title = "Grouped Bar Plot of Age Distribution by Death Event", x = "Age", y = "Count") 

summary(heart_failure$ejection_fraction)
summary(heart_failure$ejection_fraction[heart_failure$DEATH_EVENT == 0])
summary(heart_failure$ejection_fraction[heart_failure$DEATH_EVENT == 1])
# Grouped box plot of "ejection_fraction" for different death events
library(ggplot2)
heart_failure$DEATH_EVENT <- as.factor(heart_failure$DEATH_EVENT)
ggplot(heart_failure, aes(x = DEATH_EVENT, y = ejection_fraction)) +
  geom_boxplot() +
  labs(title = "Grouped Box Plot of Ejection Fraction % for Different Death Events",
       x = "Death Event",
       y = "Ejection Fraction") +
  theme_minimal()

summary(heart_failure$serum_creatinine)
summary(heart_failure$serum_creatinine[heart_failure$DEATH_EVENT == 0])
summary(heart_failure$serum_creatinine[heart_failure$DEATH_EVENT == 1])
# Grouped box plot of "serum_creatinine" for different death events
library(ggplot2)
heart_failure$DEATH_EVENT <- as.factor(heart_failure$DEATH_EVENT)
ggplot(heart_failure, aes(x = DEATH_EVENT, y = serum_creatinine)) +
  geom_boxplot() +
  labs(title = "Grouped Box Plot of Serum Creatinine in mg/dL for Different Death Events",
       x = "Death Event",
       y = "Serum Creatinine") +
  theme_minimal() +
  theme(plot.title = element_text(size = 10))

summary(heart_failure$time)
summary(heart_failure$time[heart_failure$DEATH_EVENT == 0])
summary(heart_failure$time[heart_failure$DEATH_EVENT == 1])
# Grouped box plot of "time" for different death events
library(ggplot2)
heart_failure$DEATH_EVENT <- as.factor(heart_failure$DEATH_EVENT)
ggplot(heart_failure, aes(x = DEATH_EVENT, y = time)) +
  geom_boxplot() +
  labs(title = "Grouped Box Plot of Days for Different Death Events",
       x = "Death Event",
       y = "Days") +
  theme_minimal() +
  theme(plot.title = element_text(size = 10))


