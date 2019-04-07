library(tidyverse)
library(ramify)
library(stringr)
library(arules)
library(arulesViz)

data = as_tibble(read.csv("../../Data/train.csv"))
categorical_columns = c("Soil_Type", "Wilderness_Area")
data = data %>% select(-"Id")


for (categorical_column in categorical_columns) {
  categorical_data = data %>% select(starts_with(categorical_column))
  types = colnames(categorical_data)[apply(categorical_data,1,which.max)]
  data = data %>% select(-starts_with(categorical_column))
  data[categorical_column] = types
}

target = c("Cover_Type")
numerical_columns = setdiff(setdiff(colnames(data), target), categorical_columns)

for (numerical_column in numerical_columns) {
  data[numerical_column] = ordered(cut(data[[numerical_column]], 3, dig.lab=10))
}

# data[numerical_columns] = Map(paste, names(data[numerical_columns]), data[numerical_columns], sep = '')
data[target] = Map(paste, names(data[target]), data[target], sep = '')

data[[target]] = factor(data[[target]])
data[['Soil_Type']] = factor(data[['Soil_Type']])
data[['Wilderness_Area']] = factor(data[['Wilderness_Area']])

str(data)

transactions = as(data, "transactions")
rules = apriori(transactions, parameter = list(support=0.07, confidence=0.7), appearance = list(rhs=paste0("Cover_Type=", unique(data$Cover_Type))))
inspect(rules)