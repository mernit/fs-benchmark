#!/usr/bin/env python3
"""
Filesystem vs Database latency benchmark

Measures p50/p95/p99 for reading ~100kb of text from:
  - Filesystem (single file)
  - Filesystem (50 concurrent files, same total size)
  - PostgreSQL
  - Redis
"""

import os
import time
import statistics
import tempfile
import random
from concurrent.futures import ThreadPoolExecutor

import psycopg2
import redis as redis_lib


# --- Data generation ---

def generate_context(size_kb=100):
    """Generate realistic agent context text (markdown-style)."""
    lines = []
    headers = ["## Task", "## Context", "## Memory", "## Instructions", "## Prior Steps"]
    words = [
        "agent", "context", "file", "workspace", "user", "task", "memory",
        "output", "result", "query", "document", "step", "action", "tool",
        "retrieve", "write", "read", "process", "analyze", "summarize"
    ]
    target = size_kb * 1024
    while sum(len(l) for l in lines) < target:
        lines.append(random.choice(headers))
        for _ in range(random.randint(3, 8)):
            sentence = " ".join(random.choices(words, k=random.randint(8, 18))) + "."
            lines.append(sentence)
        lines.append("")
    return "\n".join(lines)[:target]


# --- Benchmarking ---

def percentile(data, p):
    s = sorted(data)
    idx = max(0, min(int(len(s) * p / 100), len(s) - 1))
    return s[idx]


def run(fn, iterations=1000, warmup=50):
    for _ in range(warmup):
        fn()
    times = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        fn()
        times.append((time.perf_counter() - t0) * 1000)
    return times


def print_results(name, times):
    print(f"  {'p50':>8}  {'p95':>8}  {'p99':>8}  {'mean':>8}  {'max':>8}")
    print(f"  {percentile(times,50):>7.3f}ms  {percentile(times,95):>7.3f}ms  "
          f"{percentile(times,99):>7.3f}ms  {statistics.mean(times):>7.3f}ms  "
          f"{max(times):>7.3f}ms")


def main():
    ITERATIONS = 1000
    DATA_KB = 100

    content = generate_context(DATA_KB)
    actual_kb = len(content) / 1024
    print(f"\nBenchmark: {actual_kb:.1f}kb of text, {ITERATIONS} iterations each\n")

    # --- Filesystem: single file ---
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    tmp.write(content)
    tmp.close()

    def read_single_file():
        with open(tmp.name) as f:
            return f.read()

    print(f"[ Filesystem — single file ({actual_kb:.0f}kb) ]")
    print_results("fs_single", run(read_single_file, ITERATIONS))

    # --- Filesystem: 50 concurrent files ---
    chunk_size = len(content) // 50
    chunk_files = []
    for i in range(50):
        t = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        t.write(content[i * chunk_size:(i + 1) * chunk_size])
        t.close()
        chunk_files.append(t.name)

    def read_file(path):
        with open(path) as f:
            return f.read()

    def read_50_files():
        with ThreadPoolExecutor(max_workers=50) as ex:
            list(ex.map(read_file, chunk_files))

    print(f"\n[ Filesystem — 50 concurrent files (same total size) ]")
    print_results("fs_concurrent", run(read_50_files, ITERATIONS))

    # --- PostgreSQL ---
    conn = psycopg2.connect(
        host="localhost", port=5432,
        dbname="benchmark", user="benchmark", password="benchmark"
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS documents (id INT PRIMARY KEY, content TEXT)")
    cur.execute(
        "INSERT INTO documents VALUES (1, %s) ON CONFLICT (id) DO UPDATE SET content = EXCLUDED.content",
        (content,)
    )
    conn.commit()

    def read_postgres():
        cur.execute("SELECT content FROM documents WHERE id = 1")
        return cur.fetchone()[0]

    print(f"\n[ PostgreSQL — SELECT content WHERE id = 1 ]")
    print_results("postgres", run(read_postgres, ITERATIONS))

    # --- Redis ---
    r = redis_lib.Redis(host="localhost", port=6379)
    r.set("context", content)

    def read_redis():
        return r.get("context").decode("utf-8")

    print(f"\n[ Redis — GET context ]")
    print_results("redis", run(read_redis, ITERATIONS))

    print()

    # Cleanup
    os.unlink(tmp.name)
    for path in chunk_files:
        os.unlink(path)
    cur.execute("DROP TABLE IF EXISTS documents")
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
