# Integrating the SEO System into a Client Template

## 1. Copy the system

Place the `seo-system/` folder in the client repository root.

## 2. Create the client configuration

Copy:

```text
seo-system/client-seo.config.example.json
```

to:

```text
client-seo.config.json
```

Then complete the approved business facts. Use `industry-schema-map.json` to select the industry default.

## 3. Generate the package

```bash
python seo-system/scripts/build_seo.py --config client-seo.config.json --output seo-output
```

Do not use `--production` until every approval field is complete.

## 4. Integrate generated assets

- Insert `seo-output/head-seo.html` into the final homepage `<head>`.
- Copy `robots.txt`, `sitemap.xml`, and `manifest.webmanifest` to the deployed site root.
- Confirm the JSON-LD describes only visible, truthful content.
- Keep the client’s final domain consistent everywhere.

## 5. Run the production gate

```bash
python seo-system/scripts/build_seo.py --config client-seo.config.json --output seo-output --production

python seo-system/scripts/audit_seo.py --config client-seo.config.json --site-dir site --production --report seo-output/prelaunch-audit.md
```

## 6. Install GitHub automation

Copy:

```text
seo-system/workflows/seo-quality-gate.yml
```

to:

```text
.github/workflows/seo-quality-gate.yml
```

After launch, also copy `monthly-seo-watch.yml` and confirm the configuration points to the real production website.

## 7. Preserve evidence

Retain the approved config, audit, Search Console launch record, PageSpeed baseline, and client approval in the client project.
