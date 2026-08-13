# Velora

> A personal productivity and task management app built with Kotlin Multiplatform.

[![CI](https://github.com/AlirezaNezami96/Velora/actions/workflows/ci.yml/badge.svg)](https://github.com/AlirezaNezami96/Velora/actions/workflows/ci.yml)

---

## What is Velora?

Velora is a mobile productivity application targeting **Android** and **iOS**
from a single Kotlin codebase. It is designed around daily planning, task
management, and focus — helping users capture what needs to be done and plan
when to do it.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Kotlin |
| Multiplatform | Kotlin Multiplatform (KMM) |
| UI | Compose Multiplatform |
| Networking | Ktor |
| Local DB | SQLDelight |
| Preferences | DataStore |
| DI | Koin |
| Async | Coroutines + Flow |
| Testing | Kotlin Test · Kotest · Turbine |

---

## Project Structure

```
Velora/
├── composeApp/       # Shared Compose UI + platform entry points
├── shared/           # Domain + data layers (KMM)
├── core/
│   ├── common/       # Utilities, extensions, base types
│   ├── designsystem/ # Tokens, components
│   ├── network/      # Ktor client
│   ├── database/     # SQLDelight
│   ├── datastore/    # DataStore
│   └── testing/      # Test utilities
├── feature/
│   ├── home/         # Home feature
│   └── settings/     # Settings feature
├── iosApp/           # iOS host
└── automation/       # Python autonomous development agent
```

---

## Development

### Prerequisites

- JDK 17+
- Android SDK (API 26+)
- Xcode 15+ (for iOS)
- Kotlin Multiplatform plugin

### Build

```bash
./gradlew build
```

### Run tests

```bash
./gradlew allTests
```

### Run Android app

```bash
./gradlew :composeApp:installDebug
```

---

## Autonomous Development Agent

This project is continuously developed by an autonomous agent that runs 4 times
per day via GitHub Actions. The agent:

1. Inspects the current repository state
2. Reads the 12-month roadmap
3. Plans the next smallest meaningful engineering tasks
4. Generates code changes using the Gemini API
5. Commits each change (≤50 lines/commit)
6. Pushes to GitHub

See [`automation/`](automation/) for the agent source code and
[`ROADMAP.md`](ROADMAP.md) for the 12-month engineering plan.

---

## Documentation

- [ROADMAP.md](ROADMAP.md) — 12-month engineering plan
- [ARCHITECTURE.md](ARCHITECTURE.md) — architecture decisions
- [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md) — tracked debt
- [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md) — cycle-by-cycle log

---

## Contributing

This repository is under active autonomous development. Human contributions
are welcome on feature branches via pull requests.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
