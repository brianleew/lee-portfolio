
library(readr)
heart_failure <- read_csv("heart_failure_clinical_records_dataset.csv")
na_counts <- colSums(is.na(heart_failure))
print(na_counts)

View(heart_failure)
correlation_matrix <- cor(heart_failure)
print(correlation_matrix)
installed.packages("corrplot")
library(corrplot)
corrplot(correlation_matrix, method = "color", type = "full", tl.srt = 45, 
         addCoef.col = "black", number.cex = 0.5, tl.cex = 0.8, 
         outline = TRUE)
# So as we can see from the matrix age, ejection_fraction, serum_creatine
#are all the highest correlated with death_event so its what we'll build our
#model off of
library(ggplot2)
summary(heart_failure$age)
heart_failure$DEATH_EVENT <- as.factor(heart_failure$DEATH_EVENT)
ggplot(heart_failure, aes(x = DEATH_EVENT, y = age)) +
  geom_boxplot() +
  labs(title = "Boxplots of Age for Different Death Events",
       x = "Death Event",
       y = "Age") +
  theme_minimal()

summary(heart_failure$ejection_fraction)
heart_failure |> 
  ggplot(aes(x = ejection_fraction)) +
  geom_bar()
heart_failure |> 
  ggplot(aes(x = ejection_fraction)) +
  geom_boxplot()
heart_failure |>
  ggplot(aes(x = ejection_fraction)) +
  geom_boxplot(aes(fill = DEATH_EVENT), position = "dodge") +
  scale_fill_manual(values = c("blue", "red")) +
  labs(title = "Box plot of Ejection Fraction and Death Event", x = "Ejection Fraction", y = "Count")
heart_failure |>
  ggplot(aes(x = DEATH_EVENT, y = ejection_fraction, fill = DEATH_EVENT)) +
  geom_violin() +
  scale_fill_manual(values = c("blue", "red")) +
  labs(title = "Violin plot of Ejection Fraction and Death Event", x = "Death Event", y = "Ejection Fraction")
# we do have outliers but our outliers have meaning so itll be good to keep them
# More alive people have the normal ejection fraction while more dead people have
#the abnormal values
summary(heart_failure$serum_creatinine)
heart_failure |> 
  ggplot(aes(x = serum_creatinine)) +
  geom_bar()
heart_failure |> 
  ggplot(aes(x = serum_creatinine)) +
  geom_boxplot()
heart_failure |>
  ggplot(aes(x = serum_creatinine)) +
  geom_boxplot(aes(fill = DEATH_EVENT), position = "dodge") +
  scale_fill_manual(values = c("blue", "red")) +
  labs(title = "Box plot of Serum Creatinine and Death Event", x = "Serum Creatinine", y = "Count")
heart_failure |>
  ggplot(aes(x = DEATH_EVENT, y = serum_creatinine, fill = DEATH_EVENT)) +
  geom_violin() +
  scale_fill_manual(values = c("blue", "red")) +
  labs(title = "Violin plot of Serum Creatinine and Death Event", x = "Death Event", y = "Serum Creatinine")
#more alive people are around 1 mg/dL and more dead people are 2-3 mg/DL
heart_failure$DEATH_EVENT <- factor(heart_failure$DEATH_EVENT, labels = c("Alive", "Dead"))
heart_failure |>
  ggplot(aes(x =time )) +
  geom_bar(aes(fill = DEATH_EVENT), position = "dodge") +
  scale_fill_manual(values = c("blue", "red")) 



#Now we will split the data into test and training we chose 70-30
install.packages("rsample")
library(rsample)
set.seed(123)
health_split <- initial_split(heart_failure,prop = 0.70)
train_data <- training(health_split)
test_data <- testing(health_split)

#Now to build our Logistic Regression model
#set Death Event as binary
heart_failure$DEATH_EVENT <- ifelse(heart_failure$DEATH_EVENT == "Dead",1,0)
#Graph the observations
heart_failure |> ggplot(aes(x=age, y=DEATH_EVENT)) +
  geom_point(cex = 4) +
  labs(x = "Age", y = "Probability that someone dies")
heart_failure |>
  ggplot(aes(x=age, y=DEATH_EVENT)) +
  geom_point(cex = 4) +
  labs(x = "Age", y = "Probability that someone dies") +
  geom_smooth(formula = y ~ x, method = "glm", 
              method.args = list(family = "binomial"), se = FALSE)
heart_failure |> ggplot(aes(x=serum_creatinine, y=DEATH_EVENT)) +
  geom_point(cex = 4) +
  labs(x = "Serum Creatinine", y = "Probability that someone dies")
heart_failure |>
  ggplot(aes(x=serum_creatinine, y=DEATH_EVENT)) +
  geom_point(cex = 4) +
  labs(x = "serum_creatinine", y = "Probability that someone dies") +
  geom_smooth(formula = y ~ x, method = "glm", 
              method.args = list(family = "binomial"), se = FALSE)
heart_failure |> ggplot(aes(x=ejection_fraction, y=DEATH_EVENT)) +
  geom_point(cex = 4) +
  labs(x = "Ejection Fraction", y = "Probability that someone dies")
heart_failure |>
  ggplot(aes(x=ejection_fraction, y=DEATH_EVENT)) +
  geom_point(cex = 4) +
  labs(x = "ejection_fraction", y = "Probability that someone dies") +
  geom_smooth(formula = y ~ x, method = "glm", 
              method.args = list(family = "binomial"), se = FALSE)
#build the model off of our 3 variables
logisticModel <- glm(DEATH_EVENT ~ age + ejection_fraction + serum_creatinine, data = train_data, family = "binomial")
summary(logisticModel)
#
predictions <- predict(logisticModel, newdata = test_data, type = "response")
install.packages("pROC")
library(pROC)
roc_curve <- roc(test_data$DEATH_EVENT, predictions)
plot(roc_curve, main = "ROC Curve", col = "blue")
auc_result <- auc(roc_curve)
legend("bottomright", legend = paste("AUC =", round(auc_result, 2)), col = "blue", lty = 1, cex = 0.8)

ggplot(test_data, aes(x = age, y = predictions, color = DEATH_EVENT)) +
  geom_point(size = 4) +
  labs(x = "Age", y = "Predicted Probability") +
  geom_smooth(formula = y ~ x, method = "glm", 
              method.args = list(family = "binomial"), se = FALSE)
ggplot(test_data, aes(x = serum_creatinine, y = predictions, color = DEATH_EVENT)) +
  geom_point(size = 4) +
  labs(x = "serum_creatinine", y = "Predicted Probability") +
  geom_smooth(formula = y ~ x, method = "glm", 
              method.args = list(family = "binomial"), se = FALSE)
ggplot(test_data, aes(x = ejection_fraction, y = predictions, color = DEATH_EVENT)) +
  geom_point(size = 4) +
  labs(x = "ejection_fraction", y = "Predicted Probability") +
  geom_smooth(formula = y ~ x, method = "glm", 
              method.args = list(family = "binomial"), se = FALSE)

# random forest
library(rsample)
install.packages("randomForest")
library(randomForest)
install.packages("caret")
library(caret)
#
rfDataFrame <- subset(heart_failure, select = -c(time)) # creates a new df without time
rfDataFrame$DEATH_EVENT <- as.factor(rfDataFrame$DEATH_EVENT)
set.seed(1)
train <- sample(1:nrow(rfDataFrame), 209) # separates the data for training and testing 
train_data <- rfDataFrame[train,] # gets 209 objects for training data
test_data <- rfDataFrame[-train,] # gets the remaining 90 objects in the data frame

rf <- randomForest(DEATH_EVENT ~., data = train_data)

rfPrediction <- predict(rf, train_data)
cm <- confusionMatrix(rfPrediction, train_data$DEATH_EVENT)

rfTest <- predict(rf, test_data)
rfConfMat <- confusionMatrix(rfTest, test_data$DEATH_EVENT)
rfAccuary <- sum(diag(rfConfMat$table)) / sum(rfConfMat$table)
rfAccuary

importance_df <- as.data.frame(importance(rf))
importance_df$variable <- rownames(importance_df)
ggplot(importance_df, aes(x = reorder(variable, MeanDecreaseGini), y = MeanDecreaseGini)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  labs(title = "Variable Importance in Random Forest") +
  xlab("Variable") +
  ylab("Variable Importance in Model") +
  theme_minimal()


install.packages("class") 

# Loading package 
library(class) 


set.seed(42)  # for reproducibility
train_indices <- sample(1:nrow(heart_failure), 0.7 * nrow(heart_failure))  # 70% for training
train_data <- heart_failure[train_indices, ]
test_data <- heart_failure[-train_indices, ]

# Features (X) and target variable (y) for training
X_train <- train_data[, c("age", "ejection_fraction", "serum_creatinine")]  # Adjust feature names
y_train <- train_data$DEATH_EVENT

# Features (X) and target variable (y) for testing
X_test <- test_data[, c("age", "ejection_fraction", "serum_creatinine")]  # Adjust feature names
y_test <- test_data$DEATH_EVENT

# Choose the number of neighbors (k)
k <- 5

# Train the KNN model
knn_model <- knn(train = X_train, test = X_test, cl = y_train, k = k)

# Evaluate the model
accuracy <- sum(knn_model == y_test) / length(y_test)
conf_matrix <- table(knn_model, y_test)

print(paste("Accuracy:", accuracy))
print("Confusion Matrix:")
print(conf_matrix)

# Baseline Model Naive Bayes
library(e1071)
set.seed(123)
health_split <- initial_split(heart_failure,prop = 0.70)
train_data <- training(health_split)
test_data <- testing(health_split)
model <- naiveBayes(DEATH_EVENT ~ age + ejection_fraction + serum_creatinine, data = heart_failure, usekernel = T) 
#train data 
p <- predict(model, train_data, type = 'class')

p1 <- predict(model, train_data)
(tab1 <- table(p1, train_data$DEATH_EVENT))
1 - sum(diag(tab1)) / sum(tab1)
#Test data 
p2 <- predict(model, test_data)
(tab2 <- table(p2, test_data$DEATH_EVENT))
1 - sum(diag(tab2)) / sum(tab2)
# Our baseline Model has 70-78% accuracy on the test data
