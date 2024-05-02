# LOGISTIC REGRESSION

# set working directory that suits you
# setwd("/Users/Brian/Desktop/ds-project/Heart-Failure-Prediction")

# Load data
library(readr)
hfdata <- read_csv("heart_failure_clinical_records_dataset.csv")

#Now we will split the data into test and training we chose 70-30
# install.packages("rsample") run once
library(rsample)
set.seed(123)
health_split <- initial_split(hfdata,prop = 0.70)
train_data <- training(health_split)
test_data <- testing(health_split)

# Convert DEATH_EVENT to a factor for classification (data transformation)
train_data$DEATH_EVENT <- as.factor(train_data$DEATH_EVENT)
test_data$DEATH_EVENT <- as.factor(test_data$DEATH_EVENT)

# Subset train_data and test_data to include only relevant columns (data transformation)
relevant_columns <- c("age", "serum_creatinine", "ejection_fraction", "DEATH_EVENT")
train_data <- train_data[, relevant_columns]
test_data <- test_data[, relevant_columns]

# Perform logistic regression on the train_data
log_reg_model <- glm(DEATH_EVENT ~ age + serum_creatinine + ejection_fraction, 
                     data = train_data, 
                     family = binomial())
# summary of logistic regression model
summary(log_reg_model)
# apply the model on the test_data
log_reg_pred <- predict(log_reg_model, newdata = test_data, type = "response")
# install.packages("pROC") run once
library(pROC)
roc_curve <- roc(test_data$DEATH_EVENT, log_reg_pred)
plot(roc_curve, main = "ROC Curve", col = "blue")
auc_result <- auc(roc_curve)
legend("bottomright", legend = paste("AUC =", round(auc_result, 2)), col = "blue", lty = 1, cex = 0.8)


# Stratified k-fold Cross-Validation on Logistic Regression

# Set working directory that suits you
# setwd("/Users/Brian/Desktop/ds-project/Heart-Failure-Prediction")

# Load data
library(readr)
hfdata <- read_csv("heart_failure_clinical_records_dataset.csv")

# install.packages("caret") # run once
library(ggplot2)
library(caret)

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
set.seed(123) # for reproducibility
# build the Stratified k-fold Cross-Validation model for Logistic Regression of whole data
cv_model_logReg <- train(DEATH_EVENT ~ age + serum_creatinine + ejection_fraction,
               data = hfdata, 
               method = "glm", # logistic regression
               family = "binomial",
               trControl = control,
               preProcess = c("center", "scale"),
               metric = "ROC")
print(cv_model_logReg) # print the result


