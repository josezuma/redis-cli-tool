# FAQ

## Do I need Redis installed?
Yes. This tool wraps redis-cli, which must be installed separately.

## Can I connect to a remote Redis?
Yes. Use `--host` and `--port` flags. Redis must be accessible over the network.

## Is it safe for production?
Yes. The tool only runs read-only commands (INFO, DBSIZE, SLOWLOG, CLIENT LIST, PING).

## What about Redis passwords?
Use `--host` flag and set `REDISCLI_AUTH` environment variable for password auth.

## Why not just use redis-cli directly?
This tool formats output, supports multiple commands with pretty-printing, and has JSON mode for monitoring pipelines.
