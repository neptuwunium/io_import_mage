# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from typing import Optional

import bpy

from io_import_mage.format import *


def create_skeleton(mnt: Optional[MNTFile], mop: Optional[MOPFile | KFMFile], root: bpy.types.Object) \
		-> tuple[bpy.types.Object, list[str]]: pass
