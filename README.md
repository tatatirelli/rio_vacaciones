# Rio Vacaciones
## Previsor de anomalias em preços de hotéis no Rio de Janeiro

Entre na pasta do projeto rio_vacaciones_api
```bash
cd rio_vacaciones_api
```

Crie a venv
```
python -m venv venv
```

Ative a venv

Instalar as libs
```
pip install -r requirements.txt
```

Para treinar o modelo (*modelo já está treinado*)
```bash
python src/model/model_factory.py
```

Para rodar o servidor
```bash
uvicorn src.app.service:app --host 0.0.0.0 --port 4000 --reload
```


![image](https://github.com/user-attachments/assets/3168ddaa-525d-4d90-bea0-48ddddd930ed)



# Análise de Resultados


## Introdução

O objetivo inicial deste projeto era desenvolver um modelo de detecção de anomalias em séries temporais, integrando dados sazonais e períodos de eventos para gerar alertas de outliers no mercado imobiliário do Rio de Janeiro. No entanto, durante a análise, percebemos que o dataset do [Inside Airbnb](https://insideairbnb.com/rio-de-janeiro/), utilizado para o estudo, não contém dados coletados diariamente. Em vez disso, as coletas são feitas em intervalos específicos, o que inviabiliza a aplicação de técnicas de análise de séries temporais de forma contínua.

Além disso, embora existam informações com datas dispersas, como as avaliações dos imóveis, estas não são relevantes para o objetivo de criar um "gerador de alerta de outliers". Diante disso, o escopo do projeto foi ajustado para focar na detecção de anomalias utilizando técnicas de clusterização aplicadas a dados não temporais, explorando algoritmos como KMeans e KNN.

A nova abordagem visa identificar anomalias em um conjunto de dados de imóveis localizados no Rio de Janeiro, analisando padrões de preços e características que se destacam dos demais. Para alcançar esse objetivo, realizamos uma análise exploratória e limpeza de dados, seguida pela aplicação de técnicas de machine learning, como KMeans para clusterização e KNN para detecção de anomalias. Os resultados obtidos foram comparados com a biblioteca PyCaret para validar a eficácia do método proposto.

## Análise Exploratória & Limpeza de Dados

A análise exploratória foi realizada para entender a distribuição dos dados e identificar possíveis problemas como dados faltantes ou valores atípicos. As colunas originais incluíam informações como localização (latitude e longitude), número de banheiros, preços, avaliações, disponibilidade, entre outros.

Identificamos que algumas colunas continham muitos valores nulos e que muitas das colunas restantes ou eram redundantes ou irrelevantes, ou continham problemas, como no caso do 'room_type', que foi removida por ser preenchida majoritariamente com o valor "entire home/apt", sugerindo ser o padrão do Airbnb. Isso indica que proprietários não alteram este valor para evitar a exclusão de seus imóveis dos principais filtros de busca, tornando-o pouco informativo para a análise. Com base na análise exploratória, decidimos manter apenas as colunas mais relevantes: `latitude`, `longitude`, `bathrooms` (número de banheiros) e `price` (preço).

## Clusterização

Utilizamos o método do cotovelo (Elbow Method) para determinar o número ideal de clusters para o algoritmo KMeans. Após a análise do gráfico do cotovelo, restringimos o escopo de valores para um intervalo apropriado e aplicamos o método da silhouette para refinar a escolha do número de clusters. O tempo de processamento desta pré-análise foi de aproximadamente **25 minutos**, com diferentes valores de K testados para encontrar o melhor agrupamento, e por fim determinamos que o número ideal de clusters seria **13**.

## Decisão de Treinamento do KNN com Base no KMeans

Optamos por treinar um modelo KNN com base nos resultados do KMeans, já que o PyCaret, utilizado para comparação, aceita o KNN como modelo de detecção de anomalias, mas não o KMeans. Ao realizar essa abordagem, garantimos uma base comparativa consistente entre os modelos, permitindo analisar a eficácia do KNN quando treinado a partir de agrupamentos pré-estabelecidos pelo KMeans.

## Uso do Z-Score

O Z-Score foi utilizado para padronizar os dados antes de aplicar o KMeans e KNN. Essa normalização ajudou a garantir que todas as variáveis contribuíssem igualmente para a análise de similaridade, evitando distorções causadas por diferenças de escala entre as variáveis. O Z-Score também foi utilizado para detectar anomalias nos preços, sendo um cálculo de Z-Score para cada cluster separadamente, permitindo identificar anomalias de preços dentro de cada grupo. A ideia é sugerir que em um bairro/região específica, um preço muito alto ou muito baixo pode ser considerado uma anomalia, mesmo que seja um valor comum em outra região.

Para detectar anomalias dentro de cada cluster, calculamos o Z-Score do preço das propriedades de forma separada para cada cluster. A fórmula do Z-Score é:

#### $ Z = \frac{X - \mu}{\sigma} $

onde:
- \( Z \) é o Z-Score,
- \( X \) é o valor do preço da propriedade,
- \( $\mu$ \) é a média dos preços dentro do cluster, e
- \( $\sigma$ \) é o desvio padrão dos preços dentro do cluster.

Na prática, aplicamos este cálculo para cada cluster identificado pelo modelo KMeans. As propriedades com um Z-Score acima de 1 ou abaixo de -1 foram marcadas como anomalias, indicando preços estão acima ou abaixo de 1 desvio padrão de distância da média do cluster.

## Desafios com o PyCaret e Detecção de Anomalias

Ao utilizar o PyCaret, enfrentamos desafios no entendimento do que a biblioteca faz internamente com o modelo KNN, visto que o KNN é tipicamente um algoritmo supervisionado que requer um valor de `y`, mas o PyCaret alega utilizá-lo sem perguntar o `y`. Além disso, valores anômalos detectados, como `44` e `0`, não existiam no dataset original, sugerindo possíveis inconsistências ou problemas na detecção automática do PyCaret. O PyCaret inicialmente foi pensado para otimizar a detecção de anomalias em séries temporais, no entanto, o curso deste projeto nos levou a explorar sua aplicação em dados não temporais, o que pode ter contribuído para as dificuldades encontradas.

## Simplicidade e Efetividade da Abordagem Proposta

Nossa escolha de utilizar uma abordagem direta de clusterização e detecção de outliers se mostrou eficaz. O modelo KMeans, seguido pelo KNN, forneceu resultados claros e compreensíveis, próximos aos obtidos com o PyCaret, porém com total transparência no processo de análise e decisão.

## Conclusão

A abordagem escolhida, utilizando clusterização com KMeans seguida pela detecção de anomalias com KNN, provou ser eficiente e transparente, permitindo uma compreensão completa dos passos envolvidos e dos resultados obtidos. Embora o PyCaret ofereça uma solução de baixo código, os desafios e incertezas no entendimento de seus processos internos tornam nossa abordagem preferível, especialmente para casos onde a explicabilidade é crucial. Essa abordagem é adequada tanto para a demonstração da solução quanto para a produção de uma versão alfa de um projeto que pode ser refinado posteriormente, onde a transparência é essencial.
