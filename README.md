

Entre na pasta do projeto rio_vacaciones_api
```bash
cd rio_vacaciones_api
```


Para treinar o modelo
```bash
python src/model/model_factory.py
```

Para rodar o servidor
```bash
uvicorn src.app.service:app --host 0.0.0.0 --port 4000
```
