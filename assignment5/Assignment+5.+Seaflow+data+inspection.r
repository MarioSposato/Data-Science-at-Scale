
#This notebook provides the solutions for the assignment 5 of the Data Science at Scale course on Coursera.
#In the assignment, a database with sensor readings from the SeaFlow environmental flow cytometry instrument is given,
#and a classification of the various particles is requested.

part <- read.csv("seaflow_21min.csv")

summary(part)

library(caret)

#Creation of a partition index for the dataset

idx<-createDataPartition(part$pop,
  p = 0.5,
  list = FALSE)

train <- part[idx, ]
test <- part[-idx, ]

head(train)
head(test)

str(train)

ggplot(part, aes(chl_small, pe, color=pop))+geom_point()

mean(train$time)

#Creation of a formula for the model

fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)

library(rpart)

model <- rpart(fol, method="class", data=train)

print(model)

eval_test <- predict(model, test, type = "class", list=FALSE)

#Accuracy of the model

m_accuracy=sum(test$pop==eval_test)/36171

library(randomForest)

#Creation of a random forest model

model_rnd <- randomForest(fol, data=train)

eval_test_rnd <- predict(model_rnd, test, type = "class", list=FALSE)
rnd_accuracy=sum(test$pop==eval_test_rnd)/36171
importance(model)

#Creation of a SVM classifier

library(e1071)
model_svm <- svm(fol, data=train)

eval_test_svm <- predict(model_svm, test, type = "class", list=FALSE)
svm_accuracy=sum(test$pop==eval_test_svm)/36171

#Confusion Matrices for the three models

table(pred=eval_test, true=test$pop)
table(pred=eval_test_rnd, true=test$pop)
table(pred=eval_test_svm, true=test$pop)

#Check for continuos variables

apply(test, 2, function(x) length(unique(x)))

library(dplyr)

#Data cleaning of a broken sensor

new_part<-part %>% filter(file_id!=208)

idx<-createDataPartition(new_part$pop,
  p = 0.5,
  list = FALSE)
ntrain <- new_part[idx, ]
ntest <- new_part[-idx, ]

model_svm_c <- svm(fol, data=ntrain)
eval_test_svm_c <- predict(model_svm_c, test, type = "class", list=FALSE)
svm_c_accuracy=sum(test$pop==eval_test_svm_c)/36171

svm_c_accuracy-svm_accuracy


