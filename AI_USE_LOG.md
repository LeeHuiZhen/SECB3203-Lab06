# AI USE LOG

<!-- SECB3203 prompt log. Policy: PROPOSED - for approval by the SECB3203 course team before circulation to students. Fill in, then run: python tools/check_ai_log.py AI_USE_LOG.md --assessment <key> -->

- Course: SECB3203
- Assessment: Lab 6
- Student name: Lee Hui Zhen
- Matric no: A24CS0259
- Group ID: n/a
- AI level: 1
- Tools cited: Google (2026). Gemini. Retrieved 18 November 2026 from https://gemini.google.com

## Declaration (tick exactly one)

- [ ] NIL RETURN: I did not use any generative AI tool for this assessment.
- [x] I used AI. Every interaction that influenced my work is logged below. The log is true and complete.

## Entry 1

- Date: 18 November 2026, 5:15 PM
- Tool: Google (2026). Gemini. Retrieved 18 November 2026 from https://gemini.google.com
- Purpose: explain
- Prompt: "In read_fasta, why do we still need an if record_id is not None: block after the for loop ends, and why does an empty file return nothing instead of raising FastaFormatError?"
- Output: Explained that yielding inside the loop only outputs a record when the next '>' header arrives, so the final record must be yielded after the loop finishes. Also clarified that an empty file leaves record_id as None so the generator finishes without yielding or raising an error.
- Verified by: Tested read_fasta on data/geneA.fasta, data/amplicons.fasta, and an empty temporary file using pytest.
- My change: Added the final `if record_id is not None: yield _finish(record_id, chunks, path)` check after the loop in `read_fasta`.
- Used in: src/bio_io.py (read_fasta)

## Entry 2

- Date: 18 November 2026, 5:28 PM
- Tool: Google (2026). Gemini. Retrieved 18 November 2026 from https://gemini.google.com
- Purpose: debug
- Prompt: "Can you check my bio_io.py? I got a SyntaxError in read_csv_records when returning list(csv.DictReader(handle)"
- Output: Pointed out the missing closing parenthesis in `return list(csv.DictReader(handle))` and confirmed that `newline=""` and `mkdir(parents=True, exist_ok=True)` handle Windows line endings and missing parent folders properly.
- Verified by: Fixed the parenthesis and ran `python -m pytest` to confirm the CSV tests passed.
- My change: Added the missing closing parenthesis on the return line in `read_csv_records`.
- Used in: src/bio_io.py (read_csv_records)

## Entry 3

- Date: 18 November 2026, 5:45 PM
- Tool: Google (2026). Gemini. Retrieved 18 November 2026 from https://gemini.google.com
- Purpose: hint
- Prompt: "In process_directory, why does the try/except need to be inside the for loop, and how do I stop logging.FileHandler from writing into the log of another run?"
- Output: Explained that putting try/except inside the file loop isolates errors to one file so the rest of the batch continues, and advised removing and closing the FileHandler inside a finally block so repeated runs do not duplicate handlers or append to previous logs.
- Verified by: Ran `python src/batch.py data/river --out results/cli` and checked `results/cli/processing_log.csv` and `results/cli/batch.log`.
- My change: Placed the per-file try/except inside the sorted file loop and added `LOG.removeHandler(handler)` and `handler.close()` inside `finally`.
- Used in: src/batch.py (process_directory)

## Entry 4

- Date: 18 November 2026, 6:05 PM
- Tool: Google (2026). Gemini. Retrieved 18 November 2026 from https://gemini.google.com
- Purpose: tests-plan
- Prompt: "Looking at test_visible.py, what extra cases should I add to tests/test_lab06_own.py using tmp_path so I cover Task T5?"
- Output: Suggested testing an empty FASTA file and a missing file, a FASTA record without sequence naming the file in `FastaFormatError`, a CSV round trip with commas and quotes, `process_directory` on an empty folder with exit code 0, and FASTQ quality lines starting with '@' or '+'.
- Verified by: Ran `python -m pytest` and `ruff check src` and verified all 10 tests pass with no lint errors.
- My change: Wrote five test functions in `tests/test_lab06_own.py` covering those cases.
- Used in: tests/test_lab06_own.py
