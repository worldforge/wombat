# Copyright (C) 2008 by Kai Blin
#
# WOMBAT is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA

def assetToJson(asset):
    """assetToJson(Asset) -> string
    Turn an asset into a string containing a JSON object.
    """
    return '{ path: "%s", name: "%s", size: %s }' % (asset.getPath(),
            asset.getName(), asset.getSize())

def assetListToJson(asset_list):
    """assetListToJson([Asset]) -> string
    Turn a list of assets into a JSON array
    """
    json = "["
    for asset in asset_list:
        json += assetToJson(asset)
        json += ","
    json.rstrip(",")
    json += "]"
    return json
