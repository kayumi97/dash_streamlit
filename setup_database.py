'''
Organização Recomendada
Arquivo para Inicialização do Banco: Crie um arquivo chamado, por exemplo, setup_database.py. Esse arquivo será responsável por:

Criar a tabela.
Inserir os dados do arquivo CSV no banco.
Arquivo para o Dashboard: O app.py será usado apenas para exibir os dados e interagir com o banco.
'''

import psycopg2
import pandas as pd

# Conexão com o banco
conn = psycopg2.connect(
    host="database-hap.cb6ei4cq2ox1.us-east-2.rds.amazonaws.com",
    database="postgres",
    user="postgres",
    password="batataFRITA",
    port=5432
)
cursor = conn.cursor()

# Criação da tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS world_happiness (
    country VARCHAR(255),
    year INT,
    happiness_score FLOAT
);
""")
conn.commit()

# Carregar os dados do CSV
df = pd.read_csv('2015.csv')

# Inserir os dados no banco, adicionando o ano manualmente
for index, row in df.iterrows():
    cursor.execute("""
    INSERT INTO world_happiness (country, year, happiness_score)
    VALUES (%s, %s, %s)
    """, (row['Country'], 2015, row['Happiness Score']))  # Ano fixo como 2015
conn.commit()


print("Tabela criada e dados inseridos com sucesso!")

# Fechar a conexão
cursor.close()
conn.close()
