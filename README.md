# Protein Tracker

Calculadora e rastreador de consumo de proteína diária, com interface web feita em Flask e persistência em SQLite.

O projeto calcula a meta diária de proteína com base no peso e no objetivo da pessoa (manutenção, ganho de massa ou perda de gordura), permite acompanhar o quanto já foi consumido ao longo do dia, e mantém um histórico com a sequência de dias seguidos batendo a meta.

Começou como um script de terminal em Python, depois virou uma aplicação web, e hoje já suporta múltiplos usuários cadastrados no mesmo banco.

## Como funciona

1. Na tela inicial, você escolhe um usuário já cadastrado ou cria um novo informando nome, peso e objetivo
2. O app calcula a meta diária de proteína daquela pessoa
3. Ao longo do dia, você vai adicionando o quanto consumiu em cada refeição
4. Um anel de progresso mostra visualmente o quanto falta pra bater a meta
5. Ao salvar o dia, o registro entra no histórico — a aba Histórico mostra a sequência atual de dias seguidos batendo a meta, a maior sequência já alcançada, e um resumo com todos os dias registrados
6. É possível trocar de usuário a qualquer momento, mantendo o histórico de cada um separado

## Como rodar localmente

Pré-requisitos: Python 3 instalado.

```bash
# clone o repositório
git clone https://github.com/Arthur-Isidoro/Protein-Tracker.git
cd Protein-Tracker

# instale as dependências
pip install -r requirements.txt

# crie o banco de dados (só precisa rodar uma vez)
python database.py

# rode o app
python app.py
```

Depois é só abrir `http://127.0.0.1:5000` no navegador.

## Estrutura do projeto

```
Protein-Tracker/
├── app.py                  # rotas Flask, lógica de cálculo da meta e sessão do usuário
├── database.py              # criação das tabelas e todas as queries no SQLite
├── requirements.txt         # dependências do projeto
├── protein_tracker.db       # banco de dados SQLite (gerado localmente, fora do repositório)
├── templates/
│   ├── cadastro.html        # lista de usuários cadastrados + criação de novo usuário
│   ├── tracker.html         # página de acompanhamento do consumo do dia
│   └── historico.html       # histórico de dias, streak atual, maior streak e resumo
└── static/
    └── style.css             # estilos das páginas
```

## Banco de dados

O app usa SQLite (`protein_tracker.db`), com duas tabelas:

- **usuarios** — nome, objetivo e meta de proteína (mínima e máxima) de cada pessoa cadastrada
- **registros_diarios** — um registro por usuário por dia, com o quanto foi consumido, a meta do dia, e se ela foi atingida

O arquivo `.db` não vai para o repositório (está no `.gitignore`) — cada pessoa que clonar o projeto gera o próprio banco localmente rodando `python database.py`.

## Como a meta é calculada

| Objetivo | Proteína por kg de peso corporal |
|---|---|
| Manutenção | 1.6 g/kg |
| Ganho de massa | 1.8 g/kg a 2.2 g/kg |
| Perda de gordura | 2.0 g/kg a 2.4 g/kg |

## Possíveis próximos passos

- Migrar de SQLite para MySQL
- Separar a lógica de cálculo em um módulo próprio
- Autenticação real (login com senha) em vez de seleção livre de usuário
- Editar ou apagar registros de dias já salvos
- Gráfico de evolução do consumo ao longo do tempo

## Sobre

Projeto pessoal criado para praticar Python após concluir um curso introdutório de programação.