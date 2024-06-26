# Data Science and Machine Learning
## Final Report: Team Basel (Tim Bättig & Giammarco Bozzelli) - 7th in Kaggle competition
[GitHub Directory](https://github.com/Kurthhenry/DSML)

### Introduction
We were tasked with finding building a machine learning model that can predict the difficulty of French sentences. To achieve this, we tried a plethora of different models, the results of which are summarized in the table below. The highest accuracy was obtained by combining the three last models, i.e. DistilBert, CamemBert, and FlauBert. This yielded us the final and highest accuracy of 61,5% over unseen data. The report below will explain how we proceeded and which models we used. For each of the models, a brief summary and interpretation of the results will be provided. We will then introduce the webapp that we have developed to apply the classifier we achieved the highest accuracy with. 

On a general note, all the data and code necessary to implement the below presented findings are available in the App, Code, and DATA folders in this repository. 

#### Table 1: Results
|                   | Logistic Regression | KNN   | Decision Tree | Random Forest | SVM   | Neural Network | DistilBert | CamemBert | FlauBert |
|-------------------|---------------------|-------|---------------|---------------|-------|----------------|------------|-----------|----------|
| Precision         | 41.0%               | 38.0% | 31.0%         | 40.0%         | 44.0% | 45.0%          | 55.00%     | 55.00%    | 56.00%   |
| Recall            | 41.0%               | 38.0% | 31.0%         | 41.0%         | 44.0% | 45.0%          | 54.00%     | 54.00%    | 56.00%   |
| F1-Score          | 41.0%               | 36.0% | 30.0%         | 39.0%         | 44.0% | 45.0%          | 54.00%     | 54.00%    | 56.00%   |
| Training Accuracy | 41.5%               | 37.9% | 31.3%         | 40.9%         | 43.7% | 45.1%          | 54.00%     | 54.00%    | 56.00%   |


#### EDA
In the starting phase of our project, we conducted a quick Exploratory Data Analysis (EDA) to gain a first understanding of the given dataset. For this project, we examined various features of the sentences, including linguistic attributes such as word frequency, sentence length, syntactic complexity, and vocabulary diversity. Visualizing these features through histograms, scatter plots, and correlation matrices provided valuable insights into the relationships between different variables and the target difficulty levels. Additionally, we assessed the distribution of difficulty levels across the dataset to ensure a balanced representation, which is essential for building robust predictive models. The findings from the EDA guided our feature engineering and selection process, setting a solid foundation for the subsequent modelling phase.

![EDA](https://github.com/GiammarcoBozzelli/DSML/assets/22881324/69d5f596-f265-4729-9cb9-a8bc48a66f57)

Both sentence length and word count exhibit right-skewed distributions, indicating that most sentences are relatively short in terms of both character count and word count. The average word length in sentences tends to follow a normal distribution, with most words having around 5 characters on average. The majority of sentences are syntactically simple, with most containing only 1-2 clauses. There is a notable skew towards higher vocabulary diversity, with many sentences having a TTR close to 1. The dataset maintains a balanced distribution across different difficulty levels, ensuring that each category is well-represented for model training.

![Correlation matrix](https://github.com/GiammarcoBozzelli/DSML/assets/22881324/eb9aff88-f3e6-462e-8886-6e3390179088)

The correlation matrix reveals that sentence length, word count, and average word length have the strongest positive correlations with difficulty, indicating that longer and wordier sentences with longer words are generally more difficult. Syntactic complexity has a weaker positive correlation, suggesting a minor influence on difficulty. Conversely, vocabulary diversity has a negative correlation, suggesting that sentences with more unique words relative to the total number of words tend to be easier.

Now that we have a general understanding of the dataset we can start use standard models and see to what extent we are able to predict sentences' difficulty levels.

### Models & Results
For the models described below we did not remove stopwords. The topic was hotly discussed between us two as there are very compelling arguments for and against a removel of such. Accordingly, removing stopwords could reduce noise (focus on informative words) and dimensionality (more efficient training, less overfitting) of the data which can improve model performance. On the contrary, stopwords provide context and contain useful information. Since stopwords are the foundation of a language, they might have higher presence and meaning in easier sentences. Removing such words would make it more difficult for the model to separate easier from more difficult sentences, especially in a situation like ours where training data is sparse. We decided to not remove the stopwords in the applied models outlined below. Out of curiosity, we ran the models with and without removing stopwords. Interestingly, the accuracy of the model was higher for every application without stopword removal except for the SVM model. There, accuracy was about 1% higher if we exclude stopwords.

#### Logistic Regression
<img width="358" alt="image" src="https://github.com/GiammarcoBozzelli/DSML/assets/55870958/3ea4dd8b-0fa8-48ee-8f18-e76a94df712d">

We implemented the basic [logistic regression](https://raw.githubusercontent.com/GiammarcoBozzelli/DSML/main/Code/DSML_Assignment_LogReg.py) algorithm without any additional specifications and got an accuracy of almost 30%. We then used Bayesian optimisation for hyperparameter tuning which increased accuracy to 41,5%. This is the highest value we obtained with the standard logistic regression. As can be seen below, we specified possible parameters for the regularisation strength *C*, the regularisation type, i.e. *penalty*, and the *solver*. Since the *lbfgs* solver does not support lasso regression, we tried two different parameter sets. We once excluded *L1* and used both solvers, and we once excluded *lbfgs* and used both, ridge and lasso regression. The resulting accuracies were almost identical. Since the latter is higher, we reported the final value of **41,5%** accuracy of a logistic regression model using regularisation strength *C* of 0.441, *L2* regularisation (Ridge Regression), and *liblinear* solver. 
```
param_dist = {
    'C': (1e-6, 1e+6, 'log-uniform'),
    'penalty': ['l2', "l1"],           
    'solver': ["liblinear"],
}
```

#### k-Nearest Neighbours
<img width="362" alt="image" src="https://github.com/GiammarcoBozzelli/DSML/assets/55870958/1efca0ce-54bd-45d0-9c07-f12b1cf49ae0">


We implemented the basic [KNN model](https://raw.githubusercontent.com/GiammarcoBozzelli/DSML/main/Code/DSML_Assignment_KNN.py) and played around with the parameters to get a feeling of how they behave. Generally, more neighbours do not necessarily increase accuracy. It depends on the weighting and distance metric employed. In our case, using cosine similarity as distance metric gave the highest accuracy. Using Bayesian optimisation, we found that the KNN model with 21 neighbours, cosine similarity, and distance-dependent weights gave the highest accuracy of **37.9%**. The remaining common evaluation metrics are given in _Table 1_ above. The parameters for which we wanted to find optimal values are given in the code snippet below. It includes the amount of neighbours, whether we assign uniform weights or dependent on distance, and the three most common metrics for distance measuring. As was to be expected intuitively, the accuracy is higher if we assign weights according to the distance of each neighbour. Closer neighbours obtain higher weights than more remote observations.  
```
param_dist = {
    'n_neighbors': (1, 30),
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan', 'cosine']
}
```

#### Decision Tree
<img width="989" alt="image" src="https://github.com/GiammarcoBozzelli/DSML/assets/55870958/161fdc9d-dc28-49d6-bdd1-25e6d6864486">

As for the logistic regression and KNN approaches above, we used bayesian optimisation for hyperparameter tuning to find the most promising values for the parameters of a standard [decision tree model](https://raw.githubusercontent.com/GiammarcoBozzelli/DSML/main/Code/DSML_Assignment_DecisionTree.py). The specified optimisation is given below. 
```
param_dist = {
    'max_depth': Integer(1, 50),
    'min_samples_split': Integer(2, 20),
    'min_samples_leaf': Integer(1, 20),
    'criterion': Categorical(['gini', 'entropy']),
    'max_features': Categorical([None, 'sqrt', 'log2'])
}
```
*max_depth* is the maximum allowed depth of the tree. We specified it to be at 50 levels. While deeper trees can model more complex relationships in the data, they may also lead to overfitting if they are too deep relative to the complexity of the dataset. Since our dataset is not too complex, we did not allow for excessive tree depth. The same argumentation is valid for *min_samples_split* which indicates how many samples must accumulate at one node in order for it to split. Early splitting can namely lead to overfitted models. Similarly, *min_samples_leaf* specifies the least amount of samples a leaf must have. This ensures the model does not learn overly specific patterns at the loss of generalisation. The different measures of quality of a split are given in *criterion*, where Gini Impurity and Entropy are the most common. In our optimal decision tree model, we use Gini Impurity, a maximum depth of 50 levels, a minimum amount of samples per leaf of 15, and a minimum amount of samples for a split of 20. This leaves us with an accuracy of **31.3%**. The remaining key evaluation metrics are given in the Table 1 above. 

The decision tree model performs substantially worse than logistic regression and KNN. This can be due to several reasons. Most likely, it is because in text analysis we employ TF-IDF vectorizers. These transform the text into TF-IDF features that are high-dimensional and sparse. Decision trees may not handle this kind of data well, as they make splits based on individual features, and many features in our case may have zero values.

#### Random Forest
<img width="989" alt="image" src="https://github.com/GiammarcoBozzelli/DSML/assets/55870958/1e42321e-b5d0-47da-bb7e-e677e2e93ca9">

As for the decision tree implementation above, we use hyperparameter tuning to find the most promising values for a prediction using a [random forest classifier](https://raw.githubusercontent.com/GiammarcoBozzelli/DSML/main/Code/DSML_Assignment_RandomForest.py). 
```
param_dist = {
    'n_estimators': Integer(10, 200),
    'max_depth': Integer(1, 50),
    'min_samples_split': Integer(2, 20),
    'min_samples_leaf': Integer(1, 20),
    'max_features': Categorical([None, 'sqrt', 'log2']),
    'criterion': Categorical(['gini', 'entropy'])
}
```
The only parameter differing from the decision tree implementation is the *n_estimators*. Since we are building not a single but several trees in this approach, we need to specify how many we want to allow. Accordingly, *n_estimators* determines the number of individual decision trees that will be built and combined to form the random forest model. Allowing for several trees that then vote on an outcome seems to pay off. The accuracy of our optimised random forest classifier lies with **40.9%** substantially above the decision tree employed above. The optimal parameter values are Gini impurity for split quality, 200 estimators, a maximum depth of 50 levels, at least 1 sample per leaf, and at least 19 samples to allow a split.  

#### Support Vector Machine
<img width="733" alt="image" src="https://github.com/GiammarcoBozzelli/DSML/assets/55870958/9b62bfb5-f489-4d1d-a143-20eed3fb17f6">

Our first non-basic model is an [SVM model](https://raw.githubusercontent.com/GiammarcoBozzelli/DSML/main/Code/DSML_Assignment_SVM.py) which is often used for text classification. It is suitable because of its effectiveness in high-dimensional spaces, as is the case with TF-IDF features, and its ability to find a hyperplane that best separates different classes. It essentially takes a set of labeled training data and tries to find the optimal hyperplane that separates the classes with the maximum margin (distance between the hyperplane and the nearest support vector from either class). Support vectors are the data points that are closest to the hyperplane. The hyperplane is the decision boundary that separates different classes in the feature space.
```
param_dist = {
    'C': Real(1e-6, 1e+6, prior='log-uniform'),
    'kernel': Categorical(['linear', 'rbf', 'poly']),
    'degree': Integer(2, 5),   # Only relevant for 'poly' kernel
    'gamma': Categorical(['scale', 'auto'])  # Only relevant for 'rbf' and 'poly' kernels
}
```
As for the models above, we used Bayesian optimisation for hyperparameter tuning. The main parameters are the regularisation strength *C*, and the *kernel* type. *degree* and *gamma* are further specifications for the kernel function which we will not explore further. *C* controls the trade-off between maximizing the margin and minimizing the classification error. A smaller value allows for a larger margin at the cost of more classification errors, leading to a softer margin. A larger value aims to classify all training examples correctly but may result in a smaller margin, leading to a harder margin. The *kernel* parameter specifies which function to use. That is a linear, radial basis (Gaussian), or polynomial kernel function. In our optimised model specification, we use a C value of 928.74 and a Gaussian kernel. This yields us a final accuracy of **43.7%** which is, so far, the highest attained accuracy for our language difficulty predictor.

#### Neural Network
![image](https://github.com/GiammarcoBozzelli/DSML/assets/55870958/7f7b3ee3-0e24-4a7a-a327-cc70a6788a64)

We then tried a [neural network](https://raw.githubusercontent.com/GiammarcoBozzelli/DSML/main/Code/DSML_Assignment_NeuralNet.py) approach. It is built in four layers. The first is the embedding layer that converts the input sequences of word indices into vectors of fixed length. The second is the only hidden layer that processes the data and captures dependencies. The third layer is the dropout layer that prevents overfitting by randomly setting a fraction of input units to 0 (during training). The fourth is the output layer mapping the hidden layer's outputs to the available number of classes. We use Bayesian optimisation for hyperparameter tuning. The main goal is to define the dimension of the embedding (*embedding_dim*), the amount of neurons employed (*lstm_units*) in the hidden layer, and the dropout rate (*dropout_rate*). After implementing the tuner, we are left with an optimal model. It has an embedding dimension of 128, 64 neurons in the hidden layer, a dropout rate of 0.3, and a learning rate of 0.00092. Interestingly, the neural network approach only yields an accuracy of **45,1%**. This is only slightly better than the SVM approach above. 

Generally speaking, the standard models just described yield solid but unsatisfactory prediction results on unseen data. The models predict best the difficulties on the extremes, i.e. A1, and C2. The levels in between the two vary amongst the models but never yield the best precision or recall values. This finding makes sense intuitively, as it is easier to recognise extreme patterns. Accordingly, the difference between a C2 and C1 sentence, or A1 and A2 sentence, is expected to be higher than, for example, between a B2 and C1 sentence.

### Transformers
Due to the poor performance of the "standard" models outlined up until now, we started to look at transformers since they would give us the possibility to access models pre-trained on large datasets that will definetly perform better once finetuned to our training dataset. Leveraging pre-trained models allows us to benefit from extensive training on large datasets, enabling our model to generalize better and improve its performance on predicting sentence difficulty without requiring a massive amount of labeled data.

We first performed some feature engineering on the data. We calculated the length of each sentence, the number of words per sentence, the average word length for the sentence and counted the number of punctuation characters. The additional features were stacked on other parameters and passed to each of the following models for fine-tuning. 

#### DistilBert on training_data.csv
[BERT](https://arxiv.org/abs/1810.04805), which stands for Bidirectional Encoder Representations from Transformers, is a state-of-the-art language representation model developed by Google. Unlike traditional models that read text input sequentially (left-to-right or right-to-left), BERT processes text bidirectionally. This means it reads the entire sequence of words at once, allowing it to understand the context of a word based on all surrounding words in a sentence. This particularity makes it highly effective for various natural language processing (NLP), especially text classification as in our case.

While BERT is highly accurate, it is also computationally intensive, requiring substantial resources for both training and inference. To address this challenge, Hugging Face developed DistilBERT, a distilled version of BERT, way smaller but with almost the same capabilities. For this reason, we opted for DistilBER, which is perfect for us students, having limited resources. Additionally, DistilBERT supports multiple languages, including French, ensuring that the model effectively understands and processes French sentences.

To train our DistilBERT model, we configured several parameters using the `TrainingArguments` class from the Hugging Face Transformers library. These parameters were the ones who yielded the best results in the training process. Important to point out are the following parameters:

- *learning_rate*: A small learning rate of 0.00005 is chosen to ensure stable training.
- *weight_decay*: A small weight decay of 0.0015 is applied to prevent overfitting by penalizing large weights.
- *num_train_epochs*: The number of times the entire training dataset is passed through the model. We set this to 8 to ensure sufficient training.

```
 training_args = TrainingArguments(
        output_dir=f'./results_fold_{fold + 1}',
        num_train_epochs=8,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=1000,
        weight_decay=0.0015,
        logging_dir=f'./logs_fold_{fold + 1}',
        logging_steps=20,
        evaluation_strategy="epoch",
        learning_rate=0.00005,
        fp16=True
    )
```

|                | precision | recall | f1-score | support |
|----------------|-----------|--------|----------|---------|
| A1             | 0.66      | 0.66   | 0.66     | 205     |
| A2             | 0.50      | 0.49   | 0.50     | 214     |
| B1             | 0.45      | 0.49   | 0.47     | 216     |
| B2             | 0.53      | 0.51   | 0.52     | 221     |
| C1             | 0.49      | 0.53   | 0.51     | 208     |
| C2             | 0.66      | 0.58   | 0.62     | 216     |
| **accuracy**   |           |        | 0.54     | 1280    |
| **macro avg**  | 0.55      | 0.54   | 0.55     | 1280    |
| **weighted avg** | 0.55      | 0.54   | 0.54     | 1280    |

The evaluation metrics show that the model has varying performance across different difficulty levels. The precision, recall, and F1-scores range from moderate to good, with level A1 and C2 achieving the highest F1-scores. The overall accuracy of 54% indicates that there is room for improvement in the model. The macro and weighted averages suggest that the model performs fairly consistently across classes, although certain levels like B1 and A2 have lower scores, highlighting potential areas for model tuning and further improvement.

#### CamemBert on training_data.csv
Next, we tried using the [CamemBERT](https://arxiv.org/abs/1911.03894) model, another variant of the BERT model (Bidirectional Encoder Representations from Transformers) specifically pre-trained on French language data. This model was trained on a diverse and large French dataset, which helps it grasp the syntactic and semantic nuances of the French language more effectively than a general multilingual model like BERT.

```
    training_args = TrainingArguments(
        output_dir=f'./results_fold_{fold + 1}',
        num_train_epochs=8,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=1000,
        weight_decay=0.0015,
        logging_dir=f'./logs_fold_{fold + 1}',
        logging_steps=20,
        evaluation_strategy="epoch",
        learning_rate=0.00005,
        fp16=True
    )
```
|      | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
| A1   | 0.66      | 0.66   | 0.66     | 205     |
| A2   | 0.50      | 0.49   | 0.50     | 214     |
| B1   | 0.45      | 0.49   | 0.47     | 216     |
| B2   | 0.53      | 0.51   | 0.52     | 221     |
| C1   | 0.49      | 0.53   | 0.51     | 208     |
| C2   | 0.66      | 0.58   | 0.62     | 216     |
| **Accuracy** |         |        | **0.54**    | 1280    |
| **Macro Avg** | 0.55   | 0.54   | 0.55     | 1280    |
| **Weighted Avg** | 0.55 | 0.54  | 0.54     | 1280    |

CamemBERT exhibits an overall accuracy at 54%, with both macro and weighted average F1-scores hovering around 0.55. Class A1 demonstrates the best performance with balanced precision and recall, both at 0.66. In contrast, Class B1 underperforms with the lowest F1-score of 0.47 and precision at 0.45, indicating a significant area for improvement. The model shows a mixed balance between precision and recall across classes, with classes A1 and C2 performing the best.

#### FlauBert on training_data.csv
Finally, we tried with yet another French language adaptation of BERT, the [FlauBERT](https://arxiv.org/abs/1912.05372) model, designed to perform natural language processing tasks specifically for the French language. FlauBERT is built by the French National Institute for Research in Digital Science and Technology (INRIA) and the Sorbonne University, following the architecture and pre-training approach of the original BERT model created by Google. FlauBERT was exclusively trained on a large and diverse corpus of French text, encompassing a wide range of genres and sources, which makes it highly proficient in understanding and generating French language constructs.

```
training_args = TrainingArguments(
        output_dir=f'./results_fold_{fold + 1}',
        num_train_epochs=10,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=1000,
        weight_decay=0.0015,
        logging_dir=f'./logs_fold_{fold + 1}',
        logging_steps=20,
        evaluation_strategy="epoch",
        learning_rate=0.00001,
        fp16=True
    )
```
|      | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
| A1   | 0.72      | 0.69   | 0.71     | 122     |
| A2   | 0.54      | 0.60   | 0.57     | 131     |
| B1   | 0.48      | 0.58   | 0.53     | 118     |
| B2   | 0.57      | 0.53   | 0.55     | 145     |
| C1   | 0.43      | 0.36   | 0.39     | 121     |
| C2   | 0.62      | 0.62   | 0.62     | 131     |
| **Accuracy** |         |        | **0.56**    | 768    |
| **Macro Avg** | 0.56   | 0.56   | 0.56     | 768    |
| **Weighted Avg** | 0.56 | 0.56  | 0.56     | 768    |

FlauBERT exhibits a moderate overall performance with an accuracy of 56%, and uniform macro and weighted averages for precision, recall, and F1-score at 0.56. The model's best-performing class is A1 with the highest precision and F1-score at 0.72 and 0.71 respectively, while C1 is the weakest with significantly lower metrics, showing an F1-score of only 0.39. Classes A2 and B1 are characterized by higher recall than precision, indicating a tendency to over-predict, whereas C2 demonstrates a balanced performance with both precision and recall at 0.62. Improvements in precision for several classes and boosting recall for the weakest classes could enhance the model's overall efficacy

### Augmented DF over-representing classes A2, B1, B2 and C1
Analyzing the accuracy for each class we realized that every model was relatively able to correctly categorise classes A1 and C2 while strugling more with the classes in between the extremes. We tried to amplify the dataset by creating new entries for only the middle classes by using gpt-2 but the results didn't change, probably due to the low quality of the generated sentences.

The approach that surprisingly worked best was to straightforward copy all sentences from those classes and concatenate them to the dataset. Using this approach performances increased, as expected, dramatically for the training data but also increased the ability of models to generalize to unseen data. We believe that having the central classes overrepresented enabled the model to adapt the weight assigned to each class in a more balanced manner, permitting the model to better generalize. 

Following is a list of all the models with relative performance on the augmented dataset.


#### DistilBert on augmented data

```
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=10,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=1000,
    weight_decay=0.0005,
    logging_dir='./logs',
    logging_steps=20,
    evaluation_strategy="epoch",
    learning_rate=0.000005,
    fp16=True
)
```
|      | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
| A1   | 0.71      | 0.57   | 0.63     | 169     |
| A2   | 0.70      | 0.77   | 0.74     | 318     |
| B1   | 0.74      | 0.78   | 0.76     | 329     |
| B2   | 0.73      | 0.80   | 0.76     | 310     |
| C1   | 0.75      | 0.76   | 0.76     | 312     |
| C2   | 0.65      | 0.45   | 0.53     | 158     |
| **Accuracy** |         |        | **0.72**    | 1596    |
| **Macro Avg** | 0.71   | 0.69   | 0.70     | 1596    |
| **Weighted Avg** | 0.72 | 0.72  | 0.72     | 1596    |

The classification model demonstrates good overall performance with an accuracy of 72% and consistent weighted average scores for precision, recall, and F1-Score all at 0.72. Notably, classes B1, B2, and C1 exhibit strong results, as expected the model learned better those classes due to over-representaion in the dataset. Class A2 also performs well with a F1-score of 0.74. In contrast, Class C2 shows lower efficiency, indicated by its F1-score of 0.53, due to its lower recall of 0.45 despite reasonable precision.

#### CamemBert on augmented_df 

```
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=10,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=1000,
    weight_decay=0.0005,
    logging_dir='./logs',
    logging_steps=20,
    evaluation_strategy="epoch",
    learning_rate=0.000005,
    fp16=True
)
```
|         | Precision | Recall | F1-Score | Support |
|---------|-----------|--------|----------|---------|
| A1      | 0.73      | 0.64   | 0.68     | 169     |
| A2      | 0.65      | 0.80   | 0.71     | 318     |
| B1      | 0.67      | 0.69   | 0.68     | 329     |
| B2      | 0.54      | 0.73   | 0.62     | 310     |
| C1      | 0.61      | 0.50   | 0.55     | 312     |
| C2      | 0.75      | 0.19   | 0.30     | 158     |
| **Accuracy** |         |        | **0.63**    | 1596    |
| **Macro Avg** | 0.66   | 0.59   | 0.59     | 1596    |
| **Weighted Avg** | 0.64 | 0.63  | 0.61     | 1596    |

Camembert shows an overall accuracy of 63%, with macro and weighted averages for F1-score at 0.59 and 0.61, respectively. The performance across different classes is mixed, with Class A2 showing relatively high recall (0.80) and a decent F1-score (0.71), suggesting it effectively identifies true positive. Conversely, Class C2 exhibits high precision (0.75) but significantly low recall (0.19), leading to a poor F1-score (0.30), indicating it misses many true positive cases. The overrepresented classes in the dataframe show improved metric throughout as expected.

#### FlauBert on augmented_df with A2-C1 copied

```
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=16,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=1000,
    weight_decay=0.0005,
    logging_dir='./logs',
    logging_steps=20,
    evaluation_strategy="epoch",
    learning_rate=0.000005,
    fp16=True
)
```

|      | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
| A1   | 0.75      | 0.67   | 0.71     | 169     |
| A2   | 0.75      | 0.89   | 0.81     | 318     |
| B1   | 0.86      | 0.83   | 0.85     | 329     |
| B2   | 0.86      | 0.86   | 0.86     | 310     |
| C1   | 0.87      | 0.89   | 0.88     | 312     |
| C2   | 0.85      | 0.62   | 0.72     | 158     |
| **Accuracy** |         |        | **0.82**    | 1596    |
| **Macro Avg** | 0.82   | 0.79   | 0.80     | 1596    |
| **Weighted Avg** | 0.83 | 0.82  | 0.82     | 1596    |

Flaubert displays an overall accuracy of 82%. The macro and weighted average scores for precision, recall, and F1-score are closely aligned, showcasing strong consistency across different classes. Classes B1, B2, and C1 exhibit particularly high scores in all metrics as expected due to their over representation in the new dataset.

#### Final Pipeline for prediction
We finally developed a pipeline combining the three models to generate predictions for each sentence. Each model independently predicts the classification, resulting in three sets of probability scores per sentence. We then average these probability scores across the three models for each class. The final prediction for each sentence is determined by selecting the class with the highest average probability. By experimenting with various configurations of the model's parameters, we achieved a maximum accuracy of **61.5%** on unseen data. This result, representing the best performance, is documented in the file [best_sub.csv](https://github.com/Kurthhenry/DSML/blob/main/DATA/best_sub.csv). Integrating multiple models and averaging their outputs enhances the robustness and accuracy of the predictions, leading to our highest observed accuracy on new data.

### Application 
We then thought of ways to implement the just developed model. We first considered providing an application that can predict the difficulty of Podcasts in French. We had to discard the idea because we could not find an appropriate API to scrape the transcripts of those Podcasts. The closest next best solution were videos. We knew that YouTube has autogeneration of transcripts and provides them through APIs. The idea was to create an app that can read the transcript of a YouTube video, classify its overall difficulty, but also the difficulty of each single sentence in the video. And that is what we did [here](https://raw.githubusercontent.com/Kurthhenry/DSML/main/App/webapp_final.py).

So the application basically takes the video url, scrapes the transcript, analyses the transcript and predicts its difficulty. It provides difficulty levels for the overall transcript and for each sentence. The user can browse through the sentences depending on the difficulty level he selects from a drop-down menu. If the video does not have a transcript or if the transcript does not have punctuation, the program will ask the user to upload a different url to another video. The program continues with a recommender system. From another drop-down menu, the user can select a difficulty level. The recommender will then propose two YouTube videos of that difficulty from the French YouTube's Trending page. The selection is random and renews every time the user selects a difficulty level. Here we included a warning for the A1 level that there are no Trending videos with an average difficulty of A1. That is, because YouTube is an entertainment and not an education platform. Accordingly, we expect the creators of the videos to speak naturally, which directly translates in more advanced levels of French. The recommender system is based on web-scraping through the YouTube API. We analysed the title and description of the videos with our model and predicted the difficulty depending on these text samples. The [code](https://raw.githubusercontent.com/Kurthhenry/DSML/main/App/scraper.py) for this scraping was developed by us but inspired by [Mitchell Jolly](https://github.com/mitchelljy/Trending-YouTube-Scraper/blob/master/README.md). 

The use cases for such an application are manifold. Neither Giammarco nor Tim have French as their mother tongue. We however both study in the Swiss-French part of Switzerland, where French is a huge plus. People like us could use the application to find French videos appropriate to their level to improve or strengthen their French. Learning is ensured by the fact that the user can read through every sentence of the video transcript, sorted by difficulty. The recommender function ensures that, once the accurate difficulty is found, the user is provided with other relevant videos with the selected average difficulty level.

The webapp comes with several limitations that we do not want to hide. Firstly, the app does not actively scrape the YouTube trending list. The scraping was done manually in the local IDE on the 20th of May 2024. In a real-world application, the scraping would have to be automated to keep providing the most relevant videos. Secondly, the webapp only runs locally through the terminal. In several instances we tried to deploy it online as a streamlit app, we however always received the error shown below. Apparently, streamlit has difficulties to load the transformers package that is substantial for our machine learning application. This issue would surely have to be investigated further and solved accordingly. 

![image](https://github.com/Kurthhenry/DSML/assets/55870958/dfa009c6-e164-4b8a-88a7-1def91705644)

Thirdly, the loading time when using the app for the first time is quite lengthy. That is, because we load the CamemBert and Flaubert models from [Hugging Face](https://huggingface.co/kurthhenry) Hub into the local IDE. This takes time because it requires substantial WIFI bandwith and computing power. In a situation of actual app deployment, this issue would have to be fixed to provide a satisfactory user experience. 

### Video
[Link](https://youtu.be/53AOo4s1gao) to our YouTube Video Submission.

### Work Partition 
In our collaborative project, the division of labor was planned to ensure an equitable distribution of responsibilities. We equally shared the workload, with each of us contributing 50% to all facets of the project. This balanced approach enabled us to leverage our individual strengths effectively while ensuring that both perspectives were equally represented in every phase of the project.

### Disclaimer on GPT
This report and the associated coding were developed with the assistance of ChatGPT.
