#!/usr/bin/env python3
"""Fetch optional CC0 assets for MechSim. Standard library only; no API key.
Run from any directory: python tools/fetch_cc0_assets.py
Review upstream licensing and attribution in assets/README.md.
"""
import io, json, pathlib, urllib.request, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]/"assets"/"cc0"
ROOT.mkdir(parents=True,exist_ok=True)
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"MechSimAssetPreparation/1.0"})
    with urllib.request.urlopen(req,timeout=60) as res:
        return res.read()
def save(name,data):
    if not data: raise ValueError("Empty asset "+name)
    (ROOT/name).write_bytes(data)
    print(name,len(data),"bytes")
def poly(asset,kind,fmt,name):
    try:
        files=json.loads(fetch("https://api.polyhaven.com/files/"+asset))
        url=files[kind]["1k"][fmt]["url"]
    except Exception:
        url=("https://dl.polyhaven.org/file/ph-assets/Textures/jpg/1k/rocky_terrain/rocky_terrain_diff_1k.jpg" if kind=="diff" else "https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/rocky_ridge/rocky_ridge_1k.hdr")
    save(name,fetch(url))
errors=[]
for args in [("rocky_terrain","diff","jpg","rock.jpg"),("rocky_ridge","hdri","hdr","sky.hdr")]:
    try: poly(*args)
    except Exception as exc: errors.append(str(exc))
try:
    archive=zipfile.ZipFile(io.BytesIO(fetch("https://ambientcg.com/get?file=Metal032_1K-JPG.zip")))
    for suffix,out in [("Color.jpg","metal-color.jpg"),("NormalGL.jpg","metal-normal.jpg"),("Roughness.jpg","metal-roughness.jpg")]:
        name=next(n for n in archive.namelist() if n.lower().endswith(suffix.lower()))
        save(out,archive.read(name))
except Exception as exc: errors.append(str(exc))
if errors:
    print("Some downloads failed. The game will use its procedural fallback textures.")
    for err in errors: print(err)
    raise SystemExit(1)
