# RANDOM FOREST

# set working directory that suits you
# setwd("/Users/Brian/Desktop/ds-project/Heart-Failure-Prediction")

# Load data
library(readr)
hfdata <- read_csv("heart_failure_clinical_records_dataset.csv")

# Now we will split the data into test and training; we chose 70-30
# install.packages("rsample") run once
library(rsample)
set.seed(123)
health_split <- initial_split(hfdata,prop = 0.70)
train_data <- training(health_split)
test_data <- testing(health_split)

# Convert DEATH_EVENT to a factor for classification
train_data$DEATH_EVENT <- as.factor(train_data$DEATH_EVENT)
test_data$DEATH_EVENT <- as.factor(test_data$DEATH_EVENT)

# Subset train_data and test_data to include only relevant columns (data transformation)
relevant_columns <- c("age", "serum_creatinine", "ejection_fraction", "DEATH_EVENT")
train_data <- train_data[, relevant_columns]
test_data <- test_data[, relevant_columns]

# install packages and libraries for RANDOM FOREST
# install.packages("randomForest") run once
library(randomForest)
# install.packages("caret") run once
# install.packages("ggplot2") run once, required to load ggplot2 library
library(ggplot2) # required to load caret library
library(caret)

# build the Random Forest model and train it with train_data
rf_model <- randomForest(DEATH_EVENT ~ age + serum_creatinine + ejection_fraction, 
                         data = train_data, ntree = 500)

# Summary of the trained model with train_data
print(rf_model)
# error rate 22.97% and hence, accuracy 77.03

# Now apply the model to test_data (unseen) 
predictions <- predict(rf_model, test_data)

# Evaluate the model's performance on test_data
confusionMatrix(predictions, test_data$DEATH_EVENT)
# result: 0.7111 accuracy


# Stratified k-fold Cross-Validation on Random Forest

# set working directory that suits you
# setwd("/Users/Brian/Desktop/ds-project/Heart-Failure-Prediction")

# Load data
library(readr)
hfdata <- read_csv("heart_failure_clinical_records_dataset.csv")

# install.packages("caret") # run once
# install.packages("randomForest") # run once
# install.packages("ggplot2") # run once
library(ggplot2)
library(caret)
library(randomForest)

# we need DEATH_EVENT to be a factor
hfdata$DEATH_EVENT <- as.factor(hfdata$DEATH_EVENT)

# change DEATH_EVENT (factor) to 0 or 1 to valid R variable name
levels(hfdata$DEATH_EVENT) <- c("ALIVE", "DEAD")

# 10-fold cross-validation repeated 3 times
control <- trainControl(method = "repeatedcv", 
                        number = 10, 
                        repeats = 3,
                        classProbs = TRUE, 
                        summaryFunction = twoClassSummary)
set.seed(123)  # for reproducibility
# build the Stratified k-fold Cross-Validation model for Random Forest of whole data
cv_model_rf <- train(DEATH_EVENT ~ age + serum_creatinine + ejection_fraction,
                  data = hfdata,  
                  method = "rf", # random forest
                  trControl = control,
                  metric = "ROC")
print(cv_model_rf) # print the result





