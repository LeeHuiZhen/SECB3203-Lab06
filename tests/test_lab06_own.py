import pytest

from batch import FastqFormatError, main, mean_phred, process_directory, read_fastq
from bio_io import FastaFormatError, read_csv_records, read_fasta, write_csv


def test_read_fasta_empty_and_missing(tmp_path):
    empty = tmp_path / "empty.fasta"
    empty.write_text("\n  \r\n", encoding="utf-8")
    assert list(read_fasta(empty)) == []

    with pytest.raises(FileNotFoundError):
        list(read_fasta(tmp_path / "missing.fasta"))


def test_read_fasta_no_sequence_names_file(tmp_path):
    bad = tmp_path / "no_seq.fasta"
    bad.write_text(">seq1\n>seq2\nACGT\n", encoding="utf-8")

    with pytest.raises(FastaFormatError, match="no_seq.fasta"):
        list(read_fasta(bad))


def test_write_and_read_csv_round_trip(tmp_path):
    out_csv = tmp_path / "sub" / "records.csv"
    rows = [{"sample": "S01", "note": 'comma, and "quotes"'}]
    write_csv(rows, out_csv, ["sample", "note"])

    assert read_csv_records(out_csv) == rows


def test_process_directory_empty_and_exit_code_zero(tmp_path):
    empty_dir = tmp_path / "empty_in"
    empty_dir.mkdir()
    summary = process_directory(empty_dir, tmp_path / "log.csv", tmp_path / "batch.log")
    assert summary == {"processed": 0, "rejected": 0, "records": 0}
    assert read_csv_records(tmp_path / "log.csv") == []

    good_dir = tmp_path / "good_in"
    good_dir.mkdir()
    (good_dir / "ok.fasta").write_text(">r1\nACGT\n", encoding="utf-8")
    assert main([str(good_dir), "--out", str(tmp_path / "out")]) == 0


def test_fastq_tricky_quality_and_errors(tmp_path):
    fq = tmp_path / "tricky.fastq"
    fq.write_text("@r1\nACGT\n+\n@+II\n", encoding="utf-8")
    assert list(read_fastq(fq)) == [("r1", "ACGT", "@+II")]

    bad_fq = tmp_path / "bad.fastq"
    bad_fq.write_text("@r1\nACGT\n+\nII\n", encoding="utf-8")
    with pytest.raises(FastqFormatError):
        list(read_fastq(bad_fq))

    with pytest.raises(ValueError):
        mean_phred("")