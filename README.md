# USCAN

```
 ██╗   ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
 ██║   ██║██╔════╝██╔════╝██╔══██╗████╗  ██║
 ██║   ██║███████╗██║     ███████║██╔██╗ ██║
 ██║   ██║╚════██║██║     ██╔══██║██║╚██╗██║
 ╚██████╔╝███████║╚██████╗██║  ██║██║ ╚████║
  ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
```

**Username Intelligence & OSINT Discovery Tool**

A fast, modular CLI application that checks public profile URLs across 60+ online platforms to discover where a username is registered. Built for security researchers, OSINT analysts, and digital investigators.

---

## Features

- **68 platforms** — Social, developer, gaming, content, and professional platforms
- **Async scanning** — Concurrent checks with configurable worker count
- **Confidence scoring** — HIGH / MEDIUM / LOW with platform-specific false-positive detection
- **5 export formats** — JSON, TXT, CSV, HTML, and PDF reports
- **Professional terminal UI** — Rich output with progress tracking, color-coded results, and summary tables
- **Mock & demo modes** — Full offline testing without network access
- **Cross-platform** — Linux, macOS, Windows, Kali Linux, Termux
- **Modular architecture** — Add new platforms by creating a single adapter class

---

## Installation

### Prerequisites

- **Python 3.10+** (3.12+ recommended)
- **pip** (comes with Python)
- **git** (to clone the repository)

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/). Check **"Add Python to PATH"** during installation.

2. Open **Command Prompt** or **PowerShell**:

```bash
git clone https://github.com/nexera-tech7/Osint-tool
cd uscan
pip install -e .
```

3. Verify:

```bash
uscan --version
```

> **Note:** On Windows, if `uscan` is not recognized, use `python -m uscan` instead, or ensure your Python Scripts directory is in your PATH.

### macOS

1. Install Python 3 (if not already installed):

```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

2. Clone and install:

```bash
git clone https://github.com/nexera-tech7/Osint-tool
cd uscan
pip3 install -e .
```

3. Verify:

```bash
uscan --version
```

> **Note:** On macOS, use `pip3` and `python3` if your system still ships Python 2 as the default `python`.

### Linux (Ubuntu / Debian / Kali)

1. Install Python and pip:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

2. Clone and install:

```bash
git clone https://github.com/nexera-tech7/Osint-tool
cd uscan
pip3 install -e .
```

3. Verify:

```bash
uscan --version
```

> **Kali Linux:** Python 3 and pip are pre-installed. You may need to use `pip3 install --break-system-packages -e .` or use a virtual environment.

### Linux (Fedora / Arch)

```bash
# Fedora
sudo dnf install python3 python3-pip git

# Arch
sudo pacman -S python python-pip git
```

Then clone and install as above.

### Termux (Android)

```bash
pkg update
pkg install python git
git clone https://github.com/nexera-tech7/Osint-tool
cd uscan
pip install -e .
uscan --version
```

### Virtual Environment (Recommended for all platforms)

Using a virtual environment keeps USCAN isolated from your system Python:

```bash
git clone https://github.com/nexera-tech7/Osint-tool
cd uscan

# Create virtual environment
python3 -m venv .venv

# Activate it
# Linux / macOS:
source .venv/bin/activate
# Windows (CMD):
.venv\Scripts\activate.bat
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install
pip install -e .
```

### Optional: PDF Export Support

PDF report generation requires ReportLab:

```bash
pip install -e ".[pdf]"
```

### Optional: Development Dependencies

For running tests and contributing:

```bash
pip install -e ".[dev]"
```

---

## Quick Start

```bash
# Scan a username across all platforms
uscan <user_name>

# Demo mode (no network required)
uscan --demo

# Mock mode for offline testing
uscan <user_name> --mock

# Export results
uscan <user_name> --json --html

# Scan only social platforms
uscan <user_name> --category social

# List all supported platforms
uscan --platforms
```

---

## Usage

### Basic Scan

```bash
uscan <username>
```

### Multiple Usernames

```bash
uscan alice bob charlie
```

### From File

```bash
uscan --input usernames.txt
```

### Platform & Category Filters

```bash
uscan <user_name> --platform github
uscan <user_name> --category social
uscan <user_name> --category social,developer
```

### Export Reports

```bash
uscan <user_name> --json                    # JSON report
uscan <user_name> --txt                     # Plain text report
uscan <user_name> --csv                     # CSV spreadsheet
uscan <user_name> --html                    # Standalone HTML report
uscan <user_name> --pdf                     # PDF report
uscan <user_name> --json --output report.json  # Custom output path
```

### Performance Tuning

```bash
uscan <user_name> --threads 20             # Increase concurrency (max 30)
uscan <user_name> --timeout 5              # Shorter timeout
```

### Display Options

```bash
uscan <user_name> --only-found             # Show only confirmed profiles
uscan <user_name> --quiet                  # Minimal output
uscan <user_name> --verbose                # Debug logging
uscan <user_name> --no-color               # Disable colors
```

### Username Variants

```bash
uscan <user_name> --variants               # Also scans _<user_name>, <user_name>_, <user_name>123, etc.
```

### Caching

```bash
uscan <user_name> --cache                  # Cache results for 1 hour
uscan --clear-cache                  # Clear all cached results
```

---

## Commands Reference

| Option | Short | Description |
|---|---|---|
| `<username>` | | Username(s) to scan |
| `--platform` | `-p` | Scan specific platform(s), comma-separated |
| `--category` | `-c` | Filter by category: social, developer, gaming, content, professional |
| `--threads` | `-t` | Concurrent workers (1–30, default: 10) |
| `--timeout` | | Request timeout in seconds (default: 10) |
| `--quiet` | `-q` | Minimal output |
| `--verbose` | `-v` | Debug logging |
| `--no-color` | | Disable terminal colors |
| `--only-found` | | Show only confirmed profiles |
| `--json` | | Export JSON report |
| `--txt` | | Export plain text report |
| `--csv` | | Export CSV report |
| `--html` | | Export HTML report |
| `--pdf` | | Export PDF report |
| `--output` | `-o` | Custom output file path |
| `--input` | `-i` | Read usernames from file (one per line) |
| `--mock` | | Run with deterministic mock data (no network) |
| `--demo` | | Demo mode with simulated results |
| `--variants` | | Scan common username variants |
| `--platforms` | | List all supported platforms |
| `--cache` | | Enable result caching |
| `--clear-cache` | | Clear cached results |
| `--version` | `-V` | Show version |

---

## Supported Platforms (68)

### Social (13)
Instagram, X (Twitter), Facebook, TikTok, Snapchat, Threads, Bluesky, Mastodon, P<user_name>est, Tumblr, VK, Telegram, Reddit

### Developer (17)
GitHub, GitLab, Bitbucket, Codeberg, Stack Overflow, HackerRank, LeetCode, CodePen, Replit, Kaggle, Dev.to, SourceForge, Hugging Face, npm, PyPI, GitHub Gist, Docker Hub

### Gaming (6)
Twitch, Steam, Roblox, Xbox, Chess.com, NameMC

### Content (12)
YouTube, Vimeo, Medium, Substack, SoundCloud, Spotify, Flickr, Dailymotion, Imgur, Hashnode, Mixcloud, Letterboxd, Last.fm, Giphy

### Professional (7)
LinkedIn, Behance, Dribbble, Gravatar, About.me, Linktree, Fiverr

### Other (13)
Patreon, Buy Me a Coffee, Product Hunt, Hacker News, Keybase, Wikipedia, TryHackMe, Hack The Box, Disqus, Goodreads, Instructables

---

## Architecture

```
src/uscan/
├── cli.py              # Typer CLI entry point
├── config.py           # TOML configuration loader
├── banner.py           # ASCII branding
├── mock.py             # Mock/demo engine
├── cache.py            # File-based result cache
├── scanner/
│   ├── engine.py       # Async scan orchestrator
│   ├── worker.py       # Per-platform check worker
│   ├── models.py       # Pydantic result models
│   ├── classifier.py   # HTTP response classifier
│   └── rate_limiter.py # Token-bucket rate limiter
├── platforms/
│   ├── base.py         # Platform adapter <user_name>face
│   ├── registry.py     # Platform catalog
│   ├── social.py       # Social media adapters
│   ├── developer.py    # Developer platform adapters
│   ├── gaming.py       # Gaming platform adapters
│   ├── content.py      # Content platform adapters
│   ├── professional.py # Professional platform adapters
│   └── other.py        # Other platform adapters
├── exporters/
│   ├── json_exporter.py
│   ├── txt_exporter.py
│   ├── csv_exporter.py
│   ├── html_exporter.py
│   └── pdf_exporter.py
└── ui/
    ├── console.py      # Main console UI controller
    ├── theme.py        # Color theme & styling
    ├── tables.py       # Result tables
    └── progress.py     # Live progress display
```

---

## Configuration

Create a config file at `~/.config/uscan/config.toml` (Linux/macOS) or `%APPDATA%\uscan\config.toml` (Windows):

```toml
[scan]
concurrency = 15
timeout = 8.0
retries = 2
retry_delay = 1.0

[output]
directory = "~/reports"
color = true

[cache]
enabled = false
ttl_seconds = 3600

[platforms]
disabled = ["LinkedIn"]
```

---

## Development

### Setup

```bash
git clone https://github.com/nexera-tech7/Osint-tool
cd uscan
python3 -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

All tests use mocked data and run fully offline — no network requests are made.

### Adding a New Platform

1. Open the appropriate file in `src/uscan/platforms/` (e.g., `social.py`)
2. Add a new class:

```python
class NewPlatform(Platform):
    name = "NewPlatform"
    category = "social"
    url_pattern = "https://newplatform.com/{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,30}$"
    max_length = 30
    not_found_indicators = ["User not found"]
    found_indicators = ["newplatform.com", "profile-header"]
```

3. Add it to the platform list at the bottom of the file
4. Run tests to verify

---

## Troubleshooting

### `uscan` command not found

- **Windows:** Use `python -m uscan` or add Python's Scripts folder to your PATH
- **Linux/macOS:** Use `python3 -m uscan` or ensure `~/.local/bin` is in your PATH
- **Virtual env:** Make sure you activated it (`source .venv/bin/activate`)

### Unicode characters display incorrectly (Windows)

Set your terminal to UTF-8:

```bash
chcp 65001
```

Or use Windows Terminal, which handles UTF-8 natively.

### SSL/TLS errors

Some platforms may fail with SSL errors behind corporate proxies. Set your certificates:

```bash
export SSL_CERT_FILE=/path/to/your/certificate.pem
```

### Rate limiting

If many platforms return RATE_LIMITED, reduce concurrency:

```bash
uscan <user_name> --threads 5
```

---

## Responsible Use

USCAN is designed for legitimate security research, OSINT analysis, and personal account auditing. It only checks publicly accessible profile URLs — it does not access private data, bypass authentication, solve CAPTCHAs, or circumvent security controls.

**Do:**
- Use it for authorized security assessments
- Audit your own digital footprint
- Conduct legitimate OSINT research

**Do not:**
- Use it for harassment, stalking, or doxxing
- Attempt to access private or protected accounts
- Violate any platform's terms of service
- Use it for any illegal activity

Users are solely responsible for complying with all applicable laws and platform terms of service in their jurisdiction.

---

## License

MIT — see [LICENSE](LICENSE) for details.
