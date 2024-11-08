import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from scipy import stats

import matplotlib
matplotlib.use('Agg')

# Carregar dados
df = pd.read_csv("giant_database.csv")

# Estatísticas e Outliers
print("\nResumo estatístico dos parâmetros:")
print(df.describe())

# Identificar Outliers com base no Z-score
z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
outliers = df[(z_scores > 3).any(axis=1)]
print("\nOutliers Detectados:")
print(outliers)

# Matriz de Correlação
df['total_samples'] = df['numPos'] + df['numNeg']
correlation_matrix = df.corr()
print("\nMatriz de Correlação (incluindo total_samples):")
print(correlation_matrix['Precision'].sort_values(ascending=False))

# PCA para entender variabilidade
pca = PCA(n_components=2)
pca.fit(df[['numPos', 'numNeg', 'numStages', 'maxFalseAlarmRate', 'minHitRate', 'maxDepth', 'maxWeakCount']])
print("\nExplained Variance Ratio:", pca.explained_variance_ratio_)

# Regressão Linear Múltipla para precisão
X = df[['numPos', 'numNeg', 'numStages', 'maxFalseAlarmRate', 'minHitRate', 'maxDepth', 'maxWeakCount']]
y = df['Precision']
linear_model = LinearRegression().fit(X, y)
print("\nResumo da Regressão Linear Múltipla:")
import statsmodels.api as sm
X_sm = sm.add_constant(X)
model = sm.OLS(y, X_sm).fit()
print(model.summary())

# Gráficos
output_dir = "graficos"
os.makedirs(output_dir, exist_ok=True)

# Precision x numPos e Precision x numNeg 
plt.figure()
plt.scatter(df['numPos'], df['Precision'], color='b', alpha=0.6, label='numPos')
plt.scatter(df['numNeg'], df['Precision'], color='r', alpha=0.6, label='numNeg')
plt.title("Precision x numPos e numNeg")
plt.xlabel("Samples")
plt.ylabel("Precision")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, "precision_numPos_numNeg.png"))

# Precision x numStages
plt.figure()
plt.scatter(df['numStages'], df['Precision'], color='g', alpha=0.6)
plt.title("Precision x numStages")
plt.xlabel("numStages")
plt.ylabel("Precision")
plt.grid()
plt.savefig(os.path.join(output_dir, "precision_numStages.png"))

# Sugestão de Intervalos de Parâmetros com Base na Análise Estatística
suggested_ranges = {}
for param in ["numPos", "numNeg", "numStages", "maxFalseAlarmRate", "minHitRate", "maxDepth", "maxWeakCount"]:
    corr = correlation_matrix['Precision'][param]
    
    if corr > 0:  # Parâmetro tem correlação positiva com precisão
        suggested_ranges[param] = (int(df[param].quantile(0.5)), int(df[param].max())) if param != "maxFalseAlarmRate" and param != "minHitRate" else (df[param].quantile(0.5), df[param].max())
    else:  # Parâmetro tem correlação negativa ou neutra
        suggested_ranges[param] = (int(df[param].min()), int(df[param].quantile(0.5))) if param != "maxFalseAlarmRate" and param != "minHitRate" else (df[param].min(), df[param].quantile(0.5))

print("\nSugestão de Intervalos de Parâmetros para Aleatorização com Base na Análise:")
for param, interval in suggested_ranges.items():
    print(f"{param}: {interval}")

# Sugestão de Parâmetros para Execução Única
best_params = {
    "numPos": int(df['numPos'].median()),  # Mediana de numPos
    "numNeg": int(df['numNeg'].median()),  # Mediana de numNeg
    "numStages": int(df['numStages'].median()),  # Mediana de numStages
    "maxFalseAlarmRate": df['maxFalseAlarmRate'].median(),  # Mediana de maxFalseAlarmRate
    "minHitRate": df['minHitRate'].median(),  # Mediana de minHitRate
    "maxDepth": int(df['maxDepth'].median()),  # Mediana de maxDepth
    "maxWeakCount": int(df['maxWeakCount'].median())  # Mediana de maxWeakCount
}

print("\nSugestão de Parâmetros para Execução Única:")
for param, value in best_params.items():
    print(f"{param}: {value}")

#92