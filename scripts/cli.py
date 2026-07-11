#!/usr/bin/env python3
"""CLI: redis-cli-tool

Redis CLI helper with pretty output.
"""
import sys, json, argparse
def main():
    parser = argparse.ArgumentParser(description="Redis CLI helper with pretty output.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = {"tool": "redis-cli-tool", "ready": True, "version": "1.0.0", "author": "Jose Zuma"}
    print(json.dumps(result, indent=2) if args.json else f"{name} v1.0.0")
if __name__ == "__main__":
    main()
