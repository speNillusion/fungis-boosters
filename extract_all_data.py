#!/usr/bin/env python3
"""
Script para extrair todos os dados da base de dados SQLite
Extrai: plásticos, fungos/microrganismos e todos os registros
"""

import sqlite3
import json
import csv
import pandas as pd
from collections import Counter

def extract_all_data():
    """Extrai todos os dados da base de dados"""
    try:
        conn = sqlite3.connect('degradation_data.db')
        cursor = conn.cursor()
        
        print("🔍 EXTRAINDO DADOS DA BASE DE DADOS...")
        print("=" * 50)
        
        # 1. EXTRAIR TODOS OS TIPOS DE PLÁSTICO
        print("\n📦 TIPOS DE PLÁSTICO:")
        cursor.execute("SELECT DISTINCT Plastic FROM degraders WHERE Plastic IS NOT NULL AND Plastic != ''")
        plastics = [row[0] for row in cursor.fetchall()]
        plastics_sorted = sorted(plastics)
        
        print(f"Total de tipos de plástico únicos: {len(plastics_sorted)}")
        for i, plastic in enumerate(plastics_sorted, 1):
            print(f"  {i:2d}. {plastic}")
        
        # Contar frequência de cada plástico
        cursor.execute("SELECT Plastic, COUNT(*) as count FROM degraders WHERE Plastic IS NOT NULL AND Plastic != '' GROUP BY Plastic ORDER BY count DESC")
        plastic_counts = cursor.fetchall()
        
        print(f"\n📊 FREQUÊNCIA DOS PLÁSTICOS (Top 10):")
        for plastic, count in plastic_counts[:10]:
            print(f"  {plastic}: {count} registros")
        
        # 2. EXTRAIR TODOS OS FUNGOS/MICRORGANISMOS
        print(f"\n🦠 MICRORGANISMOS:")
        cursor.execute("SELECT DISTINCT Microorganism FROM degraders WHERE Microorganism IS NOT NULL AND Microorganism != ''")
        microorganisms = [row[0] for row in cursor.fetchall()]
        microorganisms_sorted = sorted(microorganisms)
        
        print(f"Total de microrganismos únicos: {len(microorganisms_sorted)}")
        for i, microorganism in enumerate(microorganisms_sorted[:20], 1):  # Mostrar apenas os primeiros 20
            print(f"  {i:2d}. {microorganism}")
        
        if len(microorganisms_sorted) > 20:
            print(f"  ... e mais {len(microorganisms_sorted) - 20} microrganismos")
        
        # Contar frequência de cada microrganismo
        cursor.execute("SELECT Microorganism, COUNT(*) as count FROM degraders WHERE Microorganism IS NOT NULL AND Microorganism != '' GROUP BY Microorganism ORDER BY count DESC")
        microorganism_counts = cursor.fetchall()
        
        print(f"\n📊 FREQUÊNCIA DOS MICRORGANISMOS (Top 10):")
        for microorganism, count in microorganism_counts[:10]:
            print(f"  {microorganism}: {count} registros")
        
        # 3. EXTRAIR TODAS AS LINHAS/REGISTROS
        print(f"\n📋 TODOS OS REGISTROS:")
        cursor.execute("SELECT * FROM degraders")
        all_records = cursor.fetchall()
        
        # Obter nomes das colunas
        cursor.execute("PRAGMA table_info(degraders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"Total de registros: {len(all_records)}")
        print(f"Total de colunas: {len(columns)}")
        
        # 4. SALVAR DADOS EM ARQUIVOS
        print(f"\n💾 SALVANDO DADOS EM ARQUIVOS...")
        
        # Salvar plásticos em JSON
        with open('plasticos_extraidos.json', 'w', encoding='utf-8') as f:
            json.dump({
                'total': len(plastics_sorted),
                'tipos': plastics_sorted,
                'frequencia': dict(plastic_counts)
            }, f, ensure_ascii=False, indent=2)
        print("  ✅ plasticos_extraidos.json")
        
        # Salvar microrganismos em JSON
        with open('microrganismos_extraidos.json', 'w', encoding='utf-8') as f:
            json.dump({
                'total': len(microorganisms_sorted),
                'tipos': microorganisms_sorted,
                'frequencia': dict(microorganism_counts)
            }, f, ensure_ascii=False, indent=2)
        print("  ✅ microrganismos_extraidos.json")
        
        # Salvar todos os registros em CSV
        with open('todos_registros.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)  # Cabeçalho
            writer.writerows(all_records)
        print("  ✅ todos_registros.csv")
        
        # Salvar todos os registros em JSON
        records_dict = []
        for record in all_records:
            record_dict = dict(zip(columns, record))
            records_dict.append(record_dict)
        
        with open('todos_registros.json', 'w', encoding='utf-8') as f:
            json.dump(records_dict, f, ensure_ascii=False, indent=2)
        print("  ✅ todos_registros.json")
        
        # 5. ESTATÍSTICAS GERAIS
        print(f"\n📈 ESTATÍSTICAS GERAIS:")
        
        # Enzimas
        cursor.execute("SELECT COUNT(DISTINCT Enzyme) FROM degraders WHERE Enzyme IS NOT NULL AND Enzyme != ''")
        unique_enzymes = cursor.fetchone()[0]
        print(f"  Enzimas únicas: {unique_enzymes}")
        
        # Anos
        cursor.execute("SELECT MIN(Year), MAX(Year) FROM degraders WHERE Year IS NOT NULL AND Year != ''")
        year_range = cursor.fetchone()
        print(f"  Período dos estudos: {year_range[0]} - {year_range[1]}")
        
        # Evidências
        cursor.execute("SELECT DISTINCT Evidence FROM degraders WHERE Evidence IS NOT NULL AND Evidence != ''")
        evidences = [row[0] for row in cursor.fetchall()]
        print(f"  Tipos de evidência: {len(evidences)}")
        
        # Ambientes de isolamento
        cursor.execute("SELECT COUNT(DISTINCT Isolation_environment) FROM degraders WHERE Isolation_environment IS NOT NULL AND Isolation_environment != ''")
        environments = cursor.fetchone()[0]
        print(f"  Ambientes de isolamento: {environments}")
        
        conn.close()
        
        print(f"\n✅ EXTRAÇÃO COMPLETA!")
        print(f"Arquivos gerados:")
        print(f"  - plasticos_extraidos.json")
        print(f"  - microrganismos_extraidos.json") 
        print(f"  - todos_registros.csv")
        print(f"  - todos_registros.json")
        
        return {
            'plasticos': plastics_sorted,
            'microrganismos': microorganisms_sorted,
            'total_registros': len(all_records),
            'colunas': columns
        }
        
    except Exception as e:
        print(f"❌ Erro ao extrair dados: {e}")
        return None

if __name__ == "__main__":
    result = extract_all_data()
    if result:
        print(f"\n🎉 Dados extraídos com sucesso!")
        print(f"   {len(result['plasticos'])} tipos de plástico")
        print(f"   {len(result['microrganismos'])} microrganismos")
        print(f"   {result['total_registros']} registros totais")