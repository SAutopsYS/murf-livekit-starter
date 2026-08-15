# Scripts

Local CI wrappers. Same checks as `.github/workflows/ci.yml` minus the privacy grep job.

```bash
./scripts/ci.sh
```

```powershell
.\scripts\ci.ps1
```

Do not add a product Playwright suite here. E2E is planned in [41 SALORA OS v1](../docs/engineering/41_SALORA_OS_V1_RELEASE.md), not implemented.
