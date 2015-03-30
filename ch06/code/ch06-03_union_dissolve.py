#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shapely.geometry import MultiPolygon
from shapely.ops import cascaded_union
from utils import create_shapes
from utils import out_geoj

# input NOAA Shapefile
shp = "../geodata/temp-all-warn-week.shp"

# output union_dissolve results as GeoJSON
out_geojson_file = "../geodata/results_union_dissolve.geojson"


def check_geom(in_geom):
    """
    :param in_geom: input valid Shapely geometry objects
    :return: Shapely MultiPolygon cleaned
    """
    plys = []
    for g in in_geom:
        # if geometry is NOT valid
        if not g.is_valid:
            print "Oh no invalid geometry"
            # clean polygon with buffer 0 distance trick
            new_ply = g.buffer(0)
            print "now lets make it valid"
            # add new geometry to list
            plys.append(new_ply)
        else:
            # add valid geometry to list
            plys.append(g)
    # convert new polygons into a new MultiPolygon
    out_new_valid_multi = MultiPolygon(plys)
    return out_new_valid_multi

# input Shapefile and convert to Shapely geometries
shply_geom = create_shapes(shp)

# Check the Shapely geometries if they are valid if not fix them
new_valid_geom = check_geom(shply_geom)

# run our union with dissolve
dissolve_result = cascaded_union(new_valid_geom)

# output the resulting union dissolved polygons to GeoJSON file
out_geoj(dissolve_result, out_geojson_file)

