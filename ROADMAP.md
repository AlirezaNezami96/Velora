# Velora — 12-Month Engineering Roadmap

**Application:** Velora — Personal Productivity & Task Management  
**Stack:** Kotlin Multiplatform · Compose Multiplatform · Android · iOS  
**Start Date:** 2026-08  
**Target Completion:** 2027-08  
**Daily Cycles:** 4 runs/day · 10–15 commits/run · ≤50 lines/commit

---

## Legend

- `[ ]` Not started
- `[/]` In progress
- `[x]` Complete
- `[!]` Blocked

---

## Phase 1 — Foundation (Months 1–2: Aug–Sep 2026)

### 1.1 Project Scaffolding
- [ ] Create root `settings.gradle.kts` with all modules
- [ ] Create `gradle/libs.versions.toml` version catalog
- [ ] Configure root `build.gradle.kts`
- [ ] Configure `composeApp/build.gradle.kts` (KMM + Compose)
- [ ] Configure `shared/build.gradle.kts`
- [ ] Configure `core/common/build.gradle.kts`
- [ ] Configure `core/designsystem/build.gradle.kts`
- [ ] Configure `core/network/build.gradle.kts`
- [ ] Configure `core/database/build.gradle.kts`
- [ ] Configure `core/datastore/build.gradle.kts`
- [ ] Configure `core/testing/build.gradle.kts`
- [ ] Configure `feature/home/build.gradle.kts`
- [ ] Configure `feature/settings/build.gradle.kts`
- [ ] Add Android `AndroidManifest.xml` to composeApp
- [ ] Add iOS `iosApp.xcodeproj` scaffolding
- [ ] Create `.gitignore` (Kotlin/Android/iOS/Gradle/macOS)
- [ ] Create `.editorconfig`

### 1.2 Build System
- [ ] Verify all modules compile from CLI (`./gradlew build`)
- [ ] Add Gradle wrapper (gradlew, gradlew.bat, gradle-wrapper.jar)
- [ ] Pin Gradle version to stable release
- [ ] Enable Gradle caching configuration

### 1.3 CI/CD Foundation
- [ ] Create `.github/workflows/ci.yml` (build + test on push/PR)
- [ ] Create four daily agent workflows (00:00, 06:00, 12:00, 18:00 UTC)
- [ ] Verify CI passes on first push

### 1.4 Code Quality Infrastructure
- [ ] Add `detekt` static analysis
- [ ] Create `detekt.yml` config
- [ ] Add detekt to CI pipeline
- [ ] Add `.editorconfig` for consistent formatting
- [ ] Add `kotlinx-coroutines` linting rules

### 1.5 Logging & Error Infrastructure (shared module)
- [ ] Create `core/common/Logger.kt` (expect/actual for platform logging)
- [ ] Create `core/common/Result.kt` (sealed class: Success/Error/Loading)
- [ ] Create `core/common/extensions/FlowExtensions.kt`
- [ ] Create `core/common/extensions/StringExtensions.kt`

### 1.6 Documentation
- [ ] `README.md` — project overview, setup guide
- [ ] `ARCHITECTURE.md` — architecture decisions and module map
- [ ] `TECHNICAL_DEBT.md` — initial tracking
- [ ] `DEVELOPMENT_LOG.md` — first entry

---

## Phase 2 — Domain Layer (Month 2: Sep 2026)

### 2.1 Core Domain Models
- [ ] `shared/domain/model/Task.kt`
- [ ] `shared/domain/model/Category.kt`
- [ ] `shared/domain/model/Priority.kt` (enum)
- [ ] `shared/domain/model/TaskStatus.kt` (enum)
- [ ] `shared/domain/model/DailyPlan.kt`

### 2.2 Repository Interfaces
- [ ] `shared/domain/repository/TaskRepository.kt`
- [ ] `shared/domain/repository/CategoryRepository.kt`
- [ ] `shared/domain/repository/PlanRepository.kt`

### 2.3 Use Cases
- [ ] `shared/domain/usecase/GetAllTasksUseCase.kt`
- [ ] `shared/domain/usecase/CreateTaskUseCase.kt`
- [ ] `shared/domain/usecase/UpdateTaskUseCase.kt`
- [ ] `shared/domain/usecase/DeleteTaskUseCase.kt`
- [ ] `shared/domain/usecase/GetTasksByStatusUseCase.kt`
- [ ] `shared/domain/usecase/GetTasksByCategoryUseCase.kt`
- [ ] `shared/domain/usecase/GetTodayPlanUseCase.kt`
- [ ] `shared/domain/usecase/UpdatePlanUseCase.kt`

### 2.4 Domain Tests
- [ ] `shared/test/domain/model/TaskTest.kt`
- [ ] `shared/test/domain/usecase/CreateTaskUseCaseTest.kt`
- [ ] `shared/test/domain/usecase/GetAllTasksUseCaseTest.kt`

---

## Phase 3 — Data Layer (Month 3: Oct 2026)

### 3.1 Local Database (SQLDelight)
- [ ] Configure SQLDelight plugin in `core/database`
- [ ] Create `Task.sq` — CRUD queries
- [ ] Create `Category.sq` — CRUD queries
- [ ] Create `DailyPlan.sq` — CRUD queries
- [ ] Create Android SQLDelight driver factory
- [ ] Create iOS SQLDelight driver factory
- [ ] Create database module initializer

### 3.2 DataStore (Preferences)
- [ ] Configure DataStore in `core/datastore`
- [ ] Create `UserPreferencesDataStore.kt`
- [ ] Create `PreferencesKeys.kt`
- [ ] Android DataStore factory implementation
- [ ] iOS DataStore factory implementation

### 3.3 Data Mappers
- [ ] `TaskMapper.kt` — domain ↔ database entity
- [ ] `CategoryMapper.kt`
- [ ] `DailyPlanMapper.kt`

### 3.4 Repository Implementations
- [ ] `TaskRepositoryImpl.kt`
- [ ] `CategoryRepositoryImpl.kt`
- [ ] `PlanRepositoryImpl.kt`

### 3.5 Data Layer Tests
- [ ] `TaskRepositoryImplTest.kt`
- [ ] `CategoryRepositoryImplTest.kt`
- [ ] SQLDelight query tests

---

## Phase 4 — Networking (Month 3–4: Oct–Nov 2026)

### 4.1 Ktor Client Setup
- [ ] Configure Ktor in `core/network`
- [ ] Create `HttpClientFactory.kt` (expect/actual)
- [ ] Create `NetworkConfig.kt`
- [ ] Add JSON content negotiation plugin
- [ ] Add logging plugin
- [ ] Add timeout configuration

### 4.2 API Infrastructure
- [ ] Create `ApiResult.kt` sealed class
- [ ] Create `ApiException.kt`
- [ ] Create `ResponseMapper.kt`
- [ ] Create base `BaseApiService.kt`

### 4.3 Mock API Integration (local dev)
- [ ] Create `MockInterceptor.kt` for offline testing
- [ ] Create mock JSON fixtures

### 4.4 Network Tests
- [ ] Mock Ktor client tests
- [ ] API error handling tests

---

## Phase 5 — Dependency Injection (Month 4: Nov 2026)

### 5.1 Koin Setup
- [ ] Create `shared/di/SharedModule.kt`
- [ ] Create `shared/di/DomainModule.kt`
- [ ] Create `shared/di/DataModule.kt`
- [ ] Create `core/network/di/NetworkModule.kt`
- [ ] Create `core/database/di/DatabaseModule.kt`
- [ ] Create Android `AppModule.kt`
- [ ] Create iOS Koin initializer

### 5.2 DI Tests
- [ ] Verify all Koin modules can be loaded
- [ ] Check module parameter completeness

---

## Phase 6 — Design System (Month 4–5: Nov–Dec 2026)

### 6.1 Tokens
- [ ] `VeloraColors.kt` — color palette
- [ ] `VeloraTypography.kt` — type scale
- [ ] `VeloraShapes.kt` — shape tokens
- [ ] `VeloraSpacing.kt` — spacing scale
- [ ] `VeloraTheme.kt` — MaterialTheme wrapper

### 6.2 Reusable Components
- [ ] `VeloraButton.kt` — primary/secondary variants
- [ ] `VeloraTextField.kt` — styled input
- [ ] `VeloraTopBar.kt` — app bar
- [ ] `VeloraBottomNav.kt` — navigation bar
- [ ] `VeloraCard.kt` — card container
- [ ] `VeloraChip.kt` — priority/category chips
- [ ] `VeloraLoadingIndicator.kt`
- [ ] `VeloraErrorState.kt`
- [ ] `VeloraEmptyState.kt`

### 6.3 Design System Tests
- [ ] Preview tests for each component

---

## Phase 7 — Navigation (Month 5: Dec 2026)

### 7.1 Navigation Graph
- [ ] Add navigation dependency
- [ ] Create `NavGraph.kt`
- [ ] Create `Screen.kt` sealed class
- [ ] Home route
- [ ] Task detail route
- [ ] Create task route
- [ ] Settings route

### 7.2 Bottom Navigation
- [ ] Create `MainScreen.kt` with bottom nav
- [ ] Integrate NavGraph into App.kt

---

## Phase 8 — Feature: Home (Months 5–6: Dec 2026–Jan 2027)

### 8.1 Home Presentation Layer
- [ ] `HomeState.kt` — UI state model
- [ ] `HomeEvent.kt` — user events
- [ ] `HomeViewModel.kt` — state management
- [ ] `HomeScreen.kt` — Compose UI
- [ ] `TaskListItem.kt` — list item component
- [ ] `CategoryFilter.kt` — horizontal filter bar

### 8.2 Home Tests
- [ ] `HomeViewModelTest.kt`
- [ ] `HomeScreenTest.kt` (UI tests)

---

## Phase 9 — Feature: Task Detail (Month 6: Jan 2027)

- [ ] `TaskDetailState.kt`
- [ ] `TaskDetailEvent.kt`
- [ ] `TaskDetailViewModel.kt`
- [ ] `TaskDetailScreen.kt`
- [ ] Priority picker component
- [ ] Category picker component
- [ ] Due date picker component
- [ ] `TaskDetailViewModelTest.kt`

---

## Phase 10 — Feature: Create Task (Month 6–7: Jan–Feb 2027)

- [ ] `CreateTaskState.kt`
- [ ] `CreateTaskEvent.kt`
- [ ] `CreateTaskViewModel.kt`
- [ ] `CreateTaskScreen.kt`
- [ ] Form validation
- [ ] `CreateTaskViewModelTest.kt`

---

## Phase 11 — Feature: Settings (Month 7: Feb 2027)

- [ ] `SettingsState.kt`
- [ ] `SettingsViewModel.kt`
- [ ] `SettingsScreen.kt`
- [ ] Theme preference (light/dark/system)
- [ ] App version display
- [ ] Data management options

---

## Phase 12 — Feature: Daily Planner (Month 7–8: Feb–Mar 2027)

- [ ] `PlanState.kt`
- [ ] `PlanViewModel.kt`
- [ ] `PlanScreen.kt`
- [ ] Drag-and-drop task ordering
- [ ] Daily schedule view
- [ ] Plan progress indicator

---

## Phase 13 — Offline-First & Sync (Month 8–9: Mar–Apr 2027)

- [ ] Offline-first repository pattern
- [ ] Local cache-first reads
- [ ] Background sync strategy
- [ ] Conflict detection and resolution
- [ ] Sync status UI states
- [ ] Offline mode indicators

---

## Phase 14 — Performance (Month 9: Apr 2027)

- [ ] Measure and optimize startup time
- [ ] Lazy loading for large task lists
- [ ] Database query optimization
- [ ] Memory leak detection
- [ ] Image/icon optimization
- [ ] Baseline profiles (Android)

---

## Phase 15 — UX Polish (Month 9–10: Apr–May 2027)

- [ ] Compose animations for screen transitions
- [ ] Task completion animation
- [ ] Swipe-to-delete with undo
- [ ] Pull-to-refresh
- [ ] Accessibility: content descriptions
- [ ] Dark mode support
- [ ] Responsive layout for tablets

---

## Phase 16 — Security (Month 10: May 2027)

- [ ] Encrypted DataStore for sensitive preferences
- [ ] Secure network communication (TLS pinning)
- [ ] ProGuard/R8 configuration
- [ ] Secret management review
- [ ] Audit for API key exposure

---

## Phase 17 — Advanced Testing (Month 10–11: May–Jun 2027)

- [ ] Complete unit test coverage for domain layer
- [ ] Integration tests for repositories
- [ ] UI tests for all screens
- [ ] End-to-end test scenarios
- [ ] Performance benchmarks
- [ ] Screenshot tests

---

## Phase 18 — Observability (Month 11: Jun 2027)

- [ ] Structured logging system
- [ ] Crash reporting integration
- [ ] Performance monitoring
- [ ] Analytics events (opt-in)
- [ ] Debug logging panel (debug builds)

---

## Phase 19 — Production Hardening (Month 11–12: Jun–Jul 2027)

- [ ] Refactor technical debt items
- [ ] Dependency version upgrades
- [ ] API stability review
- [ ] Architecture documentation update
- [ ] Code review checklist
- [ ] Performance regression tests
- [ ] ProGuard rules validation

---

## Phase 20 — Release Preparation (Month 12: Jul–Aug 2027)

- [ ] Release build configuration
- [ ] Play Store metadata and screenshots
- [ ] App Store metadata
- [ ] Release CI/CD pipeline
- [ ] Version management strategy
- [ ] Final QA pass
- [ ] Public documentation update
- [ ] Release notes

---

## Milestones

| Milestone | Target Date | Description |
|-----------|-------------|-------------|
| M1 | Sep 2026 | Project compiles on Android + iOS |
| M2 | Oct 2026 | Domain and data layers complete |
| M3 | Nov 2026 | DI and networking wired up |
| M4 | Dec 2026 | Design system and navigation done |
| M5 | Jan 2027 | Home and task features working |
| M6 | Feb 2027 | Full MVP feature set |
| M7 | Apr 2027 | Offline-first behavior |
| M8 | Jun 2027 | Production quality tests |
| M9 | Aug 2027 | App Store / Play Store ready |

---

*This roadmap is a living document. The autonomous agent updates it after every development cycle.*
