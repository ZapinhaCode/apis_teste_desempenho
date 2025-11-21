# APIs Teste de Desempenho

Projeto para testes de desempenho entre APIs desenvolvidas em Flask (Python) e Laravel (PHP), utilizando Docker Compose para orquestração dos serviços e PostgreSQL como banco de dados.

## Pré-requisitos

- Docker
- Docker Compose

## Estrutura do Projeto

```
├── flask_api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── laravel_api/
│   ├── Dockerfile
│   └── ... (Estrutura padrão Laravel)
├── gateway/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── Script Test Gateway/
│       ├── test_01.bash
│       ├── test_02.bash
│       └── test_03.bash
├── Jmeter Testes/
│   └── ... Resultados capturados no Jmeter
├── .gitignore
├── banco.sql
├── docker-compose.yml
├── DockerFile.db
└── README.md
```

## Serviços

- **db**: PostgreSQL
- **pgadmin**: Interface web para PostgreSQL
- **flask_api / flask_api2**: API em Flask (Python)
- **laravel_api / laravel_api2**: API em Laravel (PHP)
- **gateway**: NGINX para roteamento das APIs

## Configuração do Banco de Dados

- O banco de dados é inicializado automaticamente via arquivo `banco.sql`.
- Usuário padrão: `admin`
- Senha padrão: `supersecret`
- Nome do banco: `app_db`
- Os schemas utilizados são `flask_schema` (Flask) e `laravel_schema` (Laravel).

## Como executar

1. Certifique-se de ter o Docker e Docker Compose instalados.
2. Execute o comando abaixo na raiz do projeto:

   ```sh
   docker compose up --build
   ```

3. Os serviços serão expostos nas seguintes portas:
   - Flask API 1: `localhost:5001`
   - Flask API 2: `localhost:5003`
   - Laravel API 1: `localhost:5002`
   - Laravel API 2: `localhost:5004`
   - Gateway (NGINX): `localhost:8080`
   - pgAdmin: `localhost:5050`

## Acesso ao pgAdmin

- URL: [http://localhost:5050](http://localhost:5050)
- Login: `admin@admin.com`
- Senha: `admin`

## Endpoints Gerais das APIs

- `POST /api/users`  
  Cria um usuário.  
  Body (JSON):
  ```json
  {
    "name": "nomeUsuarioapi",
    "email": "usuario@api.com",
    "username": "usernameapi",
    "password": "senhaapi123"
  }
  ```

- `GET /api/users`  
  Lista todos os usuários.

- `GET /api/users/{id}`  
  Consulta usuário pelo ID.

- `PUT /api/users/{id}`  
  Atualiza usuário pelo ID.  
  Body (JSON):
  ```json
  {
    "name": "nomeUsuarioAtualizadoApi",
    "email": "usuarioAtualizado@api.com",
    "username": "usernameAtualizadoApi",
    "password": "senhaatualizadaapi123"
  }
  ```

- `DELETE /api/users/{id}`  
  Remove usuário pelo ID.

- `GET /api/whoami`
  Retorna o nome da instância que foi realizado a requisição


## Como testar as APIs

Você pode utilizar o Postman, Insomnia ou cURL para testar as APIs.


## Testes de Gateway

Scripts de teste estão disponíveis em `gateway/Script Test Gateway/` para simular requisições e medir desempenho. Para executar:

```sh
cd gateway/Script\ Test\ Gateway
bash test_01.bash
```

## Testes com JMeter

Os testes de carga das APIs não utilizaram o gateway, eles foram realizados via JMeter, e estão disponibilizados na pasta `Jmeter Testes`, onde lá terá os testes separados em seguintes pastas que sinalizam a configuração utilizada:
- Numero de usuários virtuais / Tempo de inicialização / Contador de interação


## Observações

- As APIs Flask e Laravel utilizam o mesmo banco de dados PostgreSQL, porém com schemas diferentes.
- O serviço pgAdmin pode ser acessado para gerenciar o banco de dados.
- O NGINX Gateway pode ser configurado para balanceamento de carga e roteamento entre as APIs.

### Detalhes do Gateway (NGINX)

O serviço `gateway` utiliza o NGINX para realizar o balanceamento de carga e o roteamento das requisições entre as APIs Flask e Laravel. A configuração do NGINX está definida no arquivo `gateway/nginx.conf`.

**Principais funções do gateway:**

- **Balanceamento de carga:**
  O NGINX distribui as requisições entre múltiplas instâncias das APIs (por exemplo, `flask_api` e `flask_api2`, `laravel_api` e `laravel_api2`), permitindo testes de desempenho e maior disponibilidade.

- **Roteamento de requisições:**
  O NGINX pode direcionar as requisições para diferentes APIs conforme o caminho da URL ou regras definidas. Por exemplo, requisições para `/flask/` podem ser roteadas para o backend Flask, e `/laravel/` para o backend Laravel.

- **Monitoramento e testes:**
  O gateway permite simular cenários de carga e testar o desempenho das APIs por meio dos scripts em `gateway/Script Test Gateway/`.

Consulte o arquivo `gateway/nginx.conf` para personalizar o balanceamento e roteamento conforme sua necessidade.


## Possíveis problemas

- **Porta ocupada:** Certifique-se de que as portas 5001, 5002, 5003, 5004, 5050 e 8080 estão livres antes de subir os containers.
- **Permissões:** Se houver erro de permissão nos volumes, execute `sudo chown -R $USER:$USER .` na raiz do projeto.
- **Banco não inicializa:** Verifique se o arquivo `banco.sql` está correto e se o serviço `db` está rodando.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o conteúdo abaixo:

```
MIT License

Copyright (c) 2025 Bernardo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```