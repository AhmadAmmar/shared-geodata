"""Convert the source boundary files to clearly named GeoJSON in WGS 84, leaving the originals untouched.

Writes catalogue.csv with the original path, new path, features, area check and source. Rerun to rebuild.
"""
import csv
from pathlib import Path

import geopandas as gpd

R = Path(__file__).resolve().parent.parent
G = Path(r"D:\GIS")
GEE = Path.home() / "dev/gee-backup/ahmadammargeo/assets/data"
TP = Path.home() / "Downloads/thirdpole-20251027T200721Z-1-001/thirdpole"
V2 = Path.home() / "dev/uib-snow-cover/data/regions/tp_regions_v2.geojson"
A = G / "adm/Adminbdy Shapefile"
W = G / "pak_adm_wfp_20220909_shp"
O = G / "adm/pak_adm_ocha_pco_gaul_20181218_shp"
SRC_A = "Pakistan administrative boundary set, with my edits"
SRC_G = "My Earth Engine asset, with my edits"
SRC_T = "Own Third Pole domain, derived from DEM and slope in Earth Engine"

ITEMS = []
for level, name in ((0, "national"), (1, "provinces"), (2, "districts"), (3, "tehsils")):
    ITEMS.append((next(W.glob(f"pak_admbnda_adm{level}_*.shp")), f"pakistan/wfp_2022/pakistan_adm{level}_{name}_wfp_2022", "WFP, 2022-09-09"))
    ITEMS.append((next(O.glob(f"pak_admbnda_adm{level}_*.shp")), f"pakistan/ocha_2018/pakistan_adm{level}_{name}_ocha_2018", "OCHA, 2018-12-18"))
for f, n in (("National_Boundary", "national"), ("Provincial_Boundary", "provinces"), ("District_Boundary", "districts"), ("Tehsil_Boundary", "tehsils"), ("Union_Council", "union_councils"), ("National_Constituency_with_Projected_2010_Population", "national_constituencies_population_2010"), ("Provincial_Constituency", "provincial_constituencies")):
    ITEMS.append((A / f"{f}.shp", f"pakistan/admin_set/pakistan_{n}", SRC_A))
ITEMS += [
    (G / "adminbdy-shapefile/Lahore_District.shp", "pakistan/admin_set/lahore_district", SRC_A),
    (A / "Sindh.shp", "pakistan/admin_set/sindh_province", SRC_A),
    (next((G / "adm/Pakistan Shapefile with Kashmir").glob("*.shp")), "pakistan/edited/pakistan_national_with_kashmir", SRC_A),
    (GEE / "pk0.geojson", "pakistan/edited/pakistan_national_outline", SRC_G),
    (GEE / "pkTehsil.geojson", "pakistan/edited/pakistan_tehsils_408_units", SRC_G),
    (GEE / "AJKLULC__AJK.geojson", "pakistan/edited/azad_jammu_kashmir_outline", SRC_G),
    (next((p for p in G.glob("OSNI*/*.shp"))), "ireland_britain/northern_ireland_local_government_districts_2012", "OSNI Open Data"),
    (G / "British Isles/britisles.shp", "ireland_britain/british_isles_outline", "Own file"),
    (GEE / "tp_regions_v1.geojson", "third_pole/third_pole_regions_v1_all_levels", "Own; basins from HydroBASINS, countries from FAO GAUL"),
    (V2, "third_pole/third_pole_regions_v2", "Ranges and divisions from GMBA Mountain Inventory v2; sub-basins from HydroBASINS level 5"),
]
for f, n in (("strict", "strict"), ("balanced", "balanced"), ("balanced_contig", "balanced_contiguous"), ("expanded", "expanded"), ("exp_contiguous", "expanded_contiguous"), ("bal_convex_hull", "balanced_convex_hull"), ("elev_only_2000", "elevation_above_2000m")):
    ITEMS.append((TP / f"third_pole_{f}.shp", f"third_pole/domain_variants/third_pole_domain_{n}", SRC_T))


def main():
    rows = []
    for src, new, source in ITEMS:
        g = gpd.read_file(src)
        g = g.to_crs(4326) if g.crs and g.crs.to_epsg() != 4326 else g.set_crs(4326, allow_override=g.crs is None)
        out = R / "data" / f"{new}.geojson"
        out.parent.mkdir(parents=True, exist_ok=True)
        g.to_file(out, driver="GeoJSON", COORDINATE_PRECISION=6)
        back = gpd.read_file(out)
        assert len(back) == len(g), src
        rows.append(dict(file=f"data/{new}.geojson", features=len(g), mb=round(out.stat().st_size / 1e6, 2), source=source, original=str(src).replace(str(Path.home()), "~")))
    rows.append(dict(file="data/pakistan/geoboundaries_2019/pakistan_adm2_districts_geoboundaries_2019.geojson", features=126, mb="", source="geoBoundaries", original=r"D:\GIS\geoBoundariesPK2.geojson"))
    with open(R / "catalogue.csv", "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, ["file", "features", "mb", "source", "original"])
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "files;", round(sum(r["mb"] or 0 for r in rows), 1), "MB; largest", max(r["mb"] or 0 for r in rows))


if __name__ == "__main__":
    main()
