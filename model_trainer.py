import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# 📊 Veriyi yüklüyoruz
data = pd.read_csv("C:/Users/LENOVO/PycharmProjects/fastapi_dondurma_karı_tahmini/Ice Cream Sales - temperatures.csv")

# 📊 X ve y belirleme
X = data[["Temperature"]]
y = data[["Ice Cream Profits"]]

# 📊 Train-test ayırımı (buraya aslında gerek bile yok çünkü tek seferlik eğitim yapıyoruz)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 📊 Modelimizi eğitiyoruz
model = LinearRegression()
model.fit(X_train, y_train)

# 📦 Modeli pickle formatında kaydediyoruz
with open("linear_regression_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model başarıyla kaydedildi!")
