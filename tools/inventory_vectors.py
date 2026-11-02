"""List every vector file under the given folders, read-only: features, CRS, bounds, fields, size and content hash.

    python tools/inventory_vectors.py <out.csv> <folder> [<folder> ...]
"""
import csv
import hashlib
import sys
from pathlib import Path

import pyogrio

EXT = {".shp", ".geojson", ".topojson", ".gpkg", ".kml"}


def main(out, *folders):
    rows = []
    for folder in folders:
        for p in sorted(Path(folder).rglob("*")):
            if not p.is_file() or p.suffix.lower() not in EXT or p.name.startswith("._"):
                continue
            row = dict(path=str(p), mb=round(p.stat().st_size / 1e6, 2), sha=hashlib.sha256(p.read_bytes()).hexdigest()[:16])
            try:
                i = pyogrio.read_info(p)
                b = i.get("total_bounds")
                row.update(n=i["features"], geom=i["geometry_type"], crs=(i["crs"] or "")[:24], bounds=None if b is None else [round(x, 2) for x in b], fields="|".join(i["fields"])[:300])
            except Exception as e:
                row.update(n="", geom="ERROR", crs="", bounds="", fields=str(e)[:80])
            rows.append(row)
    with open(out, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, ["path", "n", "geom", "crs", "bounds", "mb", "sha", "fields"])
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "vector files")


if __name__ == "__main__":
    main(*sys.argv[1:])
