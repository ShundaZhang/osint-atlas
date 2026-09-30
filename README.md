# OSINT & GEO Atlas

An independent bilingual learning website for open-source intelligence and geographic analysis.

**Live:** https://shundazhang.github.io/osint-atlas/

Default English; EN / 中文 switches to the equivalent page. Language preference is shared with the other atlases on the same origin. Each lesson can be read without a third-party account.

## Contents

- OSINT foundations, search/collection, media verification, entity analysis and evidence preservation
- GEO workflow, visual clues, maps/OSM, satellite imagery, terrain, chronolocation and coordinate reference systems
- Alternative hypotheses, claim-specific source independence, reporting and AI assistance
- Three practical projects, a downloadable bilingual case notebook and three deterministic browser exercises
- Searchable original-resource directory, access notes and chapter-level source links

Figures, synthetic maps, course prose and exercise fixtures are original. No external map tiles or third-party images are mirrored. Exercises make no network requests and do not store exercise input. Only the selected language is saved locally.

## Build

Python 3, standard library only:

```sh
python3 -B build.py
python3 -B audit.py
python3 -m http.server 8770
```

Generated HTML and local assets are committed so GitHub Pages can publish directly from `main` at `/`. Use `index.html` for English, `index.zh.html` for Chinese. Generator sources are the source of truth; regenerate both languages after edits.

## Verification

`audit.py` checks bilingual counterparts, local links/anchors, duplicate IDs, one H1 per page, source references and static exercise wiring. `node check-labs.cjs` exercises real browser-script branches with synthetic DOM fixtures, including contradictions, source-lineage cases and coordinate-order failures. Browser review additionally covers language switching, search/category filtering and mobile overflow.

External resources and access notes reviewed on **1 October 2026**. A successful link check does not guarantee availability on every network or account. Services may change. The NOAA legacy calculator is marked as unmaintained; Copernicus Browser requires a free account; ExifTool links to the official repository as an alternative to blocked documentation.
