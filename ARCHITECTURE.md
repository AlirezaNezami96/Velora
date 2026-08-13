# Velora — Architecture

## Overview

Velora is a personal productivity and task-management application built with
**Kotlin Multiplatform (KMM)** and **Compose Multiplatform**. It targets
**Android** and **iOS** from a single shared codebase.

---

## Module Structure

```
Velora/
├── composeApp/               # Android/iOS app entry point, shared Compose UI
├── shared/                   # Shared domain and data layers
├── core/
│   ├── common/               # Utilities, extensions, Result type, Logger
│   ├── designsystem/         # Color, typography, shape tokens + UI components
│   ├── network/              # Ktor HTTP client, API infrastructure
│   ├── database/             # SQLDelight schema and drivers
│   ├── datastore/            # DataStore preferences
│   └── testing/              # Shared test utilities, fakes, fixtures
├── feature/
│   ├── home/                 # Home screen: task list, filters
│   └── settings/             # User preferences, theme
├── iosApp/                   # iOS host application (Swift)
└── automation/               # Python autonomous development agent
```

---

## Architectural Layers

```
┌─────────────────────────────────────────────┐
│                Presentation                 │
│  Compose UI · ViewModel · UiState · Events  │
└───────────────────┬─────────────────────────┘
                    │ uses
┌───────────────────▼─────────────────────────┐
│                  Domain                     │
│      Models · Repositories (interfaces)     │
│      Use Cases · Business Rules             │
└───────────────────┬─────────────────────────┘
                    │ implements
┌───────────────────▼─────────────────────────┐
│                   Data                      │
│  Repository Implementations · Mappers       │
│  SQLDelight · DataStore · Ktor API          │
└─────────────────────────────────────────────┘
```

---

## Key Decisions

### 1. Kotlin Multiplatform for Shared Logic
All domain and data logic lives in the `shared` module targeting both platforms.
Platform-specific code is isolated via `expect`/`actual` declarations.

### 2. Compose Multiplatform for Shared UI
The UI is written once in Compose and rendered natively on both Android and iOS.
Platform-specific entry points (`MainActivity`, `ContentView`) initialize the
shared Compose tree.

### 3. Unidirectional Data Flow (UDF)
Each screen has:
- `UiState` — immutable data class representing the current state
- `Event` — sealed class representing user actions
- `ViewModel` — transforms events into state using `StateFlow`

### 4. Koin for Dependency Injection
Koin is chosen for its Kotlin-first API and KMM compatibility.
Modules are structured by layer: `DomainModule`, `DataModule`, `NetworkModule`.

### 5. SQLDelight for Local Persistence
SQLDelight generates type-safe Kotlin APIs from SQL schemas.
Platform drivers (Android/iOS) are provided via `expect`/`actual` factories.

### 6. Ktor for Networking
Ktor is used for HTTP communication with a KMM-compatible engine per platform.

### 7. Repository Pattern
Repositories abstract data sources from the domain layer.
All repositories expose `Flow<T>` for reactive data streams.

### 8. Offline-First
Local database is always the source of truth.
Background sync updates the local database; UI observes the local source.

---

## Navigation

Type-safe navigation using the Compose Navigation library.
Routes are defined as sealed classes in `Screen.kt`.

---

## Testing Strategy

```
Unit tests        → domain models, use cases, mappers, ViewModels
Integration tests → repository implementations (in-memory DB)
UI tests          → Compose screen interactions
E2E tests         → critical user flows (future)
```

---

## Platform-Specific Code

| Concern | Android | iOS |
|---------|---------|-----|
| SQLDelight driver | `AndroidSqliteDriver` | `NativeSqliteDriver` |
| DataStore | `createDataStore` (Context) | `createDataStore` (path) |
| Ktor engine | `Android` | `Darwin` |
| Logger | `android.util.Log` | `NSLog` |

---

*Last updated: 2026-08-13 by Velora Autonomous Agent*
