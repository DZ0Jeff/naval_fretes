# NAVAL FRETES

## sistema de automação de fretes marítimos

---

## instalação

(opcional) recomendavel instalar o ambiente desenvolvimento antes

```
pip install virtualenv
python -m venv venv && .\venv\scripts\activate
```

instale as depênciencias:

```
pip install -r requirements.txt
```

crie um arquivo ".env" com as informações do ".env.example", trocando os campos necessários

para rodar rode o comando:

```
python main.py
```

## modo de uso

como o servidor rodando, possui a seguintes requisições da api

http://127.0.0.1:5000/search (POST)

{
	"from":"nome da cidade de saída",
	"to":"nome da cidade de saída",
	"commodity": "mercadoria",
	"date": "data de embarcação (0000-00-00)"
}

ou com curl:

curl --request POST \
  --url http://127.0.0.1:5000/search \
  --header 'Content-Type: application/json' \
  --data '{
	"from":"Santos",
	"to":"london",
	"commodity": "Chocolate",
	"date": "2022-11-15"
}'

requisição que retorna os dados de frete de embarcações com base nos dados de entrada (JSON):

- from: nome da cidade de saída
- to: nome da cidade de saída
- commodity:  mercadoria
- date: data de embarcação (0000-00-00) 
