from __future__ import annotations

from typing import Any
import json
import logging
import shapely.geometry
from geojson.codec import loads

from ckan import plugins
from ckan.types import Context

import ckanext.spatial_index_fix.utils as utils


log = logging.getLogger(__name__)
try:
    from shapely.errors import GeometryTypeError

    GeometryParseError = (GeometryTypeError, TypeError)
except ImportError:
    # Previous version of shapely uses ValueError and TypeError
    GeometryParseError = (ValueError, TypeError)

class SpatialIndexFixPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        return

    # IPackageController

    def after_update(self, context: Context, pkg_dict: dict[str, Any]) -> None:
        self.after_dataset_update(context, pkg_dict)

    def after_dataset_update(self, context: Context, pkg_dict: dict[str, Any]) -> None:
        if not utils.is_fix_enabled(utils.Fixes.update):
            return

        pkg_id = pkg_dict["id"]        
        geometry = pkg_dict.get("spatial")

        if geometry and not self.is_geometry_valid(pkg_id, geometry):
            pkg_dict.pop("spatial")

        # Check extras
        geometry = None
        for extra in pkg_dict.get("extras", []):
            if extra["key"] == "spatial":
                geometry = extra["value"]

        if geometry and not self.is_geometry_valid(pkg_id, geometry):
            pkg_dict["extras"] = filter(
                lambda extra: extra["key"] != "spatial",
                pkg_dict["extras"],
            )

    def before_dataset_index(self, pkg_dict: dict[str, Any]) -> dict[str, Any]:
        if not utils.is_fix_enabled(utils.Fixes.indexing):
            return pkg_dict
        
        pkg_id = pkg_dict["id"]
        if not pkg_dict.get("extras_spatial"):
            return pkg_dict

        geom_from_metadata = pkg_dict.get("spatial")
        if not geom_from_metadata:
            return pkg_dict

        try:
            geometry = json.loads(geom_from_metadata)
            if not geometry:
                return pkg_dict
        except Exception:
            log.exception(
                "Geometry not valid JSON, not indexing: %s :: %s", 
                pkg_id,
                geom_from_metadata[:100],
            )
            pkg_dict.pop("spatial")
            return pkg_dict

        try:
            shapely.geometry.shape(geometry)
        except Exception:
            log.exception("Not indexing: %s :: %s", pkg_id, json.dumps(geometry)[:100])
            pkg_dict.pop("spatial")
            return pkg_dict

        return pkg_dict

    def is_geometry_valid(self, pkg_id: str, geometry_str: Any) -> bool:
        try:
            geometry = loads(str(geometry_str))
        except ValueError:
            log.exception("Error decoding JSON object: %s", pkg_id)
            return False

        if not hasattr(geometry, "is_valid") or not geometry.is_valid:
            msg = f"Error: Wrong GeoJSON object in {pkg_id} "
            if hasattr(geometry, "errors"):
                msg = msg + f": {geometry.errors()}"
            log.error(msg)
            return False

        return True
