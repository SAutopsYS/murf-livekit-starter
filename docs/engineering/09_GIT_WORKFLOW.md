# 09 — Git Workflow

How we change the hall without losing the thread.

---

## Branch strategy

| Branch | Role |
|---|---|
| `main` | Always runnable. Voice works. |
| `feat/<area>-<short>` | One milestone (e.g. `feat/brand-foundation`) |
| `fix/<area>-<short>` | Defect |
| `docs/<short>` | Documentation only |
| `hotfix/<short>` | Production break |

No long-lived personal branches that rewrite the kernel.  
Do not commit `scripts/node_modules` or `.env`.

## Commit convention

```
<type>(<scope>): <imperative why>

feat(brand): apply SALORA pulse and mark
fix(specialists): fail closed to host after one retry
docs(engineering): add frontend constitution
chore(ci): ...
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `sec`.  
Scopes: `voice`, `memory`, `specialists`, `tools`, `analytics`, `enterprise`, `brand`, `web`, `docs`.  
Why, not a file list.  
Never commit secrets.

## PR checklist

- [ ] App still talks (session path untouched or verified)  
- [ ] No second voice pipeline  
- [ ] No utterance field / log  
- [ ] Reused existing modules  
- [ ] Tests for forget / fail-closed / privacy if those paths moved  
- [ ] `uv run python -m pytest` if backend changed  
- [ ] `pnpm exec tsc --noEmit` if frontend changed  
- [ ] Constitution / engineering doc cited if the change is architectural  
- [ ] README updated only if operators need a new command  

## Review rules

Reviewers refuse: hover-only meaning, transcript-shaped columns, guest-of-guest, “tests later” on kernel, raw new palettes.  
Approval is not a like. See [04](04_FRONTEND_CONSTITUTION.md) and [05](05_BACKEND_CONSTITUTION.md) checklists.

## Release flow

1. `main` green  
2. Pin agent name, voice, and env as today  
3. Tag `vMAJOR.MINOR.PATCH` when we cut a named release  
4. Challenge days stay in README history; they are not version numbers  

## Hotfix strategy

Branch from `main`. Smallest diff. Still no utterance field.  
A hotfix that bypasses specialist recovery or forget is an incident, not a shortcut.  
Then PR back to `main`.

## Versioning

Semver for tagged releases.  
Guests and prompts pin independently of the git tag.  
“Latest model” is not a release.

User rule: do not commit unless asked. This file does not authorize drive-by commits.
