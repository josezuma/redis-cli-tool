#!/usr/bin/env python3
"""redis-cli-tool — Redis CLI helper. Check keys, memory usage, slow logs, connected clients.
Wraps the redis-cli command with formatted, colorized output."""

import sys, json, subprocess, argparse

REDIS_CMDS = {
    "info": "redis-cli INFO",
    "keys": "redis-cli DBSIZE",
    "memory": "redis-cli INFO memory",
    "slowlog": "redis-cli SLOWLOG GET 10",
    "clients": "redis-cli CLIENT LIST",
    "ping": "redis-cli PING",
}

def run_redis(cmd, host=None, port=None):
    base = "redis-cli"
    if host:
        base += f" -h {host}"
    if port:
        base += f" -p {port}"
    
    parts = cmd.split(" ", 1)
    full_cmd = f"{base} {parts[1]}" if len(parts) > 1 else base
    
    try:
        r = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=5)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except FileNotFoundError:
        return None, "redis-cli not found. Install Redis CLI.", 1
    except subprocess.TimeoutExpired:
        return None, "Command timed out", 1

def format_info(output):
    lines = output.split("\n")
    sections = {}
    current_section = None
    for line in lines:
        if line.startswith("#"):
            current_section = line.strip("# ").strip()
            sections[current_section] = {}
        elif ":" in line and current_section:
            k, v = line.split(":", 1)
            sections[current_section][k.strip()] = v.strip()
    return sections

def main():
    parser = argparse.ArgumentParser(description="Redis CLI helper with pretty output")
    parser.add_argument("command", nargs="?", default="info", 
                       choices=["info", "keys", "memory", "slowlog", "clients", "ping"],
                       help="Redis command to run")
    parser.add_argument("--host", default=None, help="Redis host")
    parser.add_argument("--port", type=int, default=None, help="Redis port")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cmd = REDIS_CMDS.get(args.command, "redis-cli INFO")
    stdout, stderr, rc = run_redis(cmd, args.host, args.port)

    if stderr and "not found" in stderr:
        print(stderr, file=sys.stderr)
        sys.exit(1)

    if rc != 0:
        print(f"Error: {stderr or 'command failed'}", file=sys.stderr)
        sys.exit(1)

    if args.command == "info":
        sections = format_info(stdout)
        result = {
            "server": sections.get("Server", {}),
            "memory": sections.get("Memory", {}),
            "clients": sections.get("Clients", {}),
            "stats": sections.get("Stats", {}),
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"🖥️  Redis Server Info")
            s = result["server"]
            print(f"  Version: {s.get('redis_version', '?')}")
            print(f"  Uptime:  {s.get('uptime_in_days', '?')} days")
            m = result["memory"]
            print(f"  Memory:  {m.get('used_memory_human', '?')} / {m.get('total_system_memory_human', '?')}")
            c = result["clients"]
            print(f"  Clients: {c.get('connected_clients', '?')} connected")
    
    elif args.command == "keys":
        if args.json:
            print(json.dumps({"keys": int(stdout)}))
        else:
            print(f"🗝️  Total keys: {stdout}")
    
    elif args.command == "memory":
        sections = format_info(stdout)
        mem = sections.get("Memory", {})
        if args.json:
            print(json.dumps(mem))
        else:
            print(f"💾 Redis Memory")
            print(f"  Used:       {mem.get('used_memory_human', '?')}")
            print(f"  Peak:       {mem.get('used_memory_peak_human', '?')}")
            print(f"  RSS:        {mem.get('used_memory_rss_human', '?')}")
            print(f"  Fragmentation: {mem.get('mem_fragmentation_ratio', '?')}")
    
    elif args.command == "slowlog":
        lines = stdout.split("\n")
        entries = []
        for line in lines:
            if line.strip() and not line.startswith("127."):
                entries.append(line.strip())
        if args.json:
            print(json.dumps({"slowlog_entries": entries[:10]}))
        else:
            print(f"🐢 Slow Log (last 10)")
            for e in entries[:10]:
                print(f"  {e[:120]}")
    
    elif args.command == "clients":
        clients = [c.strip() for c in stdout.split("\n") if c.strip()]
        if args.json:
            print(json.dumps({"clients": clients}))
        else:
            print(f"👥 Connected Clients: {len(clients)}")
            for c in clients[:10]:
                parts = c.split(" ")
                addr = [p.split("=")[1] for p in parts if p.startswith("addr")] or ["?"]
                print(f"  {addr[0]}")

    elif args.command == "ping":
        result = {"ping": stdout == "PONG"}
        if args.json:
            print(json.dumps(result))
        else:
            print(f"{'✅ Redis is alive' if result['ping'] else '❌ No response'}")


if __name__ == "__main__":
    main()
