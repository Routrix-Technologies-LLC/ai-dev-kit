---
name: kit-homelab
description: Use for any home lab, server or home network work - setting up or fixing a server, NAS, Raspberry Pi, Proxmox or other hypervisor, Docker or containers, a reverse proxy, DNS, VPN, backups, a router, firewall, switch or Wi-Fi, or self-hosting an app - and whenever the person mentions a host, IP, port or device by name. Keeps a homelab notes repository as the single record of what exists, reads it before working and writes back to it after, so nothing is asked twice and nothing is forgotten. Also triggers on "document this", "where is X running", "what's the IP of", "add this to my notes".
---

# Home lab work

Home lab work goes wrong in two ways: changing something without knowing what else depends on it, and forgetting what was done. This skill prevents both with one habit: **read the notes, do the work, write the notes.**

## The notes repository

The record lives in a git repository, by default `~/Projects/homelab-notes/`. If it does not exist, offer to create it (explain in one line: it is a private notebook of their setup that the AI reads and updates, so they never have to repeat an IP or remember what changed). Layout:

```
homelab-notes/
  README.md        inventory: one row per device or host (name, what it is, IP, where it lives, how to reach it)
  network.md       internet connection, router, subnets or VLANs, DHCP and DNS, Wi-Fi, port forwards, VPN
  hosts/<name>.md  one per machine: hardware, OS, what runs on it, how to log in (method only, never the password)
  services/<name>.md  one per service: where it runs, ports, config location, how to update, how to back up
  backups.md       what is backed up, where, how often, when a restore was last tested
  changes.md       dated log, newest first: what changed and why
  todo.md          known problems and ideas
```

Never store passwords, keys, tokens or recovery codes in it. Write where they are kept ("in the password manager under 'NAS admin'"), not what they are. Keep the repository private.

## 1. Before doing anything: read

1. Open the notes repository and read `README.md`, then the files for the devices and services involved.
2. Ask only for what is not written down, and write the answer in when you get it.
3. If the notes and reality disagree, trust reality, say so, and fix the notes.

## 2. While working

- **Read-only first.** Look before changing: status commands, config files, logs. Changes to a router, firewall, switch, DNS, or anything other things depend on need the person's go-ahead after you explain what will change and what could break.
- **Back up a config before changing it,** and say how to put it back.
- **Do not open anything to the internet** (port forwards, public DNS records, disabling a firewall rule, exposing an admin page) without explaining the risk and the safer alternatives (a VPN such as WireGuard or Tailscale, or an authenticated tunnel), and getting a clear yes.
- **Verify before alarming.** Do not call something exposed or broken from config alone; check it (from outside the network if it is about exposure) and show the evidence. If you cannot check, say "unverified".
- **Use the specialists.** `infrastructure-engineer` for containers, Docker Compose, reverse proxies, TLS, DNS and hosting; `site-reliability-engineer` for monitoring, alerting and backups; `security-engineer` for hardening a service. For a full security review of the lab, `/kit-start` sets up the security team with a written scope. Apps they want to build and host go through the App Studio (`/app-start`).
- Copy config files that matter into the notes with secrets replaced by `<redacted>`. Never copy `.env` files or key files.

## 3. Before finishing: write back

1. Update the right files: new device in `README.md` and `hosts/`, new service in `services/`, network changes in `network.md`, new data in `backups.md`.
2. Add a dated line to `changes.md` saying what changed and why.
3. Anything unknown or unfinished goes in `todo.md`, never guessed.
4. Check that no secret slipped in, then commit (and push if it has a private remote).
5. Tell the person in one line what was recorded and where.
