# ConnectFarm - API

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white) ![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white) ![Supabase](https://img.shields.io/badge/Supabase-181818?style=for-the-badge&logo=supabase&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)

Esse repositório contém a API do projeto ConnectFarm(projeto apresentado na Fetin de 2024), responsável por coletar e disponibilizar dados ao app, além de fazer as análises de dados para o painel web.


## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`SUPABASE_USER` `SUPABASE_PASSWORD` `SUPABASE_HOST`  `SUPABASE_PORT` `SUPABASE_PORT`

`MONGO_URI`

`API-KEY` `SECRET_KEY` `ALGORITHM`

`ONESIGNAL_APP_ID` `ONESIGNAL_REST_API_KEY`

## Rodando localmente

Clone o projeto

```bash
  git clone https://link-para-o-projeto
```

Entre no diretório do projeto

```bash
  cd my-project
```

Instale as dependências

```bash
  pip install -r requirements.txt
```

Rode o projeto

```bash
  python -m uvicorn api.api:app --reload
```
## Rodando os testes

Para rodar os testes do projeto é muito simples, apenas rode o seguinte comando

```bash
  pytest
```

## Documentação

[Documentação](https://connect-farm-api.vercel.app/docs)


## Relacionados
[Aplicativo](https://github.com/LauraPivoto/connect-farm)

[Painel Web](https://github.com/gabrielss2406/ConnectFarm-WebAPP)

[Simulador de localização e painel da balança](https://github.com/gabrielss2406/ConnectFarm-LocalizationSystem)

