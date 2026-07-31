[README.md](https://github.com/user-attachments/files/30577191/README.md)
# Protein Tracker

Calculadora e rastreador de consumo de proteína diária, com interface web feita em Flask.

O projeto calcula a meta diária de proteína com base no peso e no objetivo da pessoa (manutenção, ganho de massa ou perda de gordura), e permite acompanhar o quanto já foi consumido ao longo do dia.

Começou como um script de terminal em Python e evoluiu para uma aplicação web.

## Como funciona

1. Você informa nome, peso e objetivo
2. O app calcula sua meta diária de proteína
3. Ao longo do dia, você vai adicionando o quanto consumiu em cada refeição
4. Um anel de progresso mostra visualmente o quanto falta pra bater a meta

## Como rodar localmente

Pré-requisitos: Python 3 instalado.

```bash
# clone o repositório
git clone https://github.com/Arthur-Isidoro/Protein-Tracker.git
cd Protein-Tracker

# instale as dependências
pip install -r requirements.txt

# rode o app
python app.py
```

Depois é só abrir `http://127.0.0.1:5000` no navegador.

## Estrutura do projeto

```
Protein-Tracker/
├── app.py              # rotas Flask e lógica de cálculo da meta
├── requirements.txt    # dependências do projeto
├── templates/
│   ├── cadastro.html   # página de cadastro (nome, peso, objetivo)
│   └── tracker.html    # página de acompanhamento do consumo
└── static/
    └── style.css        # estilos das páginas
```

## Como a meta é calculada

| Objetivo | Proteína por kg de peso corporal |
|---|---|
| Manutenção | 1.6 g/kg |
| Ganho de massa | 1.8 g/kg a 2.2 g/kg |
| Perda de gordura | 2.0 g/kg a 2.4 g/kg |

## Possíveis próximos passos

- Salvar o histórico de consumo num banco de dados (hoje ele se perde ao fechar o navegador)
- Separar a lógica de cálculo em um módulo próprio
- Adicionar autenticação para múltiplos usuários
- Histórico de dias anteriores

## Sobre

Projeto pessoal criado para praticar Python após concluir um curso introdutório de programação.
