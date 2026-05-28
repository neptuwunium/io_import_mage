# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from .kfm import KFMFile  # .KFM, Key Frame Motion
from .mage import MageFile  # .MAGE, Mage Actor File
from .mnt import MNTFile  # .MNT, Model Node Tree
from .mop import MOPFile  # .MOP, Motion Pack
from .nud import NUDFile  # .NUD, NuData

__all__ = ['MageFile', 'NUDFile', 'MNTFile', 'MOPFile', 'KFMFile']
