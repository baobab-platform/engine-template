# Platform L2 / L3 testing hooks

This scaffold is created from `baobab-platform/engine-template`. Before the
engine is lifecycle `active`, wire integrated testing as follows.

## Contract spine (Phase B)

1. Pin Shared contracts in `contracts.lock.yaml` (see
   `contracts.lock.yaml.example` and `baobab-platform/shared` EA-01).
2. Validate from a sibling `shared` checkout:

```bash
python3 ../shared/scripts/contract_lock.py check \
  --repository-root . \
  --shared-repo ../shared \
  --mode enforce
```

## L2 — dependency integration

Prefer the platform Compose topology from `baobab-platform/infrastructure`
(Postgres, RabbitMQ, Redis, APISIX) rather than inventing a second stack.

```bash
# After language stack is chosen, add Makefile targets modelled on baobab-cp:
#   INFRASTRUCTURE_DIR ?= ../infrastructure
#   make dev-up-infra   # start platform dependencies
#   make test-integration
```

Do **not** share database tables with other engines. Cross-engine facts move
by API or versioned events from `shared`.

## L3 — platform critical path

Infrastructure owns the L3 harness (`make platform-l3`). Optional probes:

| Variable | Purpose |
| --- | --- |
| `PLATFORM_CP_URL` | Control-plane readiness |
| `PLATFORM_IAM_URL` | OIDC discovery |
| `ENGINE_TEMPLATE_DIR` | This template (or derived engine) for hooks check |

When this engine exposes a health/ready URL, document it here so platform L3
can set `PLATFORM_*_URL` in CI or local runs.

## Checklist before first capability ships

- [ ] `contracts.lock.yaml` present and enforced in CI
- [ ] `make test` (L0) green without external deps
- [ ] `make test-integration` documented and runnable against infrastructure Compose
- [ ] No shared DB with other engines
