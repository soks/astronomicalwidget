# Tonight's Sky v2 — Open-Meteo clouds + 7Timer! seeing

Minimal astronomical night forecast for an iframe in TablissNG. All presentation logic runs client-side, with no frontend dependencies.

## Design

- A **single, solid, dark, rounded card** at `rgba(9,15,27,0.70)` by default. No blur, glossy overlays, or gradients.
- Hourly cloud percentage from Open-Meteo and astronomical-night highlighting.
- Seeing from 7Timer! astro model (3-hour intervals) displayed as an **approximate representative category value** in arcseconds, never a precise measurement. Hover for the exact interval. `—` if unavailable.
- Width 202 px. Keep iframe at `width=204` and use `height=362` (adjust after checking Tabliss scaling).

## Deploy to existing soks/astronomicalwidget

1. Replace root `index.html`.
2. Add `scripts/fetch_seeing.py`.
3. Add `.github/workflows/deploy-widget.yml`.
4. Go to repository **Settings → Pages → Build and deployment → Source** and switch from **Deploy from a branch** to **GitHub Actions**. This is important: scheduled Actions deployments will publish the refreshed `seeing.json`. Do NOT keep branch mode.
5. Under **Actions**, choose **Update seeing and deploy widget → Run workflow** once. Check the build/deploy jobs; inspect `https://soks.github.io/astronomicalwidget/seeing.json` to confirm it has `init` and `dataseries`. The scheduled run repeats every 3 hours (with possible GitHub delays).
6. Put this into TablissNG Custom HTML:

```html
<iframe src="https://soks.github.io/astronomicalwidget/?opacity=0.7"
  width="204" height="362" scrolling="no"
  style="border:0;background:transparent;color-scheme:normal"></iframe>
```

`?step=1` shows 1-hour rows (increase iframe height). `?opacity=0.65` adjusts the single card's opacity; default is 0.7.

### Seeing interpretation

7Timer!'s categorical seeing index (1 best, 8 worst):

| Category | Seeing range | Short display |
| --- | --- | --- |
| 1 | <0.5″ | <0.5″ |
| 2 | 0.5–0.75″ | ~0.6″ |
| 3 | 0.75–1.0″ | ~0.9″ |
| 4 | 1.0–1.25″ | ~1.1″ |
| 5 | 1.25–1.5″ | ~1.4″ |
| 6 | 1.5–2.0″ | ~1.8″ |
| 7 | 2.0–2.5″ | ~2.3″ |
| 8 | >2.5″ | >2.5″ |

These approximate values are midpoints rounded to one decimal; not 7Timer!'s measured seeing, and not predictions of your PHD2 RMS or image FWHM. A forecast is aligned to its nearest 3-hour time slot; no interpolation to fabricate precision.

**Data:** https://open-meteo.com/ and https://www.7timer.info/doc.php?lang=en

### Failure modes

- If 7Timer! is down or the API payload is invalid, seeing displays `—`, while Open-Meteo cloud forecasts still work.
- Browser frontend cannot reliably fetch 7Timer! directly due to CORS. GitHub Actions fetches it server-side and deploys an ordinary static JSON file.
- Scheduled GitHub Actions runs may be delayed or disabled after prolonged repository inactivity. Manually run the workflow in that case.
- The GitHub Pages site has to use **GitHub Actions** as its publishing source for periodic JSON refresh to work. No PAT, external servers, or new browser extensions.
