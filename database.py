import sqlite3

conn = sqlite3.connect('gestao_academia.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_aluno INTEGER,
        valor_pago REAL,
        data_pagamento TEXT,
        mes_referencia TEXT,
        FOREIGN KEY (id_aluno) REFERENCES alunos (id)
    )
''')
conn.commit()
conn.close()