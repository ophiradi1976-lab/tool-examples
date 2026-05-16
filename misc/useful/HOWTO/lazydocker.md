# lazydocker — Terminal UI for Docker

A keyboard-driven Docker TUI for managing containers, images, volumes, and
networks without typing long `docker` commands.

## Launch

```bash
lazydocker
```

## Panel layout

```
┌──────────────┬─────────────────────────────┐
│  Projects    │                             │
├──────────────┤       Main panel            │
│  Containers  │   (logs / stats / config)   │
├──────────────┤                             │
│  Services    │                             │
├──────────────┼─────────────────────────────┤
│  Images      │                             │
├──────────────┤                             │
│  Volumes     │                             │
└──────────────┴─────────────────────────────┘
```

Navigate panels with arrow keys or `h`/`l`. Move between items with `j`/`k`.

## Essential keybindings

### Containers
| Key | Action |
|-----|--------|
| `Enter` | View logs |
| `d` | Remove container |
| `s` | Stop container |
| `r` | Restart container |
| `e` | Exec into shell (`/bin/sh`) |
| `[` / `]` | Switch main panel view (logs / stats / config / top) |

### Images
| Key | Action |
|-----|--------|
| `d` | Remove image |
| `f` | Pull latest |

### General
| Key | Action |
|-----|--------|
| `q` | Quit |
| `?` | Show keybindings |
| `x` | Open command menu for current item |

## Main panel views (toggle with `[` / `]`)

- **Logs** — live log stream for the selected container
- **Stats** — CPU, memory, network I/O
- **Config** — full container inspect output
- **Top** — processes running inside the container

## docker-compose support

lazydocker detects `docker-compose.yml` and groups containers under a
**Services** panel, letting you start/stop services as a group.

## Use-cases

- Monitoring a local dev stack (logs + resource usage at a glance)
- Quickly exec-ing into a container without remembering the container ID
- Cleaning up stopped containers, dangling images, and unused volumes
- Watching real-time stats across multiple containers simultaneously
