# SECB3203 Lab 6 - Files and exceptions: bio_io.py and batch.py

Student: Lee Hui Zhen, A24CS0259

## Setup
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Run
    python -m pytest                 # all tests
    ruff check src                   # style check
    python src/batch.py data/river --out results/cli      # the command-line tool

## What is in this repository
- `src/bio_io.py` : FastaFormatError, read_fasta, read_csv_records, write_csv
- `src/batch.py` : process_directory, read_fastq, mean_phred, main (command-line tool)
- `tests/` : visible tests and my own tests (test_lab06_own.py)
- `data/` : raw synthetic data, read-only (amplicons.fasta, river/, qc_records.csv, reads.fastq)
- `results/` : files the tool writes (not committed)
- `AI_USE_LOG.md` : my AI prompt log (or nil return)

## Exit codes of batch.py
- **0**: Every FASTA file in the input folder was processed successfully with zero rejected files.
- **1**: The batch run completed, but at least one FASTA file was rejected (for example, an empty, malformed, or non-UTF-8 file).
- **2**: The input path given on the command line does not exist or is not a folder, so no files were processed and an error message was printed to stderr.
