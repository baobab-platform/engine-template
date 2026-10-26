# DEV-14 — adopting the reusable engine integration framework

**Authority:** Accepted EA v2.3 and EA-DEV DEV-14; accepted specification
`shared/docs/architecture/ea-dev-reusable-engine-onboarding-2026-10-23.md`;
Shared profile contract established in #402, with the corrected Payments
startup registration in #403 at
`32b71f3335e566daeb58246f17fcbbf162cf7f53`.
The connected implementation is Infrastructure #64.

This template never issues an IAM identity, creates a CP Principal, grants a
Tenant, activates a CapabilityProvider, or certifies production readiness.

## Four separate input contracts

1. Activate `.baobab/environment.yaml` from the existing example. This
   declares exact toolchain requirements, not capabilities or runtime health.
2. Activate `.baobab/capability-provider.yaml` from the example. Declare only
   honestly supported canonical capability keys and current implementation
   evidence under ADR-SHARED-017. `IMPLEMENTED` is not `ACTIVE`.
3. Choose a Shared development synthetic enterprise scenario, such as the
   unrelated `external-client` with no DigitalEstate. The CP creates all
   canonical identifiers, legal-actor evaluations, grants and bindings.
4. Propose an engine-specific integration-run descriptor using
   `shared/contracts/development/v1/engine-integration-profile.schema.json`.
   Choose only needed IAM, CP, subject engine, and its native dependencies;
   CMS/BFF must not be included unless this particular engine requires them.

The descriptor lives under Shared's
`contracts/development/v1/examples/engines/`. Refer to `pulse-intelligence`
and `payments-sandbox` there for the approved shape; *do not copy their
provider keys, capability versions, client IDs, or tenant authority* into a
different engine. New IAM clients are reviewed and registered through Shared
and implemented by IAM, not minted in a template.

## Native owner adapter

Copy `.baobab/development_adapter.py.example` to
`.baobab/development_adapter.py` when you begin implementation. Every
phase intentionally returns `BLOCKED / OWNER_ADAPTER_NOT_IMPLEMENTED`.
The initial scaffold itself cannot pass onboarding or cause an engine to be
activated.

The connected controller invokes the following owner phases inside an
**unprivileged** container. The native engine remains in its own language;
Infrastructure supplies the bounded `engine_sdk.Driver` and private context.
No wrapper needs another IAM issuer/bootstrap or access to CP's database.

| Phase | Successful owner observation (only after actual execution) |
| --- | --- |
| `prepare` | `{"prepared": true}` after native migrations and reversible seeding |
| `test` | `{"cases": {...}}` containing every declared **owner** case and actual PASS/FAIL/BLOCKED reasons |
| `observe` | `{"effects": {...}, "resolutions": [...], "checks": {...}}` from native stores/reads for independent CP audit joins |
| `unavailable` | `{"observed": true}` after the native endpoint refuses while a real required process is stopped |
| `denied` | `{"observed": true}` after the native endpoint denies withdrawn/retired/disabled authority without effects |
| `restored` | `{"observed": true}` after a current authenticated native operation succeeds on recovery |

`case_updates` may accompany the last three observations for declared owner
cases. They cannot accept common ENG-ONB cases or erase a FAIL. A boolean from
an owner is insufficient: Infrastructure separately checks native runtime
identity, current CP resolution deltas, supported durable native audits and
actual issuer/host cleanup. Preserve unimplemented or unavailable domain cells
as BLOCKED; never substitute an empty report or component mock for execution.

Readiness uses the descriptor's actual HTTP readiness endpoint, not a successful
adapter exit. Component-only `readiness`, `migrate`, `seed`, `exercise` and
`cleanup` probes are retained for compatibility, separately from that connected
protocol. An owner may use them to:
- `readiness`: verify the real engine and required dependencies;
- `migrate`: execute the owner's native migrations against the owned store;
- `seed`: create reversible synthetic engine-domain records using CP-issued
  IDs and current authority, never mutate CP tables;
- `exercise`: run all required successful and denied native cases through
  normal endpoints and record actual effect/denial evidence;
- `cleanup`: reverse owned fixtures without altering other tenants or
  resources.

Infrastructure remains responsible for source/image pins, private network,
short-lived IAM credentials, actual CP authority/issuer readback, lease
watchdog, immutable redacted receipts and independently verified teardown.
The adapter must not gain a Docker socket, IAM issuer admin secret or CP
database credentials.

All results must identify source/actual execution separately. An adapter
returning code zero is not sufficient to qualify ENG-ONB-01..09: the common
harness observes native effects, negative cases and cleanup independently.

## Prior to proposing an adopted profile

- Lock current Shared and owner source revisions and OCI image digests.
- Validate the owner's capability provider declaration against Shared.
- Validate the new descriptor using the exact Shared validator.
- Provide bounded tests for positive and negative cases, including denied
  wrong audience, wrong Tenant and revoked authority.
- Keep unimplemented cases BLOCKED rather than skipped/PASS.
- Add current owner/runbook, explicit rollback and cleanup procedures.
- Run Actions and Codespaces with comparable receipts; retain different
  machine-environment classifications.
- Keep startup registration aligned with the owner declaration for providers
  already listed in Shared's startup bundle index. An omitted invocation clears
  the route during CP restart; provider metadata drift changes its version.
- Keep retry business bodies and idempotency keys stable when CP context headers
  refresh. A lost response can require replay of the same resource; it must not
  require another commercial or financial execution.
- Keep staging/production independent. Real Payments sandbox is still
  simulated money and cannot establish PSP qualification.

**Reusability test:** a third headless engine should need its own descriptor,
native dependencies and adapter, but no bespoke changes in IAM/CP bootstrap or
unrelated Nabhold CMS/BFF journeys. This is the DEV-14 exit criterion, not a
source-only template smoke test.

## Existing template workflow

The adapter example is checked by `dev14-template.yml` to confirm each phase
remains fail-closed. Once copied and implemented in a real engine repository,
delete the template-only workflow and implement genuine owner-domain CI.
