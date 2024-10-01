# ConnectFarm - API

Esse repositório contém a API do projeto ConnectFarm, responsável por coletar e disponibilizar dados ao app, além de fazer as análises de dados para o painel web.


## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`SUPABASE_USER` `SUPABASE_PASSWORD` `SUPABASE_HOST`  `SUPABASE_PORT` `SUPABASE_PORT`

`MONGO_URI`

`API-KEY` `SECRET_KEY` `ALGORITHM`

`ONESIGNAL_APP_ID` `ONESIGNAL_REST_API_KEY`## Rodando localmente

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

## Stack utilizada

**Banco de Dados:** PostgreSQL(Supabase) para dados do usuário e MongoDB(Atlas) para dados da fazenda.

**Back-end:** Python com FastAPI
## Relacionados
[Aplicativo](https://github.com/LauraPivoto/connect-farm)

[Painel Web](https://github.com/gabrielss2406/ConnectFarm-WebAPP)

[Simulador de localização e painel da balança](https://github.com/gabrielss2406/ConnectFarm-LocalizationSystem)

