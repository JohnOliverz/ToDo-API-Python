# ToDo API Python

API REST para gerenciamento de tarefas desenvolvida com FastAPI, SQLAlchemy e autenticação JWT.

## 🚀 Funcionalidades

- ✅ Autenticação JWT com segurança aprimorada
- ✅ CRUD completo de usuários
- ✅ CRUD completo de tarefas
- ✅ Sistema de status flexível (Pendente, Em Progresso, Concluída)
- ✅ Relacionamento User-Task
- ✅ Documentação automática (Swagger)
- ✅ Validação robusta de dados com Pydantic
- ✅ Tratamento de erros personalizado
- ✅ Formato JSON padronizado
- ✅ Variáveis de ambiente para segurança

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **SQLite** - Banco de dados
- **JWT** - Autenticação via tokens
- **Pydantic** - Validação de dados
- **Bcrypt** - Hash de senhas
- **Python-JOSE** - Manipulação de tokens JWT
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

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
```json
POST /register
Content-Type: application/json

{
  "username": "joao_silva",
  "email": "joao@email.com",
  "password": "senha123"
}
```

### Login
```json
POST /token
Content-Type: application/json

{
  "username": "joao_silva",
  "password": "senha123"
}
```

### Usar token
```http
Authorization: Bearer <seu-jwt-token>
```

## 📝 Endpoints

### Autenticação
- `POST /register` - Registrar usuário
- `POST /token` - Login

### Usuários (Requer autenticação)
- `GET /users/me` - Obter perfil do usuário atual
- `PUT /users/me` - Atualizar perfil do usuário atual
- `DELETE /users/me` - Deletar conta do usuário atual

### Tarefas (Requer autenticação)
- `POST /tasks` - Criar nova tarefa
- `GET /tasks` - Listar todas as tarefas do usuário
- `PUT /tasks/{id}` - Atualizar tarefa específica
- `PATCH /tasks/{id}/status` - Atualizar status da tarefa
- `DELETE /tasks/{id}` - Deletar tarefa específica

## 🎯 Sistema de Status de Tarefas

As tarefas possuem 3 status possíveis:

- **Pendente** (padrão) - Tarefa criada mas não iniciada
- **Em Progresso** - Tarefa sendo executada
- **Concluída** - Tarefa finalizada

### Exemplo de atualização de status:
```json
PATCH /tasks/1/status
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "Em Progresso"
}
```

## 📁 Estrutura do Projeto

```
ToDo-API-Python/
├── app/
│   ├── api/           # Endpoints da API
│   │   ├── auth.py    # Autenticação
│   │   ├── users.py   # Usuários
│   │   └── tasks.py   # Tarefas
│   ├── common/        # Módulos compartilhados
│   │   ├── auth.py    # Funções de autenticação
│   │   ├── exceptions.py # Tratamento de erros
│   │   └── validators.py # Validadores customizados
│   ├── database/      # Configuração do banco
│   ├── models/        # Modelos SQLAlchemy
│   ├── schemas/       # Schemas Pydantic
│   └── main.py        # Aplicação principal
├── .env               # Variáveis de ambiente
├── .env.example       # Template de variáveis
├── requirements.txt   # Dependências
├── create_db.py      # Script para criar BD
└── migrate_tasks.py  # Script de migração
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
3. Teste os endpoints com dados JSON

### Exemplos de Teste

**Criar tarefa:**
```json
POST /tasks
{
  "title": "Estudar FastAPI",
  "description": "Ler documentação e fazer exercícios"
}
```

**Atualizar status:**
```json
PATCH /tasks/1/status
{
  "status": "Concluída"
}
```

## ⚙️ Variáveis de Ambiente

```env
SECRET_KEY=sua-chave-secreta-jwt-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🔒 Validações Implementadas

### Usuários
- Username: 3-50 caracteres, apenas letras, números e underscore
- Senha: Mínimo 6 caracteres, deve conter letra e número
- Email: Formato válido obrigatório

### Tarefas
- Título: Obrigatório, máximo 200 caracteres
- Descrição: Opcional, máximo 1000 caracteres
- Status: Apenas valores permitidos (Pendente, Em Progresso, Concluída)

## 🛡️ Tratamento de Erros

- **400** - Dados inválidos
- **401** - Não autenticado
- **404** - Recurso não encontrado
- **409** - Conflito (usuário já existe)
- **422** - Erro de validação
- **500** - Erro interno do servidor

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Desenvolvido para estudos de FastAPI e APIs REST modernas.