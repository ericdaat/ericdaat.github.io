Title: Out of core text classification with Scikit Learn
Date: 2018-02-02 10:20
Modified: 2018-02-02 10:20
Category: Programming
Tags: scikit-learn, code, machine-learning, classification
Slug: out-of-core-text-classification-scikit-learn
Authors: Eric Daoud
Summary: In this article, we are going to demonstrate how to build a simple text classifier for larger than RAM datasets. This approach is called Out of Core Learning, and many python Machine Learning librairies make this very easy to implement. For this example I used reviews from the [Yelp Dataset Challenge](https://www.yelp.com/dataset/challenge) and Python [scikit-learn](http://scikit-learn.org/stable/) library.
status: published

In this article, we are going to demonstrate how to build a simple text classifier for larger than RAM datasets. This approach is called Out of Core Learning, and many python Machine Learning librairies make this very easy to implement. For this example I used reviews from the [Yelp Dataset Challenge](https://www.yelp.com/dataset/challenge) and Python [scikit-learn](http://scikit-learn.org/stable/) library.

## The Dataset

First, download the dataset from the [Yelp website](https://www.yelp.com/dataset/challenge). Once you're done, we are going to work with the the reviews file. It contains one Json per row, and I like to use the [Python Pandas](https://pandas.pydata.org/) library to read datasets.  
Pandas has a nice function called `read_json` that we are going to use for reading the dataset. However we have to be careful of two things:

 - The dataset is really large, so we don't want to fully load it in RAM
 - It's not really a Json file, it has one Json per line

Thankfully, Pandas is so awesome that it provides everything we need to address these two issues. We are going to use `chunksize` to tell pandas to load the file chunk by chunk, and `lines=True` to tell Pandas that the file is not one full json but multiple json rows.

The function will look like this:

``` python
dfs = pd.read_json('./yelp_academic_dataset_review.json',
                   lines=True,
                   chunksize=5000)
```

The `dfs` variable is a generator, on which we will iterate to get the Dataframe chunks.

We are mainly interested in two columns from this dataframe:

 - *text*: The text from the user review.
 - *stars*: How many stars did the user give.

We will simply do a binary classification, and predict whether the review was positive or negative. For this, we take the assumption that a positive review has a rating greater than 3. We can create a new column called *sentiment* with the following code:

``` python
df_['sentiment'] = df_['stars'].apply(lambda r: 1 if r > 3 else 0)
```

Our input data will be *text*, and the target *sentiment*.

## The Classifier Model

## Full Code

``` python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier


dfs = pd.read_json('./yelp_academic_dataset_review.json',
                   lines=True,
                   chunksize=5000)

v = HashingVectorizer()
clf = SGDClassifier()

for i, df_ in enumerate(dfs):
    df_['sentiment'] = df_['stars'].apply(lambda r: 1 if r > 3 else 0)

    text_train, text_val, target_train, target_val = \
        train_test_split(df_['text'], df_['sentiment'])

    clf.partial_fit(X=v.transform(text_train),
                    y=target_train,
                    classes=[0, 1])

    val_score = clf.score(v.transform(text_val), target_val)
    print 'Batch {0}, val score {1}'.format(i+1, val_score)
```

And our model learns pretty well !

``` text
Batch 1, val score 0.8376
Batch 2, val score 0.7568
Batch 3, val score 0.8472
Batch 4, val score 0.8504
Batch 5, val score 0.8272
Batch 6, val score 0.7992
Batch 7, val score 0.8096
Batch 8, val score 0.812
Batch 9, val score 0.8496
Batch 10, val score 0.8072
Batch 11, val score 0.8944
Batch 12, val score 0.8304
Batch 13, val score 0.8096
...
Batch 418, val score 0.9248
Batch 419, val score 0.92
Batch 420, val score 0.9136
Batch 421, val score 0.9216
Batch 422, val score 0.9088
Batch 423, val score 0.9136
Batch 424, val score 0.916
Batch 425, val score 0.9096
Batch 426, val score 0.9248
Batch 427, val score 0.9184
Batch 428, val score 0.916
Batch 429, val score 0.9072
```
