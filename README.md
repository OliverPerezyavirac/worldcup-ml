# World Cup ML Predictor

Proyecto en el cual empleo ML para analizar datos históricos, ranking FIFA y clasificatorias y tener una probabilidad de cual será el proximo campeón mundial.

## Stack
- Python 3.11
- Scikit-learn
- Random Forest
- Docker

## Estructura
- {data/raw}: datos originales en JSON
- {data/processed}: datos procesados
- {src}: código fuente
- models: modelos entrenados

## Ejecución con docker
```bash 
docker build -t worldcup-ml . 
docker run worldcup-ml