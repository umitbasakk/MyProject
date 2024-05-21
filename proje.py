# -*- coding: utf-8 -*-
"""Proje.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ur9s-9PBiiWfD_y0-Pz0jaS1uBmd8DH1
"""

import streamlit as st 
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import pandas

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

st.write("Veri")
df= pandas.read_excel("glassLearning.xlsx") # Veri Seti Okunur
st.write(df)
df.drop('ID',axis=1, inplace=True) #ID tablodan silinir
#Her Özellik için normalizasyon yapılır
df['RI'] = df['RI'].apply(lambda v: (v - df['RI'].min()) / (df['RI'].max() - df['RI'].min()))
df['Na'] = df['Na'].apply(lambda v: (v - df['Na'].min()) / (df['Na'].max() - df['Na'].min()))
df['Mg'] = df['Mg'].apply(lambda v: (v - df['Mg'].min()) / (df['Mg'].max() - df['Mg'].min()))
df['Al'] = df['Al'].apply(lambda v: (v - df['Al'].min()) / (df['Al'].max() - df['Al'].min()))
df['Si'] = df['Si'].apply(lambda v: (v - df['Si'].min()) / (df['Si'].max() - df['Si'].min()))
df['K'] = df['K'].apply(lambda v: (v - df['K'].min()) / (df['K'].max() - df['K'].min()))
df['Ca'] = df['Ca'].apply(lambda v: (v - df['Ca'].min()) / (df['Ca'].max() - df['Ca'].min()))
df['Ba'] = df['Ba'].apply(lambda v: (v - df['Ba'].min()) / (df['Ba'].max() - df['Ba'].min()))
df['Fe'] = df['Fe'].apply(lambda v: (v - df['Fe'].min()) / (df['Fe'].max() - df['Fe'].min()))
st.write("Normalizasyon Sonrası:")
st.write(df)
testSize=0.1
###Filtre Yöntemi ile Özellik eleme Korelasyonu 0.55 üstü özellikler tutulur.
target = 'Type'
korelasyon = df.corr()
korelasyon_hdf = abs(korelasyon[target])
secilen_ozellik = korelasyon_hdf[korelasyon_hdf > 0.55].index.tolist()
FList = df[secilen_ozellik]
secilen_ozellik.remove('Type')
FListNoClass = df[secilen_ozellik]


col1, col2, col3 =st.columns(3)

Ri_value = col1.number_input("RI",min_value=-2.0,max_value=5.0,value=0.0)
Na_value = col1.number_input("Na",min_value=-2.0,max_value=5.0,value=0.0)
Mg_value = col1.number_input("Mg",min_value=-2.0,max_value=5.0,value=0.0)

Al_value = col2.number_input("Al",min_value=-2.0,value=2.0)
Si_value = col2.number_input("Si",min_value=-2.0,value=2.0)
K_value = col2.number_input("K",min_value=-2.0,value=2.0)

Ca_value = col3.number_input("Ca",min_value=-2.0,value=2.0)
Ba_value = col3.number_input("Ba",min_value=-2.0,value=2.0)
Fe_value = col3.number_input("Fe",min_value=-2.0,value=2.0)

######################################################################## PCA ########################################################################

# Özellikler (bağımsız değişkenler) ve hedef değişken (bağımlı değişken) olarak ayırma
X = FList.drop(columns=[target])
y = FList[target]

skaler = StandardScaler()
X_scaled = skaler.fit_transform(X)

pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)

xTrain, xTest, yTrain, yTest = train_test_split(X_pca, y, test_size=testSize, random_state=42)

rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(xTrain, yTrain)

yPred = rf_model.predict(xTest)

yt = pd.DataFrame(yTest)
class_names = yt['Type'].unique()
cmatrix = confusion_matrix(yTest, yPred)

class_namesEq = [None] * len(class_names)

for i in range(len(class_namesEq)):
    if class_names[i] == 1:
        class_namesEq[i] = "F.İ Görmüş Bina Penceresi"
    elif class_names[i] == 2:
        class_namesEq[i] = "F.İ Görmemiş Bina Penceresi"
    elif class_names[i] == 3:
        class_namesEq[i] = "F.İ Görmüş Araç Camı"
    elif class_names[i] == 5:
        class_namesEq[i] = "Konteyner Camı"
    elif class_names[i] == 6:
        class_namesEq[i] = "Yemek Takımları"
    elif class_names[i] == 7:
        class_namesEq[i] = "Far Camı"            

tableMatris = pd.DataFrame(cmatrix, index=class_namesEq, columns=class_namesEq)
st.write("""
    <div style="text-align: center;">
        PCA Uygulandıktan Sonra
    </div>
""", unsafe_allow_html=True)
st.write("Karışıklık Matrisi:")
st.table(tableMatris.style.set_table_attributes('style="font-size: 20px; width: 100%; text-align: center;"'))

accuracypca = accuracy_score(yTest, yPred)
precisionpca = precision_score(yTest, yPred, average='macro')
recallpca = recall_score(yTest, yPred, average='macro')
f1pca = f1_score(yTest, yPred, average='macro')

st.write("PCA Doğruluk:", accuracypca*100)
st.write("PCA Hassasiyet:", precisionpca*100)
st.write("PCA Duyarlılık:", recallpca*100)
st.write("PCA F1 Skoru:", f1pca*100)
st.write("""
    <div style="text-align: center;">
        86.3% doğruluk ile en başarılı modelim olmuştur.
    </div>
""", unsafe_allow_html=True)