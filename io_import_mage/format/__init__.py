# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from io_import_mage.format.mage import MageFile # .MAGE, Mage Actor File
from io_import_mage.format.mnt import MNTFile # .MNT, Model Node Tree
from io_import_mage.format.nud import NUDFile # .NUD, NuData
# from io_import_mage.format.mop import MOPFile # .MOP, Motion Pack
# from io_import_mage.format.kfm import KFMFile # .KFM, Key Frame Motion


__all__ = ['MageFile', 'NUDFile', 'MNTFile']
