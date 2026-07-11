<div align=center>
  <h1>🗝️ Redis CLI Tool</h1>
  <p><em>A friendly Redis CLI wrapper. Check keys, memory usage, slow logs, connected clients, and server info — all with formatted, colorized output. Wraps the standard redis-cli with better ergonomics.</em></p>
  <p><a href=LICENSE><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt=License></a></p>
  <p><strong>Author:</strong> <a href=https://github.com/josezuma>Jose Zuma</a></p>
</div>

---

## Quick Start

```bash
git clone https://github.com/josezuma/redis-cli-tool.git
cd redis-cli-tool
python3 scripts/redis_tool.py info
```

## Prerequisites

Redis CLI must be installed and a Redis server running locally or accessible.

```bash
# macOS
brew install redis

# Ubuntu/Debian
sudo apt-get install redis-tools

# Verify
redis-cli PING
```

## Demo

```bash
$ python3 scripts/redis_tool.py info

🖥️  Redis Server Info
  Version: 7.2.4
  Uptime:  14 days
  Memory:  2.45M / 16.00G
  Clients: 3 connected
```

```bash
$ python3 scripts/redis_tool.py keys
🗝️  Total keys: 42
```

```bash
$ python3 scripts/redis_tool.py memory

💾 Redis Memory
  Used:       2.45M
  Peak:       4.12M
  RSS:        8.50M
  Fragmentation: 1.02
```

```bash
$ python3 scripts/redis_tool.py clients
👥 Connected Clients: 3
  127.0.0.1:54321
  127.0.0.1:54322
  127.0.0.1:54323
```

## Commands

| Command | Description |
|---------|-------------|
| `info` | Server info: version, uptime, memory, clients |
| `keys` | Total key count via DBSIZE |
| `memory` | Detailed memory stats (used, peak, RSS, fragmentation) |
| `slowlog` | Last 10 slow queries |
| `clients` | List of connected clients with addresses |
| `ping` | Check if Redis is alive |

## Options

```bash
# Connect to a specific host/port
python3 scripts/redis_tool.py info --host myredis.example.com --port 6379

# JSON output for monitoring
python3 scripts/redis_tool.py memory --json
```

## Related

- [ssl-cert-monitor](https://github.com/josezuma/ssl-cert-monitor)
- [dns-lookup](https://github.com/josezuma/dns-lookup)
- [port-forward-manager](https://github.com/josezuma/port-forward-manager)

## License

MIT © 2026 Jose Zuma
