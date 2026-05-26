# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from typing import Optional

import bpy

from io_import_mage.format import *


def create_material(name: str) -> bpy.types.Material: pass


def import_nud(nud: NUDFile, mnt: Optional[MNTFile], mop: Optional[MOPFile | KFMFile], name: str,
               super_root: bpy.types.Object): pass
