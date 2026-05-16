# asciinema — Record Terminal Sessions

Records terminal sessions and lets you share them as lightweight, text-based
animations (not video). Viewers can pause, copy text from the recording.

## Basic usage

```bash
asciinema rec                         # start recording (Ctrl+D or exit to stop)
asciinema rec demo.cast               # save to a local file
asciinema play demo.cast              # play back a recording
asciinema upload demo.cast            # upload to asciinema.org
```

## Recording options

```bash
asciinema rec -t "My Demo" demo.cast        # set a title
asciinema rec --overwrite demo.cast         # overwrite existing file
asciinema rec -i 2.5 demo.cast             # cap idle time to 2.5s (avoids long pauses)
asciinema rec -c "bash --norc" demo.cast   # use a specific shell/command
```

## Playback options

```bash
asciinema play demo.cast              # play at recorded speed
asciinema play -s 2 demo.cast        # play at 2x speed
asciinema play -i 1 demo.cast        # cap idle pauses to 1 second
```

## Workflow: record → share

```bash
# 1. Record
asciinema rec demo.cast

# 2. Review locally
asciinema play demo.cast

# 3. Upload and get a shareable link
asciinema upload demo.cast
# → https://asciinema.org/a/abc123
```

## Embedding in a README

After uploading, asciinema gives you an embed link:

```markdown
[![asciicast](https://asciinema.org/a/abc123.svg)](https://asciinema.org/a/abc123)
```

## Use-cases

- Documenting CLI tools or workflows for teammates
- Creating demos for open source project READMEs
- Recording interview coding sessions or walkthroughs
- Sharing debugging sessions without screen recording software

## Tips

- `-i 2.5` is almost always worth using — removes awkward pauses
- The `.cast` file is JSON — it's diff-able and can be edited manually
- Viewers can copy-paste commands directly from the recording
