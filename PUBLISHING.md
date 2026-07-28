# Publishing OraCalm — a step-by-step release guide

Three destinations, in this order: **① GitHub → ② PyPI → ③ Zenodo (DOI)**. GitHub first (the code's home), PyPI whenever you like, and Zenodo last because it mints its DOI from a GitHub *Release*.

> **Credentials.** Your GitHub token and PyPI recovery codes live in `DentGit/0 Credentials/`. Use them yourself — never paste tokens into chat. Commits are already configured to use your GitHub **noreply** email (`273202244+Hezarani@users.noreply.github.com`) to avoid the GH007 privacy block.

Run everything from the repo folder:

```bash
cd ~/Desktop/Claude-Cowork/Projects/DentGit/oracalm
```

---

## 0 · Pre-flight (once)

```bash
python3 -m pytest -q            # expect: 43 passed
python3 -c "import oracalm; print(oracalm.__version__)"   # 0.1.0
ls README.md LICENSE CITATION.cff pyproject.toml paper.md .zenodo.json
ls assets/banner.png assets/social-preview.png docs/index.html
```

If the git folder still has stale lock files from the build sandbox, start clean (your Mac *can* delete them, unlike the sandbox):

```bash
rm -rf .git
git init -b main
git add -A
git commit -m "OraCalm v0.1.0 — open scoring for validated dental-anxiety instruments"
```

---

## ① Ship on GitHub

**1. Create the empty repo.** On <https://github.com/new>: owner **Hezarani**, name **`oracalm`**, visibility **Public**. Do **not** add a README, license, or .gitignore (you already have them).

**2. Push.**

```bash
git remote add origin https://github.com/Hezarani/oracalm.git
git push -u origin main
```

(If it asks for a password, use your Personal Access Token from `0 Credentials/`, not your account password.)

**3. Make the landing page look sharp + rank (design & SEO).**

- **About panel** (⚙️ next to *About*, top-right of the repo): set the description and topics.
  - Description: `Open, multilingual scoring for validated dental-anxiety instruments (MDAS, Corah DAS, MCDASf) — Python library, CLI & web demo.`
  - Website: your Pages URL (step 5) — `https://hezarani.github.io/oracalm/`
  - Topics: `dentistry` `dental-anxiety` `mdas` `corah-das` `mcdasf` `psychometrics` `screening` `oral-health` `python` `healthcare` `patient-reported-outcomes` `dental-phobia` `open-science`
- **Social preview image** (for good link cards on X/LinkedIn/Slack — this is the OpenGraph image): *Settings → General → Social preview → Edit → Upload* `assets/social-preview.png` (1280×640).
- The banner (`assets/banner.png`) already renders at the top of the README.

**4. (Optional but recommended) README badges.** The PyPI badge starts as *"not found"* and turns green automatically after step ②. The DOI badge stays grey until step ③.

**5. Turn on the live demo (GitHub Pages).** The demo is already duplicated to `docs/index.html` so Pages can serve it:

- *Settings → Pages → Build and deployment → Source: **Deploy from a branch** → Branch: **main** / **`/docs`** → Save.*
- Wait ~1 minute; your demo is live at **`https://hezarani.github.io/oracalm/`**. Put that URL in the About panel and it's already linked from the README.

**Verify:** open the repo — banner shows, topics show, demo link works.

---

## ② Publish to PyPI

**1. Install build tools** (once):

```bash
pip install --upgrade build twine
```

**2. Check the name is free:** visit <https://pypi.org/project/oracalm/>. If it 404s, the name is available. (If taken, change `name = "..."` in `pyproject.toml` and the import folder, then re-test.)

**3. Build the distributions:**

```bash
python3 -m build            # creates dist/oracalm-0.1.0.tar.gz and .whl
twine check dist/*          # metadata sanity check — expect PASSED
```

**4. Get a PyPI API token:** <https://pypi.org/manage/account/token/> → create a token (scope: "Entire account" for the first upload). Copy it (starts with `pypi-`).

**5. (Recommended) dry-run on TestPyPI first:**

```bash
twine upload -r testpypi dist/*
# username: __token__   password: <your TestPyPI token>
pip install -i https://test.pypi.org/simple/ oracalm     # smoke test
```

**6. Upload for real:**

```bash
twine upload dist/*
# username: __token__   password: <your PyPI token starting pypi->
```

**Verify:**

```bash
pip install oracalm
oracalm list
```

> **One-way door:** version **0.1.0 is permanent** on PyPI — you can't re-upload the same version. Any fix ships as **0.1.1** (bump `version` in `pyproject.toml` **and** `__version__` in `oracalm/__init__.py`, rebuild, re-upload).

---

## ③ Connect Zenodo + tag a Release → citable DOI

**1. Link Zenodo to GitHub** (once): sign in at <https://zenodo.org/> with GitHub → top-right menu → *GitHub* → find **`oracalm`** in your repo list → flip its toggle **ON**. (Zenodo now watches for new Releases.)

**2. Cut a GitHub Release:** on the repo → *Releases → Draft a new release* → *Choose a tag* → type **`v0.1.0`** → *Create new tag on publish* → Title `OraCalm v0.1.0` → paste a short note → **Publish release**.

Or from the terminal:

```bash
git tag v0.1.0 && git push origin v0.1.0
```

(then still click *Draft a new release* from that tag and Publish — Zenodo triggers on the *published Release*, not the raw tag).

**3. Zenodo archives it and mints two DOIs** automatically (a *concept* DOI that always points to the newest version, and a *version* DOI for v0.1.0). Find them on your Zenodo record.

**4. Wire the DOI back in:**

- Copy the DOI badge Markdown from the Zenodo record (the *concept* DOI is best for "cite the software").
- Replace the grey `DOI-pending` badge in `README.md` with it.
- Add the DOI to `CITATION.cff`:

  ```yaml
  identifiers:
    - type: doi
      value: 10.5281/zenodo.XXXXXXX      # your concept DOI
  ```
- Commit and push:

  ```bash
  git add README.md CITATION.cff
  git commit -m "docs: add Zenodo DOI"
  git push
  ```

`.zenodo.json` (already in the repo) pre-fills the archive's title, description, license, keywords, and your ORCID, so the record is clean the moment it's created.

**Verify:** the DOI link resolves to your Zenodo record; the README badge is live.

---

## Order & gotchas at a glance

| Step | Needs first | One-way? | Notes |
|------|-------------|----------|-------|
| GitHub push | clean git repo | no | fix & force-push freely early on |
| Pages demo | pushed `docs/` | no | source = branch `main`, folder `/docs` |
| Social preview + topics | repo exists | no | the SEO/design layer |
| PyPI upload | `python -m build` | **yes** (per version) | `__token__` + API token; 0.1.0 is permanent |
| Zenodo DOI | a **published GitHub Release** | mostly | link Zenodo *before* releasing |

That's the whole path from folder to a starred, pip-installable, citable research output.
