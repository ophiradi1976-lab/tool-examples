# hyperfine — Command Benchmarking

A statistical benchmarking tool. Runs commands multiple times, warms up,
and reports mean/min/max/stddev with outlier detection.

## Basic usage

```bash
hyperfine 'sleep 0.3'                         # benchmark a single command
hyperfine 'grep -r foo .' 'rg foo .'          # compare two commands
hyperfine --warmup 3 'make build'             # warmup runs before measuring
```

## Common flags

| Flag | Meaning |
|------|---------|
| `--warmup N`        | Run N warmup iterations first |
| `--min-runs N`      | Minimum number of runs (default: 10) |
| `--runs N`          | Exact number of runs |
| `--prepare cmd`     | Run a command before each benchmark (e.g. clear cache) |
| `--export-json f`   | Save results to JSON |
| `--export-markdown f` | Save results as Markdown table |
| `-s basic`          | Show basic stats only |
| `--shell=none`      | Don't use a shell (faster for simple commands) |

## Comparing commands

```bash
# grep vs ripgrep
hyperfine --warmup 5 \
  'grep -r "TODO" ./src' \
  'rg "TODO" ./src'

# Python vs PyPy
hyperfine 'python script.py' 'pypy script.py'

# Different sort algorithms
hyperfine 'sort -n data.txt' 'sort -g data.txt'
```

## With setup/teardown

```bash
# Clear disk cache between runs (macOS)
hyperfine --prepare 'sync && sudo purge' 'cat large_file.txt'

# Build benchmarks — clean before each run
hyperfine --prepare 'make clean' 'make build'
```

## Parameterized benchmarks

```bash
# Test with different input sizes
hyperfine --parameter-list size 100,1000,10000 \
  'python sort.py --size {size}'
```

## Export results

```bash
# Export to markdown (great for READMEs)
hyperfine --export-markdown results.md 'cmd1' 'cmd2'

# Export to JSON for further analysis
hyperfine --export-json results.json 'cmd1' 'cmd2'
```

## Use-cases

- Comparing `grep` vs `ripgrep` vs `ack`
- Measuring impact of a code optimization
- Benchmarking build tools or compilation steps
- Documenting performance in READMEs with markdown tables
