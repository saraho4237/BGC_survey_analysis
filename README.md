# Boys and Girls Club of Rosebud Survey Analysis via Dimensionality Reduction

##### Table of Contents

1. [Introduction](#introduction)
2. [Project Goals](#project-goals)
3. [Data and EDA](#data-and-eda)
4. [Dimensionality Reduction](#dimensionality-reduction)
5. [Model Selection](#model-selection)
6. [Model Results](#model-results)
7. [Survey Recommendations](#survey-recommendations)
8. [Future Direction](#future-direction)

## Introduction

*"At the Boys and Girls Club of Rosebud, we believe our youth are sacred.  That is why, in everything we do, we seek to empower our youth to live out their dreams.  We do this through consistent mentoring relationships, and a focus on our three priority outcomes: **academic success, good character, and healthy lifestyles**."*
*-- Glen Marshall (Executive Director)*


![](images/club.png)

The Boys and Girls Club of Rosebud, South Dakota serves the youth of the Rosebud Sioux Tribe (Sicangu Oyate). Growing up on the reservation presents a variety of challenges. The Rosebud youth face some of the highest poverty rates in the nation. The economic and social issues reflect a great need for positive role models and high yield youth programming. The Boys and Girls Club of Rosebud is focused on providing programs that enable youth to succeed academically, develop strong character, and lead healthy lives.

![](images/badlands.png)

In summer 2018, the Boys and Girls Club delivered a survey (via in person interview) to club members from the 3 different club sites (Mission, Rosebud, and Parmalee). The survey was designed to measure students' perception of their experience at the club. The results of the survey could be used to predict whether or not a student planned to continue coming to the club.

![](images/bike.png)

*pictures and content from https://www.rosebudbgc.org/*

## Project Goals

1) Determine which features (survey questions) are most useful in predicting whether a student plans to continue membership at the Boys and Girls Club. Use this information to shorten the survey in the future.

2) Reduce the dimensionality of the data to get a model that accurately predicts whether or not a student plans to continue coming to the Boys and Girls Club.

## Data and EDA

Two separate surveys were administered. Student age 7 and younger were given a shorter survey version. Club members age 8+ received the following [Teen/Upper Elementary survey (30 items)](https://github.com/saraho4237/BGC_survey_analysis/blob/master/survey_questions_and_dist.md)

Survey responses were mapped to the following values:
* Questions 3 and 4:
All of the time = 4, Most times = 3, Some times = 2, Never = 1
* Question 16:
8th Grade = 1, Some high school = 2, High School Diploma = 3, College Degree = 4
* All other questions:
Strongly Agree = 5, Agree = 4, Neutral = 3, Disagree = 2, Strongly Disagree = 1.

The survey also collected information on each participant's gender identity, age, grade in Fall '18, and race/ethnicity.

### Participant Demographics

93 club members completed the Teen/Upper Elementary survey.

![](images/demo_bar.png)

Female and male classes are well balanced.

10-year-olds make up the largest age group.

Most club members attend the Mission club. Mission, SD has a relatively large population for a reservation community (pop. 1,240) and has the largest elementary and middle school on the reservation.

Most club members identify as American Indian.

### Missing Data

The following table shows the questions where one or more data points were missing as well as the number of missing data points:

| Question                                                                             | # NA |
|--------------------------------------------------------------------------------------|------|
| 2. I feel respected by fellow Club members when I am at the Club                     | 1    |
| 3. I feel safe when I am at the Club                                                 | 1    |
| 7. I feel comfortable talking to any staff member at the Boys and Girls Club         | 1    |
| 22. The Club helps me to reach my personal goals                                     | 1    |
| 23. I feel the Club celebrates who I am as a person                                  | 1    |
| 25. The Club helps me build positive feelings about my tribal and/or racial identity | 6    |
| 26. The Club helps me to learn about Lakota language and culture                     | 1    |

The missing data were not from the same observation. Also, 6 of the 7 columns with missing data only had 1 observation missing. For this reason, I decided to deal with missing data by imputing the median of the column.

The median was imputed because the data in the questions with na's were skewed (as seen in the distribution of answers to Question 7 "I feel comfortable talking to any staff member at the Boys and Girls Club").

![](images/q7.png)

### EDA Take-Aways
* The majority of survey questions are skewed left. All survey questions were worded positively ("strongly agree" is always strongly agreeing to a positive attribute). This indicates that the most common response to a question was often positive (agree or strongly agree). Yay!

* 63% of survey participants believe they will receive a college degree.

* A quick look at how the club is meeting priority outcomes:
  * Academic Success: 77% of survey respondents agree or strongly agree that "going to the Club helps me learn more and become smarter."
  * Good Character/ Citizenship: 81% of survey respondents agree or strongly agree that "going to the Club helps me develop my social skills with other students."
  * Healthy Lifestyles: 85% of survey respondents agree or strongly agree that "the Club helps me exercise more."

## Dimensionality Reduction

### Principal Components Analysis (PCA) via Singular Value Decomposition

![](images/sn1_f.png)

We will need to use ~15 principle components (orthogonal linear combinations of the data) to explain 90% of the variance in the data.

Principle component 1 explains ~30% of the variance in the data. However, the loadings on the questions are not helpful. They are all negative (what??) and also close together. There are not clear groupings of questions which explain this principle component.

Loadings: [-0.17,-0.17,-0.18, -0.18,-0.19,-0.19,-0.19,-0.19,-0.19,-0.19, -0.19,-0.19, -0.19,-0.19,-0.19,-0.19,-0.19,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.21,-0.21]

### Non_Negative Matrix Factorization

Topic 1 loads strongly on the following questions:

* 30. I have fun and enjoy my time at the Boys and Girls Club (3.22)
* 28. I’m glad I’m a Boys and Girls Club member (3.01)
* 5. At the Club, I have a good time (2.63)

Topic 1 may be labeled **"Fun."**

Topic 2 loads strongly on the following questions:

* 26. The Club helps me to learn about Lakota language and culture (3.02)
* 23. I feel the Club celebrates who I am as a person (2.91)
* 27. The Club helps me learn about myself, my family, and my tribe (2.56)
* 8. I believe all staff members care about me and my experience at the Club (2.20)

This latent topic may be labeled **"Identity Validation."**

Topic 3 loads strongly on the following questions:

* 2. I feel respected by fellow Club members when I am at the Club (2.34)
* 15. I feel like going to the Club helps me develop my social skills with other students (2.15)
* 24. The Club helps me to feel proud about who I am (1.36)
* 9. There are clear expectations for me during Club time (1.32)

This latent topic may be labeled **"Social Skills Development.""**

![](images/recon_error_f.png)

The loadings on the questions are much more interpretable in NMF. The positive loadings allow the questions to be grouped into latent topics. However, it is not clear how many latent topics should be used to predict planned retention. There is no clear drop in the Reconstruction Error elbow plot (above).

### Dimensionality Reduction via Random Forest Classifier Feature Importances

I fit a Random Forest Classifier on all 29 questions using balanced classes (planning to return vs. not planning to return). The feature importances are plotted below:

![](images/feature_import_f.png)

The most important questions for predicting planned retention are as follows (in order of feature importance):
* 17.I feel comfortable and confident in expressing myself at the Club
* **5.At the Club, I have a good time -- (Fun)**
* 11.I feel like going to the Club helps me learn more and become smarter
* 21.The Club helps me to set personal goals
* **27.The Club helps me learn about myself, my family, and my tribe -- (Identity Validation)**
* **30. I have fun and enjoy my time at the Boys and Girls Club -- (Fun)**
* 13.The Club helps me get better at reading
* 22.The Club helps me to reach my personal goals
* 10.Staff members recognize me when I do a task well or display good behavior
* **2.I feel respected by fellow Club members when I am at the Club -- (Social Skill Development)**

## Model Selection

I performed KFold cross validation to pick the set of features that would most accurately predict planned retention. I used random forest classification models with 100 trees and balanced classes.

| Random Forest Classifier Features               | KFold Cross Validation Score (Average Accuracy) |
|-------------------------------------------------|----------------------------|
| All Questions + Gender + Club + Age             | .783                       |
| Principle Components (15) + Gender + Club + Age | .739                       |
| Top 10 Questions + Gender + Club + Age          | .812                       |

The best performing model used the top 10 most important questions and demographic information to predict planned retention with 81.2% accuracy.

## Model Results
#### Performance

The 10 most important questions and demographics could predict planned retention with 79.2% accuracy on unseen test data.

![](images/roc_f.png)

#### Take-Aways

| Question 17            | Question 5            | Question 11            | Question 21            | Question 27            |
|------------------------|-----------------------|------------------------|------------------------|------------------------|
| ![](images/pdp_17.png) | ![](images/pdp_5.png) | ![](images/pdp_11.png) | ![](images/pdp_21.png) | ![](images/pdp_27.png) |

The partial dependency plots show that for the most important questions (I chose the top 5 to show, above), as responses become more positive, the probability of not planning to come back to the club (probability of attrition) goes down. That is what we would expect. Hurray!

| Gender (Female=1, Male=0)      | Club (1=Mission, 0=Rosebud or Parmalee) | Age (1 = 11+ yo, 0=8-10 yo) |
|--------------------------------|-----------------------------------------|-----------------------------|
| ![](images/pdp_gender_num.png) | ![](images/pdp_club_num.png)            | ![](images/pdp_age_bin.png) |

Female participants have a higher probability of not planning to come back to the club after the summer.

The probability of not planning to come back to the club after summer is roughly the same regardless of the club attended (Mission, Rosebud, or Parmalee). 

Survey participants in the older age group (11+) have a lower probability of not planning to come back to the club.  

## Survey Recommendations

The survey can be cut to only include the following 10 Likert Scale Items without losing predictive power:

1. I feel respected by fellow Club members when I am at the Club
2. At the Club, I have a good time
3. Staff members recognize me when I do a task well or display good behavior
4. I feel like going to the Club helps me learn more and become smarter
5. The Club helps me get better at reading
6. I feel comfortable and confident in expressing myself at the Club
7. The Club helps me to set personal goals
8. The Club helps me to reach my personal goals
9. The Club helps me learn about myself, my family, and my tribe
10. I have fun and enjoy my time at the Boys and Girls Club

Consider including a few open response questions (these responses can be analyzed via natural language processing!).

Interesting finding: a few groupings of questions emerged during topic modeling. They may be described as latent topics relating to **fun, identity validation,** and **social skill development.**

## Future Direction

In the future I would like to improve this model/expand upon this project by:
* Using grid searching to optimize random forest hyper-parameters for better model selection (vs. using the same hyper-parameters for all models).
* Trying different classifiers besides random forests (logistic regression, gradient boosting, etc.)
* Using Latent Dirichlet Allocation (LDA) to improve latent topics.
* Collecting up-to-date retention information to find out if the model is predictive of actual retention (not just planned retention).

## If you would like to contribute to the great programming at the Boys and Girls Club of Rosebud, donate [here](https://www.paypal.com/donate/?token=8QK1jdyb7m8yYDeDVMJfzwD6loKnVRq7aChJ9Skfk3U__1SYmPjAK2mgdDo6qgvNgLtqG0&country.x=US&locale.x=).
