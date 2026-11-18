"""Week 6 - reading FASTA and CSV safely."""
import csv
from collections.abc import Iterator
from pathlib import Path


class FastaFormatError(ValueError):
    """Raised when a FASTA file does not follow the format."""


def _finish(record_id: str, chunks: list[str], path) -> tuple[str, str]:
    """Join the chunks; a record must have a sequence."""
    sequence = "".join(chunks).upper()
    if not sequence:
        raise FastaFormatError(
            f"{path}: record {record_id!r} has no sequence"
        )
    return record_id, sequence


def read_fasta(path) -> Iterator[tuple[str, str]]:
    """Yield (record_id, sequence) for every record in a FASTA file.

    The id is the first word of the header. Wrapped lines are joined and the
    sequence is upper-cased. Records are produced one at a time, so large
    files do not have to fit in memory.

    Raises:
        FileNotFoundError: if the file does not exist.
        FastaFormatError: for data before the first header, an empty header
            or a record without sequence.
    """
    record_id: str | None = None
    chunks: list[str] = []
    with open(path, encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if record_id is not None:
                    yield _finish(record_id, chunks, path)
                header = line[1:].strip()
                if not header:
                    raise FastaFormatError(f"{path}:{lineno}: empty header")
                record_id, chunks = header.split()[0], []
            else:
                if record_id is None:
                    raise FastaFormatError(f"{path}:{lineno}: sequence data before the first header")
                chunks.append(line)
    if record_id is not None:
        yield _finish(record_id, chunks, path)
 

def read_csv_records(path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dictionaries (all values are strings)."""
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict], path, fieldnames: list[str]) -> None:
    """Write rows to a CSV file, creating the parent folder if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
