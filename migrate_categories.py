import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("C:/Dashboard_Frota_Dev/data/app.db")

def migrate():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Verifica se a constraint existe
    cursor.execute("PRAGMA foreign_keys=off;")

    # Cria nova tabela sem CHECK na categoria
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos_new (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            placa VARCHAR(10) NOT NULL,
            modelo VARCHAR(80),
            marca VARCHAR(80),
            ano INTEGER,
            categoria VARCHAR(20),
            status VARCHAR(20),
            observacoes TEXT,
            created_at DATETIME,
            CONSTRAINT uq_veiculos_placa UNIQUE (placa)
        );
    """)

    # Copia dados
    cursor.execute("""
        INSERT INTO veiculos_new
        SELECT id, placa, modelo, marca, ano, categoria, status, observacoes, created_at
        FROM veiculos;
    """)

    # Dropa tabela antiga
    cursor.execute("DROP TABLE veiculos;")

    # Renomeia nova
    cursor.execute("ALTER TABLE veiculos_new RENAME TO veiculos;")

    # Recria index
    cursor.execute("CREATE INDEX IF NOT EXISTS ix_veiculos_placa ON veiculos (placa);")

    cursor.execute("PRAGMA foreign_keys=on;")
    conn.commit()
    conn.close()
    print("Migration concluida. CHECK constraint removido da coluna categoria.")


if __name__ == "__main__":
    migrate()
