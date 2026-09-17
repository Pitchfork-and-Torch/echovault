# GitHub-ready package

This ZIP is ready to push as a public repository that credits GrokForge and all contributors.

## Recommended metadata

- **Owner / org:** `Pitchfork-and-Torch` (or your own account)
- **Repo name:** `echovault-global-bioacoustic-archive-decoder`
- **Website / homepage:** https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder/ship
- **Topics:** `grokforge`, `forged-on-grokforge`, `public-goods`, `open-source`
- **Description:** Forged on GrokForge: EchoVault open bioacoustic archive kit (v0.1.0)

## Manual publish (any creator)

```bash
unzip echovault-global-bioacoustic-archive-decoder-*.zip -d echovault-global-bioacoustic-archive-decoder
cd echovault-global-bioacoustic-archive-decoder
git init
git add .
git commit -m "feat: sealed package from GrokForge"
# create empty public repo on GitHub, then:
git branch -M main
git remote add origin https://github.com/YOUR_ORG/echovault-global-bioacoustic-archive-decoder.git
git push -u origin main
```

Then set the repo **Website** field to the ship page and add topics above.

## Platform publish (founder/admin)

When `GITHUB_PUBLISH_TOKEN` is configured on GrokForge, founder/admin can
**Ship to GitHub** from the sealed ship page. That path creates/updates the org
repo, sets homepage + topics, and records a public ledger event.

## Required credits

Keep README.md, CONTRIBUTORS.md, LICENSE, and NOTICE. Do not strip "Forged on GrokForge".

Ship page: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder/ship
