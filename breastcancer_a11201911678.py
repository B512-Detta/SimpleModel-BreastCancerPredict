# -*- coding: utf-8 -*-
"""BreastCancer-A11201911678

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vFZYtfF4GZ8nbq17b547byklSf7rwfSM
"""

from google.colab import drive
drive.mount('/content/drive')

#import library
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB 
import matplotlib.pyplot as plt 
import seaborn as sns 
import missingno 

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

"""**1. Mengumpulkan Data**"""

#Membaca Dataset dari File ke Pandas dataFrame
#Load Dataset

url = '/content/drive/MyDrive/datasets/wdbc.data'
bc = pd.read_csv(url, header=None)

bc.head()

"""**2. Menelaah Data**"""

bc.rename(columns = {0: "Id", 
                     1: "Type",
                     2: "radius_mean",
                     3: "texture_mean",
                     4: "perimeter_mean ",
                     5: "area_mean ",
                     6: "Smootness_mean",
                     7: "compactness_mean",
                     8: "concavity_mean",
                     9: "concave points_mean",
                     10: "symmetry_mean",
                     11: "fractal_dimension_mean",
                     12: "radius_se",
                     13: "texture_se",
                     14: "perimeter_se",
                     15: "area_se",
                     16: "smoothness_se",
                     17: "compactness_se",
                     18: "concavity_se",
                     19: "concave points_se",
                     20: "symmetry_se",
                     21: "fractal_dimension_se",
                     22: "radius_worst",
                     23: "texture_worst",
                     24: "perimeter_worst",
                     25: "area_worst",
                     26: "smoothness_worst",
                     27: "compactness_worst",
                     28: "concavity_worst",
                     29: "concave points_worst",
                     30: "symmetry_worst",
                     31: "fractal_dimension_worst",}, inplace=True)

bc

# Menganalisa tipe dan relasi data

# Melihat tipe dataset
type(bc)

# Melihat ukuran dataset
print(bc.shape)

# Melihat informasi tipe data semua kolom
bc.info()

# Melihat distribusi Class (apa saja jenisnya)
bc['Type'].unique()

# Melihat distribusi Class (jumlahnya tiap Class)
bc['Type'].value_counts()

#Mengubah kata menjadi integer
bc['Type'].replace(['M','B'],[1,0],inplace=True)
bc['Type'].value_counts()

# Melihat distribusi kelas (visualisasi diagram batang dengan library seaborn)
sns.set(font_scale=1.4)
bc['Type'].value_counts().plot(kind='bar', figsize=(7,6), rot=0)
plt.xlabel("Tipe Diagnosis kanker payudara", labelpad=14)
plt.ylabel("Jumlah", labelpad=14)
plt.title("Tingkat diagnosis kanker payudara", y=1.02)

size = len(bc['texture_mean'])
area = np.pi * (15 * np.random.rand( size ))**2
colors = np.random.rand( size )
plt.xlabel("texture mean")
plt.ylabel("radius mean") 
plt.scatter(bc['texture_mean'], bc['radius_mean'], s=area, c=colors, alpha=0.5);

# Melihat deskripsi dataset
bc.describe()

"""**3. Memvalidasi Data**"""

# Cek dataframe yang missing dengan tanda "?"
bc.head()

# Merubah nilai "?" menjadi "NaN" dengan library numpy.nan
bc.replace("?", np.nan, inplace=True)

# Melihat hasil setelah dirubah => semula "?" menjadi "NaN"
bc.head()

# Mengecek apakah dataframe ada nilai kosong atau "NaN"
bc.isnull().values.any()

"""**DATA TIDAK ADA YANG MISSING VALUE**

**4. Membersihkan Data**
"""

# Melihat kembali prosentasi dari nilai kosong (NaN) untuk fitur 4 dan fitur 38 setelah dibersihkan
bc.loc[:,list(bc.loc[:,bc.isnull().any()].columns)].isnull().sum()/(len(bc))*100

"""**DATA SUDAH BERSIH**"""

# Melihat ukuran baris dan kolom dataframe
bc.shape

# Menghapus Data Duplikat dan melihat kembali ukuran baris & kolom dataframe
bc = bc.drop_duplicates()
bc.shape

"""**Tidak ada data yang sama**"""

# Menghapus fitur yang bernilai konstant
bc = bc.loc[:, bc.apply(pd.Series.nunique) !=1]
bc.shape

"""**Tidak ada fitur yang bernilai konstant**

**5. Mengontruksi Data**
"""

# Mengecek Representasi Fitur
bc.info()

# Mengubah yang tipe Object menjadi float64
bc['Type'] = bc['Type'].astype('float64')

# Mengecek Kembali Representasi Fitur
bc.info()

bc

# Membagi Atribut/ Fitur dan Label/Class
X = bc.iloc[:,2:32] #atribut
y = bc['Type'] #label

# Menampilkan X
X.head()

# Menampilkan y
y.head()

"""**DATA ORIGINAL**"""

# Membagi data menjadi training = 70% dan testing = 30%
X_train, X_test, Y_train, Y_test = train_test_split(X,y, test_size=0.3, random_state=2022)

# Menampilkan Data Train
X_train.head()

"""**DATA NORMALISASI**"""

# Normalisasi menggunakan StandardScaler
X_norm = StandardScaler().fit_transform(X)

# Melihat hasil normalisasi dengan StandardScaler
X_norm

X_train_norm, X_test_norm, Y_train_norm, Y_test_norm = train_test_split(X_norm,y, test_size=0.3, random_state=2022)

"""**DATA ORIGINAL PCA**"""

pca = PCA(random_state=2022)
pca.fit(X)
ori_pca_array = pca.transform(X)
ori_pca = pd.DataFrame(ori_pca_array)
print("Heads of Original_PCA:",ori_pca.head())
var_ratio = pca.explained_variance_ratio_
print("\n Explained Variance Ratio:",var_ratio)
sv = pca.singular_values_
print("\n Singular Value:",sv)

# Visualisasi Data Original PCA
cum_var_ratio = np.cumsum(var_ratio)

plt.figure(figsize=(10, 5))
plt.bar(range(len(var_ratio)), 
        var_ratio, 
        alpha=0.3333, 
        align='center', 
        label='individual explained variance', 
        color = 'g')
plt.step(range(len(cum_var_ratio)),
         cum_var_ratio, 
         where='mid',
         label='cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.legend(loc='best')
plt.show()

print("Cumulative explained ratio:",cum_var_ratio)

# Dipilih 10 PC
pca = PCA(n_components=10, random_state=2022)
pca.fit(X)
ori_pca_array = pca.transform(X)
ori_pca = pd.DataFrame(data=ori_pca_array, columns = ['PC1', 'PC2','PC3','PC4','PC5','PC6','PC7','PC8','PC9','PC10'])

X_train_pca, X_test_pca, Y_train_pca, Y_test_pca = train_test_split(ori_pca,y, test_size=0.3, random_state=2022)

X_train_pca

"""**DATA NORMALISASI PCA**"""

pca = PCA(random_state=2022)
pca.fit(X_norm)
norm_pca_array = pca.transform(X_norm)
norm_pca = pd.DataFrame(norm_pca_array)
print("Heads of iris_pca:",norm_pca.head())
var_ratio = pca.explained_variance_ratio_
print("\n Explained variance ratio:",var_ratio)
sv = pca.singular_values_
print("\n Singular Value:",sv)

# Visualisasi Data Normalisasi PCA
cum_var_ratio = np.cumsum(var_ratio)

plt.figure(figsize=(10, 5))
plt.bar(range(len(var_ratio)), 
        var_ratio, 
        alpha=0.3333, 
        align='center', 
        label='individual explained variance', 
        color = 'g')
plt.step(range(len(cum_var_ratio)),
         cum_var_ratio, 
         where='mid',
         label='cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.legend(loc='best')
plt.show()

print("Cumulative explained ratio:",cum_var_ratio)

# Dipilih 10 PC
pca = PCA(n_components=10, random_state=2022)
pca.fit(X_norm)
norm_pca_array = pca.transform(X_norm)
norm_pca = pd.DataFrame(data=norm_pca_array, columns = ['PC1', 'PC2','PC3','PC4','PC5','PC6','PC7','PC8','PC9','PC10'])

X_train_norm_pca, X_test_norm_pca, Y_train_norm_pca, Y_test_norm_pca = train_test_split(norm_pca,y, test_size=0.3, random_state=2022)

X_train_norm_pca

"""**6. Menentukan Label Data**

label sudah diputuskan dibagian transformasi data.

**7. Membangun Model**

**DECISION TREE**
"""

# menyiapkan parameter yang digunakan
parameters_dt = {
                "model__max_depth": np.arange(1,21),
                "model__min_samples_leaf": np.arange(1,101,2),
                "model__min_samples_split": np.arange(2,11),
                "model__criterion": ['gini','entropy'],
                "model__random_state": [2022]
}

# Pemodelan Decision Tree
classifier_dt_pipeline = Pipeline([
                          ('model',DecisionTreeClassifier()),                                                
                          ])

"""**PEMODELAN DENGAN DATA ORIGINAL**"""

ori_classifier_dt = GridSearchCV(classifier_dt_pipeline, parameters_dt, cv=3, n_jobs=-1)

ori_classifier_dt.fit(X_train,Y_train.ravel())

ori_classifier_dt.best_estimator_

for param_name in sorted(parameters_dt.keys()):
    print('%s: %r' %(param_name,ori_classifier_dt.best_params_[param_name]))

"""**PEMODELAN DENGAN DATA NORMALISASI**"""

norm_classifier_dt = GridSearchCV(classifier_dt_pipeline, parameters_dt, cv=3, n_jobs=-1)

norm_classifier_dt.fit(X_train_norm,Y_train_norm.ravel())

norm_classifier_dt.best_estimator_

for param_name in sorted(parameters_dt.keys()):
    print('%s: %r' %(param_name,norm_classifier_dt.best_params_[param_name]))

"""**PEMODELAN DENGAN DATA ORIGINAL DAN PCA**"""

ori_pca_classifier_dt = GridSearchCV(classifier_dt_pipeline, parameters_dt, cv=3, n_jobs=-1)

ori_pca_classifier_dt.fit(X_train_pca,Y_train_pca.ravel())

ori_pca_classifier_dt.best_estimator_

for param_name in sorted(parameters_dt.keys()):
    print('%s: %r' %(param_name,ori_pca_classifier_dt.best_params_[param_name]))

"""**PEMODELAN DENGAN DATA NORMALISASI DAN PCA**"""

norm_pca_classifier_dt = GridSearchCV(classifier_dt_pipeline, parameters_dt, cv=3, n_jobs=-1)

norm_pca_classifier_dt.fit(X_train_norm_pca,Y_train_norm_pca.ravel())

norm_pca_classifier_dt.best_estimator_

for param_name in sorted(parameters_dt.keys()):
    print('%s: %r' %(param_name,norm_pca_classifier_dt.best_params_[param_name]))

"""**9. Evaluasi Model**

**EVALUASI DATA ORIGINAL**
"""

ori_y_pred_dt_train = ori_classifier_dt.predict(X_train)

ori_accuracy_dt_train = accuracy_score(Y_train,ori_y_pred_dt_train)
print('Akurasi pada training set: ', ori_accuracy_dt_train)

ori_precision_dt_train = precision_score(Y_train,ori_y_pred_dt_train, average='micro')
print('Precision pada training set: ', ori_precision_dt_train)

ori_recall_dt_train = recall_score(Y_train,ori_y_pred_dt_train, average='micro')
print('Recall pada training set: ', ori_recall_dt_train)

ori_y_pred_dt_test = ori_classifier_dt.predict(X_test)

ori_accuracy_dt_test = accuracy_score(Y_test,ori_y_pred_dt_test)
print('Akurasi pada test set: ', ori_accuracy_dt_test)

ori_precision_dt_test = precision_score(Y_test,ori_y_pred_dt_test, average='micro')
print('Precision pada test set: ', ori_precision_dt_test)

ori_recall_dt_test = recall_score(Y_test,ori_y_pred_dt_test, average='micro')
print('Recall pada test set: ', ori_recall_dt_test)

# Visualisasi Confusion Matrix dengan Seaborn
sns.heatmap(confusion_matrix(Y_test,ori_y_pred_dt_test),annot=True,cmap='viridis', fmt='.0f')
plt.xlabel('Predicted Values', fontdict={'size':14}, labelpad=10)
plt.ylabel('Actual Values', fontdict={'size':14}, labelpad=10)
plt.title('Confusion Matrix pada bagian testing untuk data asli')
plt.show()

"""**EVALUASI DATA NORMALISASI**"""

norm_y_pred_dt_train = norm_classifier_dt.predict(X_train_norm)

norm_accuracy_dt_train = accuracy_score(Y_train_norm,norm_y_pred_dt_train)
print('Akurasi pada training set: ', norm_accuracy_dt_train)

norm_precision_dt_train = precision_score(Y_train_norm,norm_y_pred_dt_train, average='micro')
print('Precision pada training set: ', norm_precision_dt_train)

norm_recall_dt_train = recall_score(Y_train_norm,norm_y_pred_dt_train, average='micro')
print('Recall pada training set: ', norm_recall_dt_train)

norm_y_pred_dt_test = norm_classifier_dt.predict(X_test_norm)

norm_accuracy_dt_test = accuracy_score(Y_test_norm,norm_y_pred_dt_test)
print('Akurasi pada test set: ', norm_accuracy_dt_test)

norm_precision_dt_test = precision_score(Y_test_norm,norm_y_pred_dt_test, average='micro')
print('Precision pada test set: ', norm_precision_dt_test)

norm_recall_dt_test = recall_score(Y_test_norm,norm_y_pred_dt_test, average='micro')
print('Recall pada test set: ', norm_recall_dt_test)

# Visualisasi Confusion Matrix dengan Seaborn
sns.heatmap(confusion_matrix(Y_test_norm,norm_y_pred_dt_test),annot=True,cmap='viridis', fmt='.0f')
plt.xlabel('Predicted Values', fontdict={'size':14}, labelpad=10)
plt.ylabel('Actual Values', fontdict={'size':14}, labelpad=10)
plt.title('Confusion Matrix pada bagian testing untuk data asli')
plt.show()

"""**EVALUASI DENGAN DATA ORIGINAL DAN PCA**"""

ori_pca_y_pred_dt_train = ori_pca_classifier_dt.predict(X_train_pca)

ori_pca_accuracy_dt_train = accuracy_score(Y_train_pca,ori_pca_y_pred_dt_train)
print('Akurasi pada training set: ', ori_pca_accuracy_dt_train)

ori_pca_precision_dt_train = precision_score(Y_train_pca,ori_pca_y_pred_dt_train, average='micro')
print('Precision pada training set: ', ori_pca_precision_dt_train)

ori_pca_recall_dt_train = recall_score(Y_train_pca,ori_pca_y_pred_dt_train, average='micro')
print('Recall pada training set: ', ori_pca_recall_dt_train)

ori_pca_y_pred_dt_test = ori_pca_classifier_dt.predict(X_test_pca)

ori_pca_accuracy_dt_test = accuracy_score(Y_test_pca,ori_pca_y_pred_dt_test)
print('Akurasi pada test set: ', ori_pca_accuracy_dt_test)

ori_pca_precision_dt_test = precision_score(Y_test_pca,ori_pca_y_pred_dt_test, average='micro')
print('Precision pada test set: ', ori_pca_precision_dt_test)

ori_pca_recall_dt_test = recall_score(Y_test_pca,ori_pca_y_pred_dt_test, average='micro')
print('Recall pada test set: ', ori_pca_recall_dt_test)

# Visualisasi Confusion Matrix dengan Seaborn
sns.heatmap(confusion_matrix(Y_test_pca,ori_pca_y_pred_dt_test),annot=True,cmap='viridis', fmt='.0f')
plt.xlabel('Predicted Values', fontdict={'size':14}, labelpad=10)
plt.ylabel('Actual Values', fontdict={'size':14}, labelpad=10)
plt.title('Confusion Matrix pada bagian testing untuk data asli')
plt.show()

"""**EVALUASI DENGAN DATA NORMALISASI DAN PCA**"""

norm_pca_y_pred_dt_train = norm_pca_classifier_dt.predict(X_train_norm_pca)

norm_pca_accuracy_dt_train = accuracy_score(Y_train_norm_pca,norm_pca_y_pred_dt_train)
print('Akurasi pada training set: ', norm_pca_accuracy_dt_train)

norm_pca_precision_dt_train = precision_score(Y_train_norm_pca,norm_pca_y_pred_dt_train, average='micro')
print('Precision pada training set: ', norm_pca_precision_dt_train)

norm_pca_recall_dt_train = recall_score(Y_train_norm_pca,norm_pca_y_pred_dt_train, average='micro')
print('Recall pada training set: ', norm_pca_recall_dt_train)

norm_pca_y_pred_dt_test = norm_pca_classifier_dt.predict(X_test_norm_pca)

norm_pca_accuracy_dt_test = accuracy_score(Y_test_norm_pca,norm_pca_y_pred_dt_test)
print('Akurasi pada test set: ', norm_pca_accuracy_dt_test)

norm_pca_precision_dt_test = precision_score(Y_test_norm_pca,norm_pca_y_pred_dt_test, average='micro')
print('Precision pada test set: ', norm_pca_precision_dt_test)

norm_pca_recall_dt_test = recall_score(Y_test_norm_pca,norm_pca_y_pred_dt_test, average='micro')
print('Recall pada test set: ', norm_pca_recall_dt_test)

# Visualisasi Confusion Matrix dengan Seaborn
sns.heatmap(confusion_matrix(Y_test_norm_pca,norm_pca_y_pred_dt_test),annot=True,cmap='viridis', fmt='.0f')
plt.xlabel('Predicted Values', fontdict={'size':14}, labelpad=10)
plt.ylabel('Actual Values', fontdict={'size':14}, labelpad=10)
plt.title('Confusion Matrix pada bagian testing untuk data asli')
plt.show()

models = [
          ('Decision Tree Data Original', ori_accuracy_dt_train, ori_accuracy_dt_test),
          ('Decision Tree Data Normalisasi', norm_accuracy_dt_train, norm_accuracy_dt_test),
          ('Decision Tree PCA Data Original', ori_pca_accuracy_dt_train, ori_pca_accuracy_dt_test),    
          ('Decision Tree PCA Data Normalisasi', norm_pca_accuracy_dt_train, norm_pca_accuracy_dt_test),      
         ]

# Melakukan perbandingan hasil training akurasi dan test akurasi dengan 4 model
predict = pd.DataFrame(data = models, columns=['Model', 'Training Accuracy', 'Test Accuracy'])
predict

models_comparison = [
                        ('Decision Tree Data Original', ori_accuracy_dt_test, ori_recall_dt_test, ori_precision_dt_test), 
                        ('Decision Tree Data Normalisasi', norm_accuracy_dt_test, norm_recall_dt_test, norm_precision_dt_test),
                        ('Decision Tree PCA Data Original', ori_pca_accuracy_dt_test, ori_pca_recall_dt_test, ori_pca_precision_dt_test),
                        ('Decision Tree PCA Data Normalisasi', norm_pca_accuracy_dt_test, norm_pca_recall_dt_test, norm_pca_precision_dt_test),                  
                    ]

# Melakukan perbandingan hasil Akurasi, Presisi dan Recall pada data Testing dengan 4 model
comparison = pd.DataFrame(data = models_comparison, columns=['Model', 'Accuracy', 'Recall', 'Precision'])
comparison

# Visualisasi Perbandingan 4 model dengan Seaborn

f, axes = plt.subplots(2,1, figsize=(14,10))

predict.sort_values(by=['Training Accuracy'], ascending=False, inplace=True)

sns.barplot(x='Training Accuracy', y='Model', data = predict, palette='Blues_d', ax = axes[0])
#axes[0].set(xlabel='Region', ylabel='Charges')
axes[0].set_xlabel('Training Accuracy', size=16)
axes[0].set_ylabel('Model')
axes[0].set_xlim(0,1.0)
axes[0].set_xticks(np.arange(0, 1.1, 0.1))

predict.sort_values(by=['Test Accuracy'], ascending=False, inplace=True)

sns.barplot(x='Test Accuracy', y='Model', data = predict, palette='Greens_d', ax = axes[1])
#axes[0].set(xlabel='Region', ylabel='Charges')
axes[1].set_xlabel('Test Accuracy', size=16)
axes[1].set_ylabel('Model')
axes[1].set_xlim(0,1.0)
axes[1].set_xticks(np.arange(0, 1.1, 0.1))

plt.show()

"""# Kesimpulan :
- Model terbaik dari Dataset Kanker Payudara adalah menggunakan Decision Tree PCA Data Normalisasi dengan nilai akurasi tertinggi pada Data Training sebesar 100% dan akurasi tertinggi pada Data Testing sebesar 95%.
"""