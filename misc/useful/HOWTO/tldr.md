# tldr — Simplified Man Pages

Community-maintained, practical cheatsheets for CLI commands. Shows common
usage examples instead of exhaustive documentation.

## Basic usage

```bash
tldr tar                  # cheatsheet for tar
tldr git commit           # multi-word commands
tldr curl                 # common curl usage
tldr --update             # update the local cache (run periodically)
```

## Flags

```bash
tldr -l                   # list all available pages
tldr -s                   # list available subcommands for a command
tldr -p linux tar         # specify platform (linux, macos, windows, common)
tldr -p macos open        # macOS-specific page
```

## Use-cases

```bash
# Forgot the tar flags? 
tldr tar

# Quickly recall ffmpeg patterns
tldr ffmpeg

# Check curl syntax without reading the whole man page
tldr curl

# Remember how to use rsync
tldr rsync
```

## Tips

- Run `tldr --update` occasionally to get new/updated pages
- If a page doesn't exist yet, `man` is the fallback
- Pages live at https://github.com/tldr-pages/tldr — you can contribute
- For more detail, always fall back to `man <command>`
