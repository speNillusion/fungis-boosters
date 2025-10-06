#!/usr/bin/env python3
"""
Script para verificar a estrutura da base de dados SQLite
"""

import sqlite3
import json

def check_database_structure():
    """Verifica a estrutura da base de dados"""
    try:
        conn = sqlite3.connect('degradation_data.db')
        cursor = conn.cursor()
        
        # Obter lista de tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("=== ESTRUTURA DA BASE DE DADOS ===")
        print(f"Tabelas encontradas: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Tabela: {table_name}")
            
            # Obter estrutura da tabela
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("  Colunas:")
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                is_pk = " (PK)" if col[5] else ""
                not_null = " NOT NULL" if col[3] else ""
                print(f"    - {col_name}: {col_type}{not_null}{is_pk}")
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  Total de registros: {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erro ao verificar base de dados: {e}")
        return False

if __name__ == "__main__":
    check_database_structure()