# Filesystem vs Database Latency Benchmark

How fast is reading text from a file compared to Postgres or Redis?

Benchmarks 1,000 reads of ~100kb of text from:
- Filesystem (single file)
- Filesystem (50 concurrent files, same total size)
- PostgreSQL (`SELECT content WHERE id = 1`)
- Redis (`GET`)

## Results

Tested on Apple M-series, local SSD, 1,000 iterations each.

| Backend | p50 | p95 | p99 | mean |
|---|---|---|---|---|
| Filesystem (single file) | 0.031ms | 0.048ms | 0.162ms | 0.038ms |
| PostgreSQL | 0.278ms | 0.712ms | 1.325ms | 0.341ms |
| Redis | 0.356ms | 1.466ms | 3.600ms | 0.536ms |
| Filesystem (50 concurrent files) | 3.533ms | 8.683ms | 17.899ms | 4.490ms |

**File reads are ~9x faster than Postgres and ~11x faster than Redis at p50.**

For context: a Claude Sonnet call takes 2,000–8,000ms. File I/O is not your bottleneck.

## Run it yourself

Requires Python 3, Postgres, and Redis.

**With Docker:**
```bash
docker compose up -d
pip install -r requirements.txt
python benchmark.py
```

**With Homebrew:**
```bash
brew install postgresql redis
brew services start postgresql redis
createdb benchmark
pip install -r requirements.txt
python benchmark.py
```
