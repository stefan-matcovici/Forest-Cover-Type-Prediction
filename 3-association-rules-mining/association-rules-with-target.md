### Imports

    library(tidyverse)
    library(ramify)
    library(stringr)
    library(arules)
    library(arulesViz)

### Load data and extract columns by type. Remove Id column.

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

### Change columns to factors and discretisize numerical columns

    for (numerical_column in numerical_columns) {
      data[numerical_column] = ordered(cut(data[[numerical_column]], 3, dig.lab=10))
    }

    data[target] = Map(paste, names(data[target]), data[target], sep = '')

    data[[target]] = factor(data[[target]])
    data[['Soil_Type']] = factor(data[['Soil_Type']])
    data[['Wilderness_Area']] = factor(data[['Wilderness_Area']])

    print(str(data))

    ## Classes 'tbl_df', 'tbl' and 'data.frame':    15120 obs. of  13 variables:
    ##  $ Elevation                         : Ord.factor w/ 3 levels "(1861.014,2525]"<..: 2 2 2 2 2 2 2 2 2 2 ...
    ##  $ Aspect                            : Ord.factor w/ 3 levels "(-0.36,120]"<..: 1 1 2 2 1 2 1 1 1 1 ...
    ##  $ Slope                             : Ord.factor w/ 3 levels "(-0.052,17.33333333]"<..: 1 1 1 2 1 1 1 1 1 1 ...
    ##  $ Horizontal_Distance_To_Hydrology  : Ord.factor w/ 3 levels "(-1.343,447.6666667]"<..: 1 1 1 1 1 1 1 1 1 1 ...
    ##  $ Vertical_Distance_To_Hydrology    : Ord.factor w/ 3 levels "(-146.7,87.33333333]"<..: 1 1 1 2 1 1 1 1 1 1 ...
    ##  $ Horizontal_Distance_To_Roadways   : Ord.factor w/ 3 levels "(-6.89,2296.666667]"<..: 1 1 2 2 1 1 1 1 1 1 ...
    ##  $ Hillshade_9am                     : Ord.factor w/ 3 levels "(-0.254,84.66666667]"<..: 3 3 3 3 3 3 3 3 3 3 ...
    ##  $ Hillshade_Noon                    : Ord.factor w/ 3 levels "(98.845,150.6666667]"<..: 3 3 3 3 3 3 3 3 3 3 ...
    ##  $ Hillshade_3pm                     : Ord.factor w/ 3 levels "(-0.248,82.66666667]"<..: 2 2 2 2 2 2 2 2 2 2 ...
    ##  $ Horizontal_Distance_To_Fire_Points: Ord.factor w/ 3 levels "(-6.993,2331]"<..: 3 3 3 3 3 3 3 3 3 3 ...
    ##  $ Cover_Type                        : Factor w/ 7 levels "Cover_Type1",..: 5 5 2 2 5 2 5 5 5 5 ...
    ##  $ Soil_Type                         : Factor w/ 38 levels "Soil_Type1","Soil_Type10",..: 21 21 4 23 21 21 21 21 21 21 ...
    ##  $ Wilderness_Area                   : Factor w/ 4 levels "Wilderness_Area1",..: 1 1 1 1 1 1 1 1 1 1 ...
    ## NULL

    transactions = as(data, "transactions")

### 

    rules = apriori(transactions, parameter = list(support=0.07, confidence=0.7), appearance = list(rhs=paste0("Cover_Type=", unique(data$Cover_Type))))

    ## Apriori
    ## 
    ## Parameter specification:
    ##  confidence minval smax arem  aval originalSupport maxtime support minlen
    ##         0.7    0.1    1 none FALSE            TRUE       5    0.07      1
    ##  maxlen target   ext
    ##      10  rules FALSE
    ## 
    ## Algorithmic control:
    ##  filter tree heap memopt load sort verbose
    ##     0.1 TRUE TRUE  FALSE TRUE    2    TRUE
    ## 
    ## Absolute minimum support count: 1058 
    ## 
    ## set item appearances ...[7 item(s)] done [0.00s].
    ## set transactions ...[79 item(s), 15120 transaction(s)] done [0.01s].
    ## sorting and recoding items ... [35 item(s)] done [0.00s].
    ## creating transaction tree ... done [0.01s].
    ## checking subsets of size 1 2 3 4 5 6 7 8 9 10

    ## Warning in apriori(transactions, parameter = list(support = 0.07,
    ## confidence = 0.7), : Mining stopped (maxlen reached). Only patterns up to a
    ## length of 10 returned!

    ##  done [0.04s].
    ## writing ... [14 rule(s)] done [0.00s].
    ## creating S4 object  ... done [0.00s].

    inspect(rules)

    ##      lhs                                                            rhs                         support confidence     lift count
    ## [1]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Horizontal_Distance_To_Roadways=(2296.666667,4593.333333]} => {Cover_Type=Cover_Type7} 0.07433862  0.7322476 5.125733  1124
    ## [2]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Wilderness_Area=Wilderness_Area3}                          => {Cover_Type=Cover_Type7} 0.08822751  0.7562358 5.293651  1334
    ## [3]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Hillshade_3pm=(82.66666667,165.3333333]}                   => {Cover_Type=Cover_Type7} 0.09682540  0.7055422 4.938795  1464
    ## [4]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Horizontal_Distance_To_Roadways=(2296.666667,4593.333333],                                                                 
    ##       Hillshade_9am=(169.3333333,254.254]}                       => {Cover_Type=Cover_Type7} 0.07175926  0.7436600 5.205620  1085
    ## [5]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Hillshade_Noon=(202.3333333,254.155],                                                                                      
    ##       Wilderness_Area=Wilderness_Area3}                          => {Cover_Type=Cover_Type7} 0.07843915  0.7477932 5.234552  1186
    ## [6]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Hillshade_9am=(169.3333333,254.254],                                                                                       
    ##       Wilderness_Area=Wilderness_Area3}                          => {Cover_Type=Cover_Type7} 0.08551587  0.7605882 5.324118  1293
    ## [7]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Slope=(-0.052,17.33333333],                                                                                                
    ##       Hillshade_3pm=(82.66666667,165.3333333]}                   => {Cover_Type=Cover_Type7} 0.07969577  0.7018055 4.912638  1205
    ## [8]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Hillshade_Noon=(202.3333333,254.155],                                                                                      
    ##       Hillshade_3pm=(82.66666667,165.3333333]}                   => {Cover_Type=Cover_Type7} 0.08842593  0.7085321 4.959724  1337
    ## [9]  {Elevation=(3187,3850.986],                                                                                                 
    ##       Hillshade_9am=(169.3333333,254.254],                                                                                       
    ##       Hillshade_3pm=(82.66666667,165.3333333]}                   => {Cover_Type=Cover_Type7} 0.09596561  0.7053962 4.937773  1451
    ## [10] {Elevation=(3187,3850.986],                                                                                                 
    ##       Hillshade_9am=(169.3333333,254.254],                                                                                       
    ##       Hillshade_Noon=(202.3333333,254.155],                                                                                      
    ##       Wilderness_Area=Wilderness_Area3}                          => {Cover_Type=Cover_Type7} 0.07665344  0.7521090 5.264763  1159
    ## [11] {Elevation=(3187,3850.986],                                                                                                 
    ##       Slope=(-0.052,17.33333333],                                                                                                
    ##       Hillshade_Noon=(202.3333333,254.155],                                                                                      
    ##       Hillshade_3pm=(82.66666667,165.3333333]}                   => {Cover_Type=Cover_Type7} 0.07863757  0.7010613 4.907429  1189
    ## [12] {Elevation=(3187,3850.986],                                                                                                 
    ##       Slope=(-0.052,17.33333333],                                                                                                
    ##       Hillshade_9am=(169.3333333,254.254],                                                                                       
    ##       Hillshade_3pm=(82.66666667,165.3333333]}                   => {Cover_Type=Cover_Type7} 0.07969577  0.7018055 4.912638  1205
    ## [13] {Elevation=(3187,3850.986],                                                                                                 
    ##       Hillshade_9am=(169.3333333,254.254],                                                                                       
    ##       Hillshade_Noon=(202.3333333,254.155],                                                                                      
    ##       Hillshade_3pm=(82.66666667,165.3333333]}                   => {Cover_Type=Cover_Type7} 0.08842593  0.7085321 4.959724  1337
    ## [14] {Elevation=(3187,3850.986],                                                                                                 
    ##       Slope=(-0.052,17.33333333],                                                                                                
    ##       Hillshade_9am=(169.3333333,254.254],                                                                                       
    ##       Hillshade_Noon=(202.3333333,254.155],                                                                                      
    ##       Hillshade_3pm=(82.66666667,165.3333333]}                   => {Cover_Type=Cover_Type7} 0.07863757  0.7010613 4.907429  1189
