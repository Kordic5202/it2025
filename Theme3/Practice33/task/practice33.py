import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Генерація штучного набору даних
np.random.seed(42)
num_samples = 500

num_features = pd.DataFrame({
    'feature1': np.random.uniform(10, 100, num_samples),
    'feature2': np.random.uniform(1, 50, num_samples),
    'feature3': np.random.uniform(5, 75, num_samples)
})

cat_features = pd.DataFrame({
    'category1': np.random.choice(['A', 'B', 'C'], num_samples),
    'category2': np.random.choice(['X', 'Y'], num_samples)
})

target = num_features['feature1'] * 0.5 + num_features['feature2'] * 2 + np.random.normal(0, 10, num_samples)

df = pd.concat([num_features, cat_features], axis=1)
df['target'] = target

# 2. Розділення на ознаки та цільову змінну
X = df.drop(columns=['target'])
y = df['target']

# 3. Розбивка на навчальний і тестовий набір
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Визначення числових та категоріальних колонок
num_cols = ['feature1', 'feature2', 'feature3']
cat_cols = ['category1', 'category2']

# 5. Побудова пайплайну для передобробки
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(drop='first'), cat_cols)
])

# 6. Лінійна регресія
lin_reg_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

lin_reg_pipeline.fit(X_train, y_train)
y_pred_lin = lin_reg_pipeline.predict(X_test)

# Оцінка лінійної регресії
mae_lin = mean_absolute_error(y_test, y_pred_lin)
mse_lin = mean_squared_error(y_test, y_pred_lin)
r2_lin = r2_score(y_test, y_pred_lin)

# 7. Random Forest Regressor (завершений код)
rf_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

rf_pipeline.fit(X_train, y_train)
y_pred_rf = rf_pipeline.predict(X_test)

# Оцінка Random Forest
mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# 8. Виведення результатів
results_df = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest Regressor'],
    'MAE': [mae_lin, mae_rf],
    'MSE': [mse_lin, mse_rf],
    'R² Score': [r2_lin, r2_rf]
})

print(results_df)

# 9. Побудова графіків
plt.figure(figsize=(10,5))
plt.bar(results_df['Model'], results_df['MAE'], color=['blue', 'green'])
plt.xlabel("Модель")
plt.ylabel("MAE")
plt.title("Порівняння MAE для моделей")
plt.show()

plt.figure(figsize=(10,5))
plt.bar(results_df['Model'], results_df['MSE'], color=['blue', 'green'])
plt.xlabel("Модель")
plt.ylabel("MSE")
plt.title("Порівняння MSE для моделей")
plt.show()

plt.figure(figsize=(10,5))
plt.bar(results_df['Model'], results_df['R² Score'], color=['blue', 'green'])
plt.xlabel("Модель")
plt.ylabel("R² Score")
plt.title("Порівняння R² Score для моделей")
plt.show()
