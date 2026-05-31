# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from typing import Optional

import bpy

from ..format import *


def get_trans(node: Optional[KFMNode]) -> tuple[float, float, float]: pass


def get_scale(node: Optional[KFMNode]) -> tuple[float, float, float]: pass


def get_rot(node: Optional[KFMNode]) -> tuple[float, float, float, float]: pass


def create_skeleton(mnt: Optional[MNTFile], kfm: Optional[MOPFile | KFMFile], root: bpy.types.Object,
                    shared: bool) -> tuple[bpy.types.Object, list[str]]: pass
