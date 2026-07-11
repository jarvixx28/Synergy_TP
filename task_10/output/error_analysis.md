# Error Analysis

## 1. Regression Errors

The regression model performs well for most samples but produces larger errors for observations with unusually high or low CO(GT) concentrations. These extreme values are more difficult to predict because Linear Regression assumes a linear relationship between the selected sensor measurements and the target variable.

Some prediction errors may also arise due to measurement noise, missing values in the original dataset, and environmental factors that are not represented by the selected input features.

---

## 2. Classification Errors

The Logistic Regression classifier occasionally makes incorrect predictions when the feature values lie close to the decision boundary. Samples with sensor readings that are similar for both pollution classes are more likely to be misclassified.

False positives occur when normal pollution levels are classified as high pollution, while false negatives occur when actual high pollution levels are predicted as normal. False negatives are generally more critical because they may fail to identify potentially hazardous air quality conditions.

---

## 3. Class Distribution

The binary classification dataset is not perfectly balanced after converting the continuous CO(GT) values into two classes using the selected threshold.

If one class contains substantially more samples than the other, the majority-class baseline may achieve reasonable accuracy despite having poor predictive capability. Therefore, evaluation metrics such as Precision, Recall, and F1 Score provide a more meaningful assessment than accuracy alone.

---

## 4. Clustering Analysis

The K-Means algorithm groups observations according to similarities in the selected air quality sensor measurements.

The resulting clusters indicate that the dataset contains natural groupings based on sensor behaviour. However, because clustering is an unsupervised learning task, these groups do not necessarily correspond to predefined pollution categories.

The quality of clustering depends on the selected features, the chosen number of clusters, and the assumption that clusters are approximately spherical.

---

## 5. Limitations of the Current Models

The implemented models have several limitations:

- Linear Regression assumes a linear relationship between the input features and the target variable, which may not fully represent complex environmental interactions.

- Logistic Regression can only learn a linear decision boundary and may struggle when the classes are not linearly separable.

- K-Means assumes that clusters are spherical and of similar size, making it sensitive to the initial centroid selection and the chosen value of K.

- The baseline models are intentionally simple and serve only as reference points for comparison.

- The models rely on a limited subset of available features and do not capture temporal relationships or other complex dependencies present in air quality measurements.

---

## Conclusion

Despite these limitations, the implemented models demonstrate the complete machine learning workflow, including preprocessing, training, evaluation, visualization, and comparison. The results show clear improvements over the baseline models while providing a strong foundation for understanding machine learning algorithms implemented entirely from scratch.