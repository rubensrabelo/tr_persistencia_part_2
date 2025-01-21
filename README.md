# Sistema de Gestão de Projetos

Um sistema projetado para organizar e gerenciar projetos, tarefas e colaboradores, utilizando uma estrutura relacional de dados. Permite rastrear o progresso, gerenciar atribuições e gerar relatórios detalhados de produtividade.

## Diagrama de classes

``` mermaid
classDiagram
  direction LR
  class Collaborator {
    name: str
    email: str
    function: str
  }
  
  class Task {
    name: str
    description: str
    delivery_forecast: datetime
    created_date: datetime
    updated_date: datetime
    status: StatusEnum
  }
  
  class Project {
    name: string
    description: string
    start_date: datetime
    created_date: datetime
    updated_date: datetime
    status: StatusEnum
  }

  Project "1"-- "*" Task
  Task "*"-- "*" Collaborator

```

## Estrutura de Pastas

### **main**
O arquivo principal que inicializa a aplicação, configura as dependências e inicia o servidor da API.

### **database**
Responsável pela configuração e conexão do banco de dados. Este arquivo gerencia a criação de tabelas, conexões e operações de banco de dados.

### **Pyproject.toml**
Este arquivo contém as configurações do projeto, incluindo dependências, configurações do ambiente e informações sobre como o projeto é construído e gerido.

### **.gitignore**
Arquivo utilizado para especificar quais arquivos e pastas devem ser ignorados pelo Git

### **Models/**
Contém as representações das entidades principais do sistema, que são usadas para definir as tabelas no banco de dados. Aqui estão os modelos que estruturam as informações:
- `project.py`: Define a estrutura e os atributos dos projetos.
- `task.py`: Define a estrutura e os atributos das tarefas associadas a cada projeto.
- `collaborator.py`: Define os colaboradores que trabalham nos projetos e suas informações.
- `assignment.py`: Define a relação entre colaboradores e tarefas, indicando quais tarefas estão atribuídas a quais colaboradores.
- **enum/**: Esta subpasta armazena enums utilizados em diferentes partes do sistema.
  - `status_enum.py`: Define os diferentes status que uma tarefa ou projeto pode ter (ex.: pendente, em andamento, concluído).

### **DTO/** (Data Transfer Object)
Contém objetos utilizados para transferir dados entre diferentes camadas do sistema (por exemplo, entre a camada de banco de dados e a API). Os DTOs ajudam a estruturar e otimizar o tráfego de dados:
- `project_dto.py`: Define o formato dos dados transferidos para o projeto.
- `task_dto.py`: Define o formato dos dados transferidos para as tarefas.
- `collaborator_dto.py`: Define o formato dos dados transferidos para os colaboradores.
- `statistic_dto.py`: Define o formato dos dados utilizados para relatórios de produtividade e estatísticas de progresso.

### **API/**
Esta pasta contém os arquivos responsáveis por controlar a lógica de negócios da aplicação e definir as rotas de acesso à API, garantindo a interação com o sistema:
- `Controller.py`: Contém a lógica central para o processamento de requisições e manipulação dos dados.
- **Routes/**: Subpasta que organiza as rotas para cada recurso da aplicação.
  - `project.py`: Define as rotas para gerenciamento dos projetos (criação, leitura, atualização, exclusão).
  - `task.py`: Define as rotas para o gerenciamento das tarefas associadas aos projetos.
  - `collaborator.py`: Define as rotas para o gerenciamento dos colaboradores e suas respectivas atribuições.
  - `statistic.py`: Define as rotas para obter e gerar relatórios de produtividade e estatísticas sobre o andamento dos projetos.


## Configuração do Projeto

### Requisitos

Antes de começar, verifique se você possui os seguintes requisitos:

- **Python 3.10+**
- **FastAPI** – Framework para criação de APIs.
- **SQLModel** – Biblioteca para trabalhar com bancos de dados relacionais.
- **SQLite** – Banco de dados utilizado no projeto.
- **Gerenciador de dependências uv** – Utilizado para gerenciar as dependências do projeto.

### Instalação

Siga os passos abaixo para configurar o projeto:

#### 1. Clone o repositório

Clone o repositório do projeto no seu diretório local:

```bash
git clone https://github.com/rubensrabelo/tr_persistencia_part_2.git
```

Para rodar a aplicação localmente, siga os passos abaixo:

### 1. Ativar o Ambiente Virtual

Ative o ambiente virtual para isolar as dependências do projeto. No terminal, execute o seguinte comando:

```bash
source .venv/bin/activate
```

### 2. Instalar as Dependências
Com o ambiente virtual ativado, instale as dependências listadas no arquivo pyproject.toml utilizando o gerenciador de dependências `uv`:

```bash
uv add pyproject
```

3. Executar a Aplicação

Após a instalação das dependências, você pode iniciar o servidor da aplicação com o comando:

```bash
fast dev main.py
```

### 3. Acesse a documentação interativa da API no navegador:

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

