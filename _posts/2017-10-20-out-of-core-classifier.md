---
layout: post
title: Out of core text classification with Scikit Learn
date: 2018-02-02
excerpt:
    In this article, we are going to demonstrate how to build a simple text classifier for larger than RAM datasets. This approach is called Out of Core Learning, and many python Machine Learning librairies make this very easy to implement. For this example I used reviews from the Yelp Dataset Challenge and Python scikit-learn.
cover: books.jpg
---

## The Dataset

First, download the dataset from the [Yelp website](https://www.yelp.com/dataset/challenge). Once you're done, we are going to work with the the reviews file. It contains one Json per row, and I like to use the [Python Pandas](https://pandas.pydata.org/) library to read datasets.
Pandas has a nice function called `read_json` that we are going to use for reading the dataset. However we have to be careful of two things:

* The dataset is really large, so we don't want to fully load it in RAM
* It's not really a Json file, it has one Json per line

Thankfully, Pandas is so awesome that it provides everything we need to address these two issues. We are going to use `chunksize` to tell pandas to load the file chunk by chunk, and `lines=True` to tell Pandas that the file is not one full json but multiple json rows.

The function will look like this:

``` python
dfs = pd.read_json('./yelp_academic_dataset_review.json',
                   lines=True,
                   chunksize=5000)
```

The `dfs` variable is a generator, on which we will iterate to get the Dataframe chunks.

We are mainly interested in two columns from this dataframe:

* *text*: The text from the user review.
* *stars*: How many stars did the user give.

We will simply do a binary classification, and predict whether the review was positive or negative. For this, we take the assumption that a positive review has a rating greater than 3. We can create a new column called *sentiment* with the following code:

``` python
df_['sentiment'] = df_['stars'].apply(lambda r: 1 if r > 3 else 0)
```

Our input data will be *text*, and the target *sentiment*.

## The Classifier Model

Now that the dataset is ready, we shall turn our input text data into something that a computer might understand. We want to map the reviews as vectors in a fixed size space: the vocabulary. Scikit-learn offers tons of ways of doing it, like [CountVectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer) or [TfidfVectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), etc ...

These are great, but they won't work for a larger than RAM dataset, specifically because we can't load the full corpus in RAM, hence we can't learn the full vocabulary base. Instead, we are going to use the [HashingVectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html#sklearn.feature_extraction.text.HashingVectorizer) which uses the hashing trick: every word gets hashed into an integer index that we then use to compute the term-document matrix. Hence, not much has to fit in memory and this approach can scale to very large datasets.

``` python
v = HashingVectorizer()
v.transform(['some text']) # a 1*N matrix where every
                           # number is 0 except for two
```

Now, we can train a classifier on top of this incoming data. Although, the classifier has to support the `partial_fit` method, otherwise the model will be overridden at each epoch. [SGDClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) is among the classifiers that supports that, and it works pretty well so we will use this one.
From there it is very similar to other classifiers, except we use `partial_fit` instead of `fit`. We will simply loop over the incoming data chunks, transform the raw text into a term-document matrix thanks to the vectorizer, and then train the model, effectively keeping the previously learned weights.

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

And here is the output of our program: our model learns pretty well ! Note that I haven't done any preprocessing or fine tuning other than what's set by default.

``` bash
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

I hope this post was useful. Don't hesitate to have a look at scikit-learn documentation on this topic: [Strategies to scale computationally: bigger data](http://scikit-learn.org/stable/modules/scaling_strategies.html).
