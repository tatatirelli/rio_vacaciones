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
