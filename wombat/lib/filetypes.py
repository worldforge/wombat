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

import os.path

img_inline = ['.gif', '.jpg', '.png']
image_exts = ['.bmp', '.gif', '.ico', '.jpg', '.png', '.psd',
        '.psp','.pspimage', '.psptube', '.raw', '.svg', '.tga', '.tif', '.xcf']
model_exts = ['.3dc', '.3ds', '.blend', '.caf', '.cal', '.cmf', '.crf', '.csf',
        '.dxf', '.emdl', '.lwo', '.max', '.md3', '.mdl', '.mesh', '.mtl',
        '.ndo', '.obj', '.skeleton', '.srf', '.texture', '.wings', '.wrl',
        '.xaf', '.xmf', '.xrl', '.xsf', '.xsi']
sound_exts = ['.mid', '.mp3', '.ogg', '.wav']
text_exts = ['.asm', '.bat', '.cfg', '.cg', '.conf', '.glsl', '.hlsl','.htm',
        '.html', '.ini', '.material', '.txt', '.url', '.xml']

def getType(name):
    """
    """
    base, ext = os.path.splitext(name)
    ext = ext.lower()

    if ext in image_exts:
        type = "image"
    elif ext in model_exts:
        type = "model"
    elif ext in sound_exts:
        type = "sound"
    elif ext in text_exts:
        type = "text"
    else:
        type = "other"

    return type

