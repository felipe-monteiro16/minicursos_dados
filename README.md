# Pipeline ETL Básico

Pipeline de extração, transformação e carregamento de dados simplificado, utilizando base de dados da ONS, download incremental com `curl_cffi`, transfomação com `pandas`. 

## Pré-requisitos

* **Python**: versão 3.11.

## Execução

### Linux
```
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Windows
```
py -3.11 -m venv venv
./venv/Scripts/activate
pip install -r ./requirements.txt
python ./main.py
```