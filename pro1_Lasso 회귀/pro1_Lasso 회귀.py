import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

file_path = r'C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_1_Relevance-between-news-topics-and-trading-volume\pro1_Lasso 회귀\pro1_Lasso-회기분석_자료.csv'

data = pd.read_csv(file_path)

# 데이터 전처리
data['Stock_Volume'] = data['Stock_Volume'].str.replace(',', '').astype(int)
data['Date'] = pd.to_datetime(data['Date'])

# MinMaxScaler를 사용한 데이터 표준화
scaler = MinMaxScaler()
X = data.drop(['Date', 'Stock_Volume'], axis=1)
y = data['Stock_Volume']
X_scaled = scaler.fit_transform(X)
y_scaled = scaler.fit_transform(y.values.reshape(-1, 1))

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# 라쏘 회귀 모델 설정 및 훈련
cv = 100
lasso_cv = LassoCV(cv=cv, random_state=0)
lasso_cv.fit(X_train, y_train.ravel())
best_alpha = lasso_cv.alpha_

# 라쏘 모델로 예측
lasso_model = Lasso(alpha=best_alpha)
lasso_model.fit(X_train, y_train.ravel())
y_pred = lasso_model.predict(X_test)

# 모델 평가
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Best Alpha: {best_alpha}, MSE: {mse}, MAE: {mae}, R2: {r2}')

# 결과 시각화
plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], y_test, label='True Data', color='blue', alpha=0.5)
plt.scatter(X_test[:, 0], y_pred, label='Predicted Data', color='red', alpha=0.5)
plt.title('Lasso Regression: Predicted vs True Data')
plt.xlabel('Scaled First Keyword Frequency')
plt.ylabel('Scaled Stock Volume')
plt.legend()
plt.show()
