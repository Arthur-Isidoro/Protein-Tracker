# Protein Tracker

Calculadora e rastreador de consumo de proteína diária, com interface web feita em Flask e persistência em SQLite.

O projeto calcula a meta diária de proteína com base no peso e no objetivo da pessoa (manutenção, ganho de massa ou perda de gordura), permite acompanhar o consumo por refeição ao longo do dia, mantém um histórico com estatísticas e gráfico, e suporta múltiplos usuários cadastrados no mesmo banco.

Começou como um script de terminal em Python, virou uma aplicação web simples, e evoluiu até essa versão com histórico completo e registro por refeição.

## Como funciona

1. Na tela inicial, você escolhe um usuário já cadastrado ou cria um novo informando nome, peso e objetivo
2. O app calcula a meta diária de proteína daquela pessoa
3. Ao longo do dia, você registra o que consumiu por refeição (ex: "Café da manhã" → Ovos 18g, Iogurte 12g) — o consumo total do dia é a soma de todos os itens
4. Um anel de progresso mostra visualmente o quanto falta pra bater a meta, com um aviso explícito quando ela é atingida
5. A virada de dia é automática: assim que a data muda, o consumo do dia anterior é salvo no histórico sozinho, sem precisar clicar em nada
6. A aba Histórico mostra:
   - A sequência atual de dias seguidos batendo a meta e a maior sequência já alcançada (ambas quebram corretamente se faltar um dia sem registro)
   - Estatísticas: média geral, média dos últimos 7 e dos últimos 30 dias
   - Um gráfico de barras dos últimos 30 dias, com uma linha marcando a meta de cada dia
   - Uma tabela com todos os dias registrados
7. Clicando em qualquer data do histórico, você vê o detalhe daquele dia (meta, consumido, status) e também as refeições detalhadas daquele dia, quando disponíveis
8. É possível trocar de usuário a qualquer momento, mantendo o histórico de cada um separado

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

### Testar rapidamente

Se quiser testar o app já com usuários e histórico preenchidos (sem precisar cadastrar do zero nem esperar dias reais passarem), rode:

```bash
python seed_teste.py
```

Isso cria 3 usuários de teste:

- **Teste** — ganho de massa, 21 dias de histórico com streaks quebrados e refeições detalhadas (Café da manhã, Almoço, Lanche, Jantar) em todos os dias, incluindo hoje
- **Testestreak** — manutenção, 10 dias seguidos batendo a meta, com refeições detalhadas em todos os dias, pra ver um streak longo e contínuo
- **Testezerado** — cadastrado, mas sem nenhum registro, pra testar as telas de "nenhum dado"

O script é seguro de rodar mais de uma vez: ele reaproveita os usuários já existentes e substitui as refeições de cada dia em vez de duplicá-las.

## Estrutura do projeto

```
Protein-Tracker/
├── app.py                  # rotas Flask, lógica de cálculo da meta e sessão do usuário
├── database.py              # criação das tabelas e todas as queries no SQLite
├── seed_teste.py             # script opcional para gerar usuários de teste com histórico e refeições completas
├── requirements.txt          # dependências do projeto
├── protein_tracker.db        # banco de dados SQLite (gerado localmente, fora do repositório)
├── templates/
│   ├── cadastro.html         # lista de usuários cadastrados + criação de novo usuário
│   ├── tracker.html          # registro de refeições do dia e progresso da meta
│   ├── historico.html        # streaks, estatísticas, gráfico e tabela de dias
│   └── detalhe_dia.html      # detalhe de um dia específico do histórico, com refeições
└── static/
    └── style.css              # estilos das páginas
```

## Banco de dados

O app usa SQLite (`protein_tracker.db`), com três tabelas:

- **usuarios** — nome, objetivo e meta de proteína (mínima e máxima) de cada pessoa cadastrada
- **registros_diarios** — um resumo por usuário por dia: total consumido, meta do dia, e se ela foi atingida. É essa tabela que alimenta o histórico, o streak e o gráfico
- **itens_consumidos** — cada item de refeição registrado (refeição, alimento, gramas de proteína), por usuário e data. Usada tanto pra montar a lista do dia atual no tracker quanto o detalhamento de refeições de qualquer dia passado no histórico. O total de `registros_diarios` é calculado somando os itens daquele dia

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
- Editar um item de refeição já adicionado (hoje só é possível remover e adicionar de novo)

## Sobre

Projeto pessoal criado para praticar Python após concluir um curso introdutório de programação.
