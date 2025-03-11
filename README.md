# CBDB LLM Evaluator

A tool for evaluating LLM responses against the China Biographical Database (CBDB).

## Setup

1. Download the CBDB SQLite database from [Hugging Face](https://huggingface.co/datasets/cbdb/cbdb-sqlite/blob/main/latest.7z)
2. Extract the downloaded `.7z` file
3. Rename the extracted database file to `cbdb.db`
4. Place `cbdb.db` in the root directory of this project

## Files

- `cbdb_llm_eval.py` - Main evaluation script
- `person_ids.txt` - List of person IDs for evaluation. These IDs can be used with the [narrative-cbdb project](https://github.com/cbdb-project/narrative-cbdb) to retrieve narrative biographical texts for the listed persons for further RAG test.
- `cbdb_llm_eval.csv` - CSV output of evaluation results
- `cbdb_llm_eval.xlsx` - Excel format of evaluation results

## Note

This project requires the CBDB SQLite database file to be named exactly as `cbdb.db` and placed in the project root directory. Without this database file, the evaluation scripts will not function properly.
