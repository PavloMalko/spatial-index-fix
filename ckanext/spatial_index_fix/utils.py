from __future__ import annotations

from enum import Enum, auto

import ckan.plugins.toolkit as tk


CONF_FIXES = "ckanext.spatial_index_fix.fixes"


def get_fixes() -> list[str]:
    return tk.aslist(tk.config.get(CONF_FIXES, []))

def is_fix_enabled(fix: Fixes) -> bool:
    return fix.name in get_fixes()

class Fixes(Enum):
    indexing = auto()
    update = auto()
