# -*- coding: utf-8 -*-
"""Proje.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ur9s-9PBiiWfD_y0-Pz0jaS1uBmd8DH1
"""
import streamlit as st 
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import joblib

# Streamlit başlığı ve açıklamaları
st.write("""
    <div style="text-align: center;">
        Filtre Yöntemi ile Özellik İndirgenen Veri Setine PCA Modelleme
    </div>
""", unsafe_allow_html=True)
st.write("""
    <div style="text-align: center;">
        030122073 - Ümit Başak
    </div>
""", unsafe_allow_html=True)

# Veri yükleme ve ön işleme
st.write("Veri")
try:
    df = pd.read_excel("glassLearning.xlsx")  # Veri Seti Okunur
except Exception as e:
    st.error("Veri seti yüklenemedi. Lütfen dosya yolunu kontrol edin.")
    st.stop()

df.drop('ID', axis=1, inplace=True)  # ID tablodan silinir

# Her Özellik için normalizasyon yapılır
features = ['RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe']
for feature in features:
    df[feature] = df[feature].apply(lambda v: (v - df[feature].min()) / (df[feature].max() - df[feature].min()))

# Filtre Yöntemi ile Özellik eleme Korelasyonu 0.3 üstü özellikler tutulur.
target = 'Type'
korelasyon = df.corr()
korelasyon_hdf = abs(korelasyon[target])
secilen_ozellik = korelasyon_hdf[korelasyon_hdf > 0.3].index.tolist()
FList = df[secilen_ozellik]
secilen_ozellik.remove('Type')
FListNoClass = df[secilen_ozellik]

# Kullanıcıdan giriş verilerini alın
st.write("""
    <div style="text-align: center;text-color:#ff0000;">
        Input Data
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
Ri_value = col1.number_input("RI", min_value=-20.0, max_value=50.0, value=0.0)
Na_value = col1.number_input("Na", min_value=-20.0, max_value=50.0, value=0.0)
Mg_value = col1.number_input("Mg", min_value=-20.0, max_value=50.0, value=0.0)

Al_value = col2.number_input("Al", min_value=-20.0, max_value=50.0, value=0.0)
Si_value = col2.number_input("Si", min_value=-20.0, max_value=100.0, value=0.0)
K_value = col2.number_input("K", min_value=-20.0, max_value=50.0, value=0.0)

Ca_value = col3.number_input("Ca", min_value=-20.0, max_value=50.0, value=0.0)
Ba_value = col3.number_input("Ba", min_value=-20.0, max_value=50.0, value=0.0)
Fe_value = col3.number_input("Fe", min_value=-20.0, max_value=50.0, value=0.0)

st.write("Girilen Data")
datas = ["RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe"]
values = [Ri_value, Na_value, Mg_value, Al_value, Si_value, K_value, Ca_value, Ba_value, Fe_value]
user_input = pd.DataFrame([values], columns=datas)
st.table(user_input.style.set_table_attributes('style="font-size: 20px; width: 100%; text-align: center;"'))

# Modelleme ve değerlendirme
X = FList.iloc[:, :-1]
y = FList.iloc[:, -1]

testSize = 0.2
xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=testSize, random_state=42)

skaler = StandardScaler()
Xtrain_scaled = skaler.fit_transform(xTrain)
Xtest_scaled = skaler.transform(xTest)

# KNN Modeli Eğitimi ve Değerlendirme
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(Xtrain_scaled, yTrain)
knn_yPred = knn_model.predict(Xtest_scaled)

knn_cmatrix = confusion_matrix(yTest, knn_yPred)
accuracyknn = accuracy_score(yTest, knn_yPred)
precisionknn = precision_score(yTest, knn_yPred, average='macro', zero_division=1)
recallknn = recall_score(yTest, knn_yPred, average='macro', zero_division=1)
f1knn = f1_score(yTest, knn_yPred, average='macro', zero_division=1)

# Sonuçları Görselleştirme
st.write("""
    <div style="text-align: center;">
        PCA Uygulandıktan Sonra
    </div>
""", unsafe_allow_html=True)
st.write("Karışıklık Matrisi:")

class_names = y.unique()
class_namesEq = ["F.İ Görmüş Bina Penceresi", "F.İ Görmemiş Bina Penceresi", "F.İ Görmüş Araç Camı", "Konteyner Camı", "Yemek Takımları", "Far Camı"]
tableMatris = pd.DataFrame(knn_cmatrix, index=class_namesEq, columns=class_namesEq)
st.table(tableMatris.style.set_table_attributes('style="font-size: 20px; width: 100%; text-align: center;"'))

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(knn_cmatrix, annot=True, cmap='Blues', fmt='g', xticklabels=class_namesEq, yticklabels=class_namesEq, ax=ax)
plt.title('k-NN Karışıklık Matrisi')
st.pyplot(fig)

st.write(f"k-nn Doğruluk: {accuracyknn:.2f}")
st.write(f"k-nn Hassasiyet: {precisionknn:.2f}")
st.write(f"k-nn Duyarlılık: {recallknn:.2f}")
st.write(f"k-nn F1 Skoru: {f1knn:.2f}")

st.write("""
    <div style="text-align: center;">
        86.3% doğruluk ile en başarılı modelim olmuştur.
    </div>
""", unsafe_allow_html=True)

# Kullanıcıdan alınan verileri ölçeklendirin ve tahmin yapın
if not user_input.isnull().values.any():  # Check if there are no null values
    # secilen_ozellik listesi kullanılarak user_input DataFrame oluşturuluyor
    user_input_scaled = skaler.transform(user_input[secilen_ozellik])
    
    # Tahmin yapın
    knn_user_prediction = knn_model.predict(user_input_scaled)
    
    st.write("""
        <div style="text-align: center;">
            Kullanıcı Girişi ile Tahmin
        </div>
    """, unsafe_allow_html=True)
    
    # Tahmin sonucunu sınıf adıyla birlikte gösterin
    st.write(f"Tahmin: {class_namesEq[knn_user_prediction[0]]}")
else:
    st.error("Kullanıcı girişi eksik veya hatalı. Lütfen tüm verileri doldurun.")
