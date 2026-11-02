# Shared geodata

Boundary files that I reuse across projects, all in GeoJSON (WGS 84), free for others to use. Please credit the sources below.

![Maps of Third Pole ranges and sub-basins, and Pakistan's districts](img/preview.png)

`catalogue.csv` lists every file with its feature count, size and source.

## Pakistan

| Folder | Contents | Source |
|---|---|---|
| `data/pakistan/wfp_2022` | National, provinces, districts, tehsils, with P-codes | WFP, 2022-09-09 |
| `data/pakistan/ocha_2018` | National, provinces, districts, tehsils, with P-codes | OCHA, 2018-12-18 |
| `data/pakistan/geoboundaries_2019` | Districts | geoBoundaries |
| `data/pakistan/admin_set` | National to union council, constituencies, 2010 projected population | Administrative set, with my edits |
| `data/pakistan/edited` | National outlines, 408 tehsils, Azad Jammu and Kashmir outline | My edited versions |

The sets differ in how they treat Kashmir and in their number of units, so check that a set suits your purpose. Boundaries in disputed areas follow each source and imply no position on any claim.

## Third Pole

| File | Contents | Source |
|---|---|---|
| `data/third_pole/third_pole_regions_v2.geojson` | 6 ranges, 41 divisions, 180 sub-basins clipped to the mountains. Use this one. | GMBA Mountain Inventory v2; HydroBASINS level 5 |
| `data/third_pole/third_pole_regions_v1_all_levels.geojson` | Earlier rectangular ranges, basins, countries | My own; HydroBASINS; FAO GAUL |
| `data/third_pole/domain_variants` | Seven outlines of the whole domain, from strict to expanded | My own, from elevation and slope |

The mountain limits in version 2 leave out flat plateau interiors. Sub-basins named "Other" lie outside the named major basins.

## Ireland and Britain

Northern Ireland local government districts (OSNI Open Data, 2012) and a British Isles outline.

## Use

```python
import geopandas as gpd
base = "https://raw.githubusercontent.com/AhmadAmmar/shared-geodata/main/data"
regions = gpd.read_file(f"{base}/third_pole/third_pole_regions_v2.geojson")
karakoram = regions[(regions.level == "division") & (regions.parent == "Karakoram")]
```

`tools/build_catalogue.py` rebuilds the files from the originals. The Earth Engine scripts are in [earth-engine-code](https://github.com/AhmadAmmar/earth-engine-code).
