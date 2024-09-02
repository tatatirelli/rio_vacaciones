import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump #, load

#%%
# Concatenação de datasets
df1 = pd.read_csv('data/1RioSeptember2023/listings.csv')
df2 = pd.read_csv('data/2RioDecember2023/listings.csv')
df3 = pd.read_csv('data/3RioMarch2024/listings.csv')
df4 = pd.read_csv('data/4RioJune2024/listings.csv')
df = pd.concat([df1, df2, df3, df4], ignore_index=True)
del df1, df2, df3, df4

# Limpeza de dados
df = df.dropna(subset=['price', 'bathrooms'])
df = df[['latitude', 'longitude', 'bathrooms', 'price']]
df.price = df.price.str.replace('$', '').str.replace(',', '').astype(float)
df = df[df['price'] > 0]
df = df[df['bathrooms'] < 16]

#%%
# Criar normalizadores de dados
scaler = StandardScaler()
df[['latitude', 'longitude', 'bathrooms']] = scaler.fit_transform(df[['latitude', 'longitude', 'bathrooms']])

mean_price = df['price'].mean()
std_price = df['price'].std()

df['price'] = (df['price'] - mean_price) / std_price


#%%
# Treinar modelo de clusterização com KMeans
kmeans = KMeans(n_clusters=15, random_state=0)

series_cluster_kmeans = kmeans.fit_predict(df[['latitude', 'longitude', 'bathrooms', 'price']])

# Treinar modelo de classificação com KNN
knn = KNeighborsClassifier(n_neighbors=4, n_jobs=-1)

knn.fit(df[['latitude', 'longitude', 'bathrooms', 'price']], series_cluster_kmeans)
df['cluster_knn'] = knn.predict(df[['latitude', 'longitude', 'bathrooms', 'price']])
clusters_knn = df['cluster_knn'].unique()

#%%
# Criar lista de modelos de predição de anomalias para cada cluster
anomaly_models = []
for cluster in clusters_knn:
    # Filtra o DataFrame para pegar apenas as entradas do cluster atual
    df_cluster = df[df['cluster_knn'] == cluster]

    # Calcula a média e o desvio padrão dos preços no cluster atual
    cluster_mean = df_cluster['price'].mean()
    cluster_std = df_cluster['price'].std()

    # Armazena o modelo RANSAC e as estatísticas do cluster para uso futuro
    anomaly_model = {
        'cluster': cluster,   # Número do cluster
        'mean': cluster_mean,  # Média dos preços do cluster
        'std': cluster_std,    # Desvio padrão dos preços do cluster
    }
    anomaly_models.append(anomaly_model)  # Adiciona o modelo à lista de modelos de anomalias

#%%
# df[['latitude', 'longitude', 'bathrooms']] = scaler.inverse_transform(df[['latitude', 'longitude', 'bathrooms']])
# df['price'] = df['price'] * std_price + mean_price

#%%
# Classe para predição de cluster
class RioVacation:
    def __init__(self, scaler, mean_price, std_price, knn, anomaly_models):
        # Inicializa as variáveis de instância
        self.scaler = scaler
        self.mean_price = mean_price
        self.std_price = std_price
        self.knn = knn
        self.anomaly_models = anomaly_models

    def __transform(self, input_df):
        input_df[['latitude', 'longitude', 'bathrooms']] = self.scaler.transform(input_df[['latitude', 'longitude', 'bathrooms']])
        input_df['price'] = (input_df['price'] - self.mean_price) / self.std_price
        return input_df

    def __inverse_transform(self, input_df):
        input_df[['latitude', 'longitude', 'bathrooms']] = self.scaler.inverse_transform(input_df[['latitude', 'longitude', 'bathrooms']])
        input_df['price'] = input_df['price'] * self.std_price + self.mean_price
        return input_df

    def predict(self, input_df):
        # Normaliza os dados de entrada
        input_df = self.__transform(input_df)

        # Prediz o cluster usando o modelo KNN treinado
        input_df['cluster_knn'] = self.knn.predict(input_df[['latitude', 'longitude', 'bathrooms', 'price']])

        # Detectar anomalias para cada linha de entrada
        input_df['anomaly'] = 0
        for index, row in input_df.iterrows():

            untransformed_temp_price = row['price'] * self.std_price + self.mean_price
            if untransformed_temp_price < 33:
                input_df.at[index, 'anomaly'] = 1
                continue

            # Encontrar o modelo de anomalia correspondente ao cluster previsto
            model = next((m for m in self.anomaly_models if m['cluster'] == row['cluster_knn']), None)
            if model:
                # Calcula o Z-score para a detecção de anomalias
                price_z_score = (row['price'] - model['mean']) / model['std']
                # Marca como anomalia se o Z-score for maior que 1
                input_df.at[index, 'anomaly'] = 1 if abs(price_z_score) > 1 else 0

        # Reverte a normalização dos dados para os valores originais
        input_df = self.__inverse_transform(input_df)
        return input_df


#%%
# Salvar modelo
dump(
    RioVacation(
        scaler=scaler,
        mean_price=mean_price,
        std_price=std_price,
        knn=knn,
        anomaly_models=anomaly_models
    ),
    'artifacts/models/rio_vac_scale_n_predict.pkl'
)

# # Carregar modelo
# rio_vacation = load('../../artifacts/models/rio_vac_scale_n_predict.pkl')
#
#
#%%
# output_df = rio_vacation.predict(df)
# #%%
# print(output_df[output_df['anomaly'] == 1][['bathrooms', 'price']].describe())
# #%%
# print(output_df[output_df['anomaly'] == 0].info())
#
# #%%
# # Exemplo de uso
# df_to_input = pd.DataFrame({
#     'latitude': [-22.965148],
#     'longitude': [-43.175437],
#     'bathrooms': [3],
#     'price': [32]
# })
#
# output_df = rio_vacation.predict(df_to_input)
#
# print(output_df)