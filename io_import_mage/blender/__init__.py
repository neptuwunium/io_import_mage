# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import os

import bpy
import math
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, Context, Property, OperatorFileListElement, TOPBAR_MT_file_import
from bpy_extras.io_utils import ImportHelper

from .import_nud import import_nud
from ..format import *
from ..format.structs.enums import MageFileType


# noinspection PyPep8Naming
class _import_template(Operator, ImportHelper):
	bl_options = {'REGISTER', 'UNDO'}

	# noinspection PyTypeHints
	files: CollectionProperty(
		type=bpy.types.OperatorFileListElement,
		options={'HIDDEN', 'SKIP_SAVE'},
	)

	def load(self, path: str): pass

	@classmethod
	def poll(cls, _: Context):
		return True

	def draw(self, context: Context): pass

	def execute(self, _: Context):
		dirname = os.path.dirname(self.filepath)
		for file in self.files:
			# noinspection PyTypeChecker
			self.load(os.path.join(dirname, file.name))
		return {'FINISHED'}


# noinspection PyPep8Naming
class MAGE_Operator(_import_template):
	bl_idname = 'import_mesh.mage_mage'
	bl_label = 'Import MAGE Actor'

	# noinspection PyTypeHints
	filter_glob: StringProperty(default='*.mage', options={'HIDDEN'})

	def load(self, path):
		with open(path, 'rb') as file:
			with MageFile(file) as mage:
				nud_root = bpy.data.objects.new(mage.name or 'NUD', None)
				nud_root.rotation_euler = (math.pi / 2, 0, 0)
				bpy.context.collection.objects.link(nud_root)

				nud_count = mage.get_count(MageFileType.Mesh)
				mnt_count = mage.get_count(MageFileType.Node)

				shared_mnt = nud_count != mnt_count
				for index in range(mage.get_count(MageFileType.Mesh)):
					nud_file = NUDFile(mage.get_mesh(index))
					if not nud_file.valid: continue
					mnt_index = MNTFile.determine_mnt_index(index, nud_count, mnt_count)
					mnt_file = MNTFile(mage.get_node(mnt_index))
					with MOPFile(mage.get_motion(mnt_index)) as mop_file:
						import_nud(nud_file, mnt_file, mop_file, mage.name or 'NUD', nud_root, shared_mnt)


# noinspection PyPep8Naming
class NU_Operator(_import_template):
	bl_idname = 'import_mesh.mage_nu'
	bl_label = 'Import Big Endian Nu Mesh'

	# noinspection PyTypeHints
	filter_glob: StringProperty(default='*.nud', options={'HIDDEN'})

	def load(self, path):
		with open(path, 'rb') as file:
			nud_root = bpy.data.objects.new('NUD', None)
			nud_root.rotation_euler = (math.pi / 2, 0, 0)
			bpy.context.collection.objects.link(nud_root)
			import_nud(NUDFile(file), None, None, 'NUD', nud_root, False)


def mage_menu_import(self, _: Context):
	self.layout.operator(MAGE_Operator.bl_idname, text="MAGE Actor (.mage)")
	self.layout.operator(NU_Operator.bl_idname, text="Big Endian Nu Mesh (.nud)")


def register():
	bpy.utils.register_class(MAGE_Operator)
	bpy.utils.register_class(NU_Operator)
	bpy.types.TOPBAR_MT_file_import.append(mage_menu_import)


def unregister():
	bpy.utils.unregister_class(MAGE_Operator)
	bpy.utils.unregister_class(NU_Operator)
	bpy.types.TOPBAR_MT_file_import.remove(mage_menu_import)
