#!/usr/bin/env python3
"""
Generate DiskANN-compatible .fvecs files from a (very) large text corpus
using a SentenceTransformers static embedding model.

The script streams the dataset, encodes in batches on CPU/GPU, and writes the
embeddings directly to binary .fvecs files – no full matrix has to fit in RAM.

Example – encode the PAQ dataset (HuggingFace) into 1024‑D vectors:
    python embed-sentences-to-fvecs.py \
        --dataset sentence-transformers/paq \
        --output_dir ../build/data \
        --query_count 10000 \
        --batch_size 128 \
        --max_rows 1000000 \



Example – encode a local text file (one text per line):
    python embed-sentences-to-fvecs.py \
        --dataset my_corpus.txt \
        --output_dir ../build/data \
        --batch_size 128 \

The script always produces two files in the output directory:
    query.fvecs  – the first N vectors (‑‑query_count)
    base.fvecs  – the following N vectors (‑‑max_rows)

Both are in the standard fvecs layout:
[int32 dimension] + [dimension × float32]

Author: ChatGPT-o3, 15/5/2025

NOTE: A threading bug has been experienced however not data-critical
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
from typing import Iterable, List

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Small patch for the multiprocess/threading bug that occurs on Python 3.10
# ---------------------------------------------------------------------------
import threading
threading._Condition = threading.Condition  # type: ignore[attr-defined]

# ---------------------------------------------------------------------------
# Helper: stream texts from either HF Hub dataset or a local text file
# ---------------------------------------------------------------------------

def stream_texts(ds_arg: str, split: str) -> Iterable[str]:
    """Yield texts one by one from a local file or a HuggingFace dataset."""
    if os.path.isfile(ds_arg):
        with open(ds_arg, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield line
    else:
        try:
            from datasets import load_dataset  # local import keeps startup fast
        except ImportError as e:
            print("datasets not installed – pip install datasets", file=sys.stderr)
            raise e

        ds = load_dataset(ds_arg, split=split, streaming=True)
        # Detect the text field lazily
        example = next(iter(ds))
        text_field = None
        for candidate in ("text", "question", "query", "sentence", "content"):
            if candidate in example:
                text_field = candidate
                break
        if text_field is None:
            raise ValueError(f"Could not detect text field in dataset. Keys: {list(example.keys())}")

        # Rewind iterator after the peek
        ds = load_dataset(ds_arg, split=split, streaming=True)
        for ex in ds:
            yield ex[text_field]

# ---------------------------------------------------------------------------
# Helper: write one vector in fvecs format
# ---------------------------------------------------------------------------

def write_fvec(file_obj, vec: np.ndarray):
    vec = vec.astype(np.float32, copy=False)
    file_obj.write(struct.pack("<i", vec.shape[0]))  # little endian int32 dim
    file_obj.write(vec.tobytes(order="C"))

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: List[str] | None = None):
    parser = argparse.ArgumentParser(description="Encode text corpus to DiskANN .fvecs using SentenceTransformers.")
    parser.add_argument("--dataset", required=True, help="HF dataset name (e.g. sentence-transformers/paq) or path to local .txt file")
    parser.add_argument("--split", default="train", help="Dataset split to use when --dataset is a HF dataset")
    parser.add_argument("--model", default="tomaarsen/static-retrieval-mrl-en-v1", help="SentenceTransformer model ID")
    parser.add_argument("--dim", type=int, default=1024, help="Output embedding dimensionality (Matryoshka models can be truncated)")
    parser.add_argument("--batch_size", type=int, default=64, help="Texts per encode batch")
    parser.add_argument("--output_dir", required=True, help="Directory to place base.fvecs and query.fvecs")
    parser.add_argument("--query_count", type=int, default=10_000, help="How many vectors to also write to query.fvecs from the start of the stream")
    parser.add_argument("--max_rows", type=int, default=None, help="Optional limit on how many rows to encode (for quick tests)")

    args = parser.parse_args(argv)

    os.makedirs(os.path.join(args.output_dir, args.dataset), exist_ok=True)

    base_path  = os.path.join(args.output_dir, args.dataset, "base.fvecs")
    query_path = os.path.join(args.output_dir, args.dataset, "query.fvecs")

    print("global path is", os.path.abspath(base_path))
    # Load model (GPU if available)
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer(args.model, device=device)

    # Stream dataset
    text_iter = stream_texts(args.dataset, args.split)

    # Open output files
    with open(base_path, "wb") as base_f, open(query_path, "wb") as query_f:
        batch: List[str] = []
        total = 0
        query_written = 0
        pbar = tqdm(unit="rows")
        for text in text_iter:
            batch.append(text)
            if len(batch) == args.batch_size:
                emb = model.encode(batch, batch_size=args.batch_size,
                                   convert_to_numpy=True,
                                   normalize_embeddings=True)  # cosine‑ready
                # optional Matryoshka truncation
                emb = emb[:, :args.dim]
                for vec in emb:
                    if query_written < args.query_count:
                        write_fvec(query_f, vec)
                        query_written += 1
                    else:
                        write_fvec(base_f, vec)
                total += emb.shape[0]
                pbar.update(emb.shape[0])
                batch.clear()
                if args.max_rows and args.query_count and total >= args.max_rows + args.query_count:
                    # stop if we have written all requested rows
                    break
        pbar.close()

    print(f"Finished. Wrote {total - query_written} vectors to {base_path}")
    print(f"First {query_written} vectors also stored in {query_path}")

if __name__ == "__main__":
    main()
