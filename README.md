Um dashboard interativo desenvolvido em **Python + Streamlit**, que analisa os **atrasos de voos no Brasil** entre 2022 e 2024.  
O projeto combina **análise exploratória de dados (EDA)** com **visualizações modernas e interativas (Plotly)**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)  
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)  
![Plotly](https://img.shields.io/badge/Plotly-5.x-green?logo=plotly)

---

## Funcionalidades

-  **Visão Geral**:
  - Total de voos realizados.
  - Total de atrasos (>15 minutos).
  - Percentual de atrasos.

-  **Top 10 Aeroportos com Mais Atrasos**:
  - Ranking atualizado com gráfico interativo.

-  **Comparativo de Companhias Aéreas**:
  - Evolução anual dos atrasos por companhia (se mais de um ano for selecionado).

-  **Distribuição de Atrasos**:
  - Por dia da semana.
  - Por período do dia (Madrugada, Manhã, Tarde, Noite).

- **Tendências (2022–2024)**:
  - Aeroportos com **aumento consistente** nos atrasos.
  - Aeroportos com **redução consistente** nos atrasos.
  - Gráfico de linha mostrando a evolução anual.

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)  
- [Streamlit](https://streamlit.io/)  
- [Pandas](https://pandas.pydata.org/)  
- [Plotly Express](https://plotly.com/python/plotly-express/)  

---

## 📂 Estrutura do Projeto

```
📦 dashboard-voos
 ┣ 📂 dataset
 ┃ ┣ flights.csv
 ┃ ┣ flights_2023.csv
 ┃ ┣ flights_2024.csv
 ┃ ┣ airport-codes.csv
 ┃ ┗ airlines-codes.csv
 ┣ 📜 app.py
 ┣ 📜 README.md
 ┗ 📜 requirements.txt
```

- `app.py` → código principal do dashboard.  
- `dataset/` → contém os arquivos CSV de voos, aeroportos e companhias.  
- `requirements.txt` → dependências do projeto.  
- `README.md` → documentação.  

---

## ▶️ Como Executar

1. Clone este repositório:

```bash
git clone https://github.com/Alchini/Dashboard-Voos-Brasil.git
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

3. Execute o Streamlit:

```bash
streamlit run main.py
```

4. Abra no navegador:  
👉 [http://localhost:8501](http://localhost:8501)

---

## Exemplo de Uso

- Selecione os anos disponíveis no **menu lateral**.  
- Veja o **resumo geral** em cards.  
- Explore as abas: **Aeroportos**, **Companhias**, **Dias/Períodos**.  
- Analise as **tendências de aumento/redução** nos atrasos.  

---
