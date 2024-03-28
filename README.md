# ckanext-spatial-index-fix

This extensions comes to provide temprorary fixes to CKAN Spatial plugin that isn't yet applied, but will be (probably) applied soon.
Pull request to Spatial plugin: https://github.com/ckan/ckanext-spatial/pull/327

By default, all the fixes are disabled. Check the **List of fixes** and **Config settings**
section to understand how to disabled specific fix.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.7 and earlier | not tested    |
| 2.8             | not tested    |
| 2.9             | not tested    |
| 2.10.0          | yes           |

## Installation

Clone from GitHub, move to plugin directory and install using `pip install -e`.

Add `spatial_index_fix` to `ckan.plugins` to enable the plugin.
N.B. `spatial_index_fix` should be put before `spatial_metadata` and `spatial_query`.

## List of fixes
Use a fix name from the parentheses to enable it via `ckanext.spatial_index_fix.fixes`

1. Fix (`indexing`) dataset indexing process by catching TypeError , make dataset possible to index and present in list/searches.

2. (`update`) Deprecate Error message when user edit a DataSet with incorrect spatial data

## Config settings

	# Provide a list of fixes names to enable it
	ckanext.spatial_index_fix.fixes = indexing update

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
