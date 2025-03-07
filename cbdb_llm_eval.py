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

person_ids = [row[0] for row in row_sample]

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

person_ids += [row[0] for row in row_sample]

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

person_ids += [row[0] for row in row_sample]

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

person_ids += [row[0] for row in row_sample]

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

person_ids += [row[0] for row in row_sample]

person_ids = list(set(person_ids))

for row in row_sample:
    new_rows = [
        {'question': f"{row[1]}(c_personid={row[0]}的籍貫是否為{row[2]}？", 'answer': "是"},
        {'question': f"{row[1]}(c_personid={row[0]}的籍貫是否為{row[3][1:]}？", 'answer': "否"}
    ]
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

# Association

c.execute('''
SELECT 
    BIOG_MAIN.c_personid, 
    BIOG_MAIN.c_name, 
    BIOG_MAIN.c_name_chn, 
    BIOG_MAIN.c_dy, 
    ALTNAME_DATA.c_alt_name, 
    ALTNAME_DATA.c_alt_name_chn, 
    ALTNAME_DATA.c_alt_name_type_code, 
    ASSOC_CODES.c_assoc_code, 
    ASSOC_CODES.c_assoc_desc, 
    ASSOC_CODES.c_assoc_desc_chn, 
    BIOG_MAIN_ASSOC.c_personid AS c_personid_assoc, 
    BIOG_MAIN_ASSOC.c_name AS c_name_assoc, 
    BIOG_MAIN_ASSOC.c_name_chn AS c_name_chn_assoc, 
    BIOG_MAIN_ASSOC.c_dy AS c_dy_assoc, 
    ALTNAME_DATA_ASSOC.c_alt_name_type_code AS c_alt_name_type_code_assoc, 
    ALTNAME_DATA_ASSOC.c_alt_name AS c_alt_name_assoc, 
    ALTNAME_DATA_ASSOC.c_alt_name_chn AS c_alt_name_chn_assoc
FROM ASSOC_CODES
INNER JOIN (
    BIOG_MAIN
    INNER JOIN (
        ASSOC_DATA
        INNER JOIN ALTNAME_DATA 
        ON ASSOC_DATA.c_personid = ALTNAME_DATA.c_personid
    ) 
    ON BIOG_MAIN.c_personid = ASSOC_DATA.c_personid
    INNER JOIN BIOG_MAIN AS BIOG_MAIN_ASSOC 
    ON ASSOC_DATA.c_assoc_id = BIOG_MAIN_ASSOC.c_personid
) 
ON ASSOC_CODES.c_assoc_code = ASSOC_DATA.c_assoc_code
INNER JOIN ALTNAME_DATA AS ALTNAME_DATA_ASSOC 
ON ASSOC_DATA.c_assoc_id = ALTNAME_DATA_ASSOC.c_personid
WHERE 
    ALTNAME_DATA.c_alt_name_type_code = 4 
    AND ALTNAME_DATA_ASSOC.c_alt_name_type_code = 4;

''')
rows = c.fetchall()

row_sample = random.sample(rows, min(len(rows), 10))

person_ids += [row[0] for row in row_sample]

# Association simple question - correct answer

for row in row_sample:
    new_row = {'question': f"{row[2]}(c_personid={row[0]})的`{row[9]}`類型社會網路關係人為{row[12]}(c_personid={row[10]})？", 'answer': '是'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Association reverse question - wrong answer
# Assoc code = 231 Studied with, but reverse the direction to get wrong answer

rows_studied_with = [row for row in rows if row[7] == 231]

row_sample = random.sample(rows_studied_with, min(len(rows_studied_with), 10))

person_ids += [row[0] for row in row_sample]

for row in row_sample:
    new_row = {'question': f"{row[12]}(c_personid={row[10]})是否為{row[2]}(c_personid={row[0]})的學生？", 'answer': '否'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    new_row = {'question': f"{row[12]}(c_personid={row[10]})是否為{row[2]}(c_personid={row[0]})的老師？", 'answer': '是'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Association wrong perons - wrong answer

# In row, get a list of person's dy = 15 save as a seperate list
# Then get a list of person's dy = 20 save as a seperate list
# Then using person's dy = 15 list's person id to filter the row to create correct answer, while random pick the person's dy = 20 to dy =15's answer to create the wrong answer

rows_dy_15 = [row for row in rows if row[3] == 15]
rows_dy_20 = [row for row in rows if row[3] == 20]

row_sample = random.sample(rows_dy_15, min(len(rows_dy_15), 10))

person_ids += [row[0] for row in row_sample]

for row in row_sample:
    row_wrong = random.choice(rows_dy_20)
    new_row = {'question': f"{row[2]}(c_personid={row[0]}, 字{row[5]})的`{row[9]}`類型社會網路關係人為{row_wrong[12]}(c_personid={row_wrong[10]}, 字{row_wrong[16]})？", 'answer': '否'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    new_row = {'question': f"{row[2]}(c_personid={row[0]}, 字{row[5]})的`{row[9]}`類型社會網路關係人為{row[12]}(c_personid={row[10]}, 字{row[16]})？", 'answer': '是'}

# Association wrong name characters - wrong answer
# In row, get a 10 random sample that len(row[12]) > 2, save as a seperate list
rows_long_name = [row for row in rows if len(row[12]) > 2]

row_sample = random.sample(rows_long_name, min(len(rows_long_name), 10))

person_ids += [row[0] for row in row_sample]

for row in row_sample:
    new_row = {'question': f"{row[2]}(c_personid={row[0]})的`{row[9]}`類型社會網路關係人為{row[12][:-1]}？", 'answer': '否'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    new_row = {'question': f"{row[2]}(c_personid={row[0]})的`{row[9]}`類型社會網路關係人為{row[12]}？", 'answer': '是'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# shuffle the dataframe
df = df.sample(frac=1).reset_index(drop=True)
print(df.head(10))

# write to csv and excel
df.to_csv('cbdb_llm_eval.csv', index=False, encoding='utf-8-sig')
df.to_excel('cbdb_llm_eval.xlsx', index=False)

# write person_ids to txt
with open('person_ids.txt', 'w') as f:
    for person_id in person_ids:
        f.write(f"{person_id}\n")

conn.close()
print('Done')
