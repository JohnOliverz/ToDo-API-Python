# ToDo API Python

API REST para gerenciamento de tarefas desenvolvida com FastAPI, SQLAlchemy e autenticação JWT.

## 🚀 Funcionalidades

- ✅ Autenticação JWT
- ✅ CRUD de usuários
- ✅ CRUD de tarefas
- ✅ Relacionamento User-Task
- ✅ Documentação automática (Swagger)
- ✅ Validação de dados com Pydantic

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **SQLite** - Banco de dados
- **JWT** - Autenticação via tokens
- **Pydantic** - Validação de dados
- **Bcrypt** - Hash de senhas

## 📋 Pré-requisitos

- Python 3.8+
- pip

## 🔧 Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd ToDo-API-Python
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Crie o banco de dados:**
```bash
python create_db.py
```

## ▶️ Executando

```bash
cd app
python main.py
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🔐 Autenticação

### Registrar usuário
```http
POST /register
Content-Type: application/x-www-form-urlencoded

username=joao&email=joao@email.com&password=senha123
```

### Login
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=joao&password=senha123
```

### Usar token
```http
Authorization: Bearer <seu-jwt-token>
```

## 📝 Endpoints

### Autenticação
- `POST /register` - Registrar usuário
- `POST /token` - Login

### Usuários
- `GET /users/me` - Obter perfil
- `PUT /users/me` - Atualizar perfil
- `DELETE /users/me` - Deletar conta

### Tarefas
- `POST /tasks` - Criar tarefa
- `GET /tasks` - Listar tarefas
- `PUT /tasks/{id}` - Atualizar tarefa
- `PATCH /tasks/{id}/complete` - Marcar como concluída
- `DELETE /tasks/{id}` - Deletar tarefa

## 📁 Estrutura do Projeto

```
ToDo-API-Python/
├── app/
│   ├── api/           # Endpoints da API
│   ├── database/      # Configuração do banco
│   ├── models/        # Modelos SQLAlchemy
│   ├── schemas/       # Schemas Pydantic
│   ├── auth.py        # Autenticação JWT
│   └── main.py        # Aplicação principal
├── .env               # Variáveis de ambiente
├── requirements.txt   # Dependências
└── create_db.py      # Script para criar BD
```

## 🧪 Testando

### Com Swagger UI
1. Acesse `http://localhost:8000/docs`
2. Registre um usuário em `/register`
3. Faça login em `/token`
4. Clique em "Authorize" e cole o token
5. Teste os endpoints protegidos

### Com Postman
1. Importe a collection do Swagger
2. Configure a autenticação Bearer Token
3. Teste os endpoints

## ⚙️ Variáveis de Ambiente

```env
SECRET_KEY=sua-chave-secreta-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Desenvolvido para estudos de FastAPI e APIs REST.