#!/usr/bin/env python3
"""Fetch and validate 7Timer! astro seeing data for static GitHub Pages deployment."""
import json
from pathlib import Path
from urllib.request import Request, urlopen

API = "https://www.7timer.info/bin/api.pl?lon=17.35&lat=51.04&product=astro&output=json"
TARGET = Path("_site/seeing.json")


def main():
    req = Request(API, headers={"User-Agent": "AstronomicalWidget/2.0 (+https://github.com/soks/astronomicalwidget)", "Accept": "application/json"})
    try:
        with urlopen(req, timeout=25) as response:
            data = json.load(response)
        assert isinstance(data, dict) and len(str(data.get("init", ""))) == 10
        series = data.get("dataseries")
        assert isinstance(series, list) and len(series) > 0
        clean = []
        for row in series:
            try:
                tp = int(row["timepoint"])
                seeing = int(row["seeing"])
                if 0 <= tp <= 120 and 1 <= seeing <= 8:
                    clean.append({"timepoint": tp, "seeing": seeing})
            except (ValueError, TypeError, KeyError):
                continue
        assert clean, "No usable seeing data"
        result = {"init": str(data["init"]), "dataseries": clean}
        print(f"7Timer! OK: {len(clean)} points from {result['init']} UTC")
    except Exception as exc:
        # Cloud cover from Open-Meteo remains functional even if seeing service fails.
        print(f"7Timer! unavailable: {exc}")
        result = {"init": "", "dataseries": []}
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(result, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
