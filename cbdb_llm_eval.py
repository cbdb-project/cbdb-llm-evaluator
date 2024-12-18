import pandas as pd
import sqlite3
import random

df = pd.DataFrame(columns=['question', 'answer'])

conn = sqlite3.connect('cbdb.db')
c = conn.cursor()

c.execute('SELECT count(*) FROM BIOG_MAIN')
total = c.fetchone()[0]
print('Total number of records:', total)

# Entry method
# Juren
c.execute('''
SELECT ed.c_personid, bm.c_name_chn
FROM ENTRY_DATA ed
JOIN BIOG_MAIN bm ON ed.c_personid = bm.c_personid
WHERE ed.c_personid IN (
    SELECT c_personid
    FROM ENTRY_DATA
    GROUP BY c_personid
    HAVING COUNT(DISTINCT c_entry_code) = 1 AND MAX(c_entry_code) = 39
)
''')
rows = c.fetchall()

row_sample = random.sample(rows, min(len(rows), 10))

for row in row_sample:
    new_row = {'question': f"{row[1]}(c_personid={row[0]})" + '的入仕方式是？', 'answer': '舉人'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Jinshi
c.execute('''
SELECT ed.c_personid, bm.c_name_chn
FROM ENTRY_DATA ed
JOIN BIOG_MAIN bm ON ed.c_personid = bm.c_personid
WHERE ed.c_personid IN (
    SELECT c_personid
    FROM ENTRY_DATA
    GROUP BY c_personid
    HAVING COUNT(DISTINCT c_entry_code) = 1 AND MAX(c_entry_code) = 36
)
''')
rows = c.fetchall()

row_sample = random.sample(rows, min(len(rows), 10))

for row in row_sample:
    new_row = {'question': f"{row[1]}(c_personid={row[0]})" + '的入仕方式是？', 'answer': '進士'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Yin
c.execute('''
SELECT ed.c_personid, bm.c_name_chn
FROM ENTRY_DATA ed
JOIN BIOG_MAIN bm ON ed.c_personid = bm.c_personid
WHERE ed.c_personid IN (
    SELECT c_personid
    FROM ENTRY_DATA
    GROUP BY c_personid
    HAVING COUNT(DISTINCT c_entry_code) = 1 AND MAX(c_entry_code) = 118
)
''')
rows = c.fetchall()

row_sample = random.sample(rows, min(len(rows), 10))

for row in row_sample:
    new_row = {'question': f"{row[1]}(c_personid={row[0]})" + '的入仕方式是？', 'answer': '恩蔭'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Biographical address
# Biographical address simple question
c.execute('''
    SELECT bm.c_personid, bm.c_name_chn, ac.c_name_chn
    FROM BIOG_MAIN bm
    JOIN ADDR_CODES ac ON bm.c_index_addr_id = ac.c_addr_id
    WHERE ac.c_name_chn NOT LIKE '%旗'
        AND LENGTH(ac.c_name_chn) BETWEEN 2 AND 3;
''')
rows = c.fetchall()

row_sample = random.sample(rows, min(len(rows), 10))

for row in row_sample:
    new_row = {'question': f"{row[1]}(c_personid={row[0]})" + '的籍貫是？', 'answer': row[2]}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Biographical address belongs question
# from BIOG_MAIN, get c_index_addr_id, c_personid, c_name_chn, then ADDR_BELONGS_DATA's c_addr_id to get c_belongs_to
# Then using c_belongs_to to join ADDR_CODES's c_addr_id, get c_addr_chn
c.execute('''
    SELECT 
        bm.c_personid, 
        bm.c_name_chn AS biog_name, 
        ac1.c_name_chn AS belongs_to_name, 
        ac2.c_name_chn AS index_addr_name
    FROM BIOG_MAIN bm
    JOIN ADDR_BELONGS_DATA abd ON bm.c_index_addr_id = abd.c_addr_id
    JOIN ADDR_CODES ac1 ON abd.c_belongs_to = ac1.c_addr_id
    JOIN ADDR_CODES ac2 ON bm.c_index_addr_id = ac2.c_addr_id
    WHERE ac1.c_name_chn NOT LIKE '%旗' 
        AND ac1.c_name_chn LIKE '%府'
        AND LENGTH(ac2.c_name_chn) > 2;
''')
rows = c.fetchall()

row_sample = random.sample(rows, min(len(rows), 10))

for row in row_sample:
    new_row = {'question': f"{row[1]}(c_personid={row[0]}的籍貫是否為{row[2]}？", 'answer': "是"}
    new_row = {'question': f"{row[1]}(c_personid={row[0]}的籍貫是否為{row[3][1:]}？", 'answer': "否"}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

df = df.sample(frac=1).reset_index(drop=True)
print(df.head(10))

# write to csv and excel
df.to_csv('cbdb_llm_eval.csv', index=False, encoding='utf-8-sig')
df.to_excel('cbdb_llm_eval.xlsx', index=False)