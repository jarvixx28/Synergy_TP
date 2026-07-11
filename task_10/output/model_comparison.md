# Model Comparison

## 1. Regression Target

The regression task predicts the **CO(GT)** concentration, which is a continuous numerical variable representing carbon monoxide levels in the atmosphere. Since the target can take any real-valued measurement within a range, it is an appropriate problem for linear regression.

---

## 2. Regression Model vs Baseline

The regression baseline predicts the mean value of the training target for every test sample. This provides a simple reference for comparison.

The Linear Regression model learns the relationship between the selected sensor readings and the CO(GT) concentration using Gradient Descent. Since it utilizes information from multiple features, it is expected to produce significantly lower MAE, MSE, and RMSE values while achieving a higher R² score than the baseline.

This demonstrates that the model successfully captures meaningful relationships within the dataset rather than predicting a constant value.

---

## 3. Classification Target

The classification task predicts whether the carbon monoxide concentration is considered **high pollution**.

A binary target named **high_pollution** is created using the condition:

- CO(GT) > 2.0 → Class 1
- CO(GT) ≤ 2.0 → Class 0

This converts the regression target into a binary classification problem suitable for Logistic Regression.

---

## 4. Classification Model vs Baseline

The classification baseline always predicts the majority class observed in the training data.

Logistic Regression learns a decision boundary using the selected environmental sensor features. Unlike the baseline, it adapts its predictions based on the input data, resulting in improved Accuracy, Precision, Recall, and F1 Score.

The confusion matrix further illustrates that the trained model identifies positive and negative classes more effectively than the baseline classifier.

---

## 5. Most Serious Classification Errors

False negatives are generally more serious in this application because they classify high pollution levels as safe. This may prevent timely action or warnings when air quality is actually poor.

False positives may cause unnecessary alerts but are usually less harmful than failing to detect hazardous pollution levels.

---

## 6. Clustering Features

The clustering task uses the following sensor measurements:

- PT08.S1(CO)
- PT08.S2(NMHC)
- PT08.S3(NOx)
- PT08.S4(NO2)
- PT08.S5(O3)

No target labels are used during clustering because K-Means is an unsupervised learning algorithm. It groups samples solely based on feature similarity.

---

## 7. Interpretation of Clusters

The generated clusters represent groups of observations with similar air quality sensor measurements.

Although the clusters are not guaranteed to correspond to predefined pollution categories, they reveal underlying patterns within the dataset and may indicate different environmental conditions or pollution levels.

---

## 8. Possible Data Leakage Risks

Several precautions were taken to prevent data leakage:

- The dataset was divided into training, validation, and test sets before model evaluation.
- Standardization parameters were computed only from the training data and then applied to the validation and test sets.
- Target variables were never used as input features.
- Clustering was performed without using any target labels.

These steps help ensure fair and unbiased evaluation.

---

## 9. Readiness for More Advanced Machine Learning Models

The dataset is suitable for more advanced machine learning algorithms after preprocessing.

The selected features contain meaningful information related to air quality, and missing values have been handled appropriately. More sophisticated models such as Decision Trees, Random Forests, Gradient Boosting, or Neural Networks could potentially achieve higher predictive performance.

However, the current implementation focuses on fundamental machine learning algorithms implemented entirely from scratch, providing a strong foundation for understanding supervised and unsupervised learning techniques.
