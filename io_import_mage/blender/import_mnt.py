# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from typing import Optional

import bpy
import mathutils

from io_import_mage.format import MOPFile
from io_import_mage.format.kfm import KFMNode
from io_import_mage.format.structs.enums import KFMChannelTarget


def get_trans(node: Optional[KFMNode]) -> tuple[float, float, float]:
	if not node or len(node.values) == 0:
		return 0, 0, 0

	# noinspection PyTypeChecker
	return tuple(node.values[0])


def get_scale(node: Optional[KFMNode]) -> tuple[float, float, float]:
	if not node or len(node.values) == 0:
		return 1, 1, 1

	# noinspection PyTypeChecker
	return tuple(node.values[0])


def get_rot(node: Optional[KFMNode]) -> tuple[float, float, float, float]:
	if not node or len(node.values) == 0:
		return 1, 0, 0, 0

	# noinspection PyTypeChecker
	return node.values[0][3], node.values[0][0], node.values[0][1], node.values[0][2]


def create_skeleton(mnt, kfm, root, shared):
	if not (mnt and mnt.valid):
		return None, []

	if shared:
		blend_obj = bpy.data.objects.get(mnt.nodes[0].name)
		if blend_obj and 'mage_bones' in blend_obj:
			return blend_obj, blend_obj['mage_bones']

	if isinstance(kfm, MOPFile):
		kfm = kfm.load('basepose')

	armature = bpy.data.armatures.new(mnt.nodes[0].name)
	blend_obj = bpy.data.objects.new(mnt.nodes[0].name, armature)
	blend_obj.parent = root
	bpy.context.collection.objects.link(blend_obj)

	bpy.context.view_layer.objects.active = blend_obj
	blend_obj.select_set(True)
	bpy.ops.object.mode_set(mode='EDIT')

	bones = []

	for node in mnt.nodes:
		edit_bone = armature.edit_bones.new(node.name)

		edit_bone.head = (0, 0, 0)
		edit_bone.tail = (0, 1, 0)

		if kfm and kfm.valid and node.header.index in kfm.nodes:
			kfm_node = kfm.nodes[node.header.index]
			node_trans = get_trans(kfm_node.get(KFMChannelTarget.Translation))
			node_rot = get_rot(kfm_node.get(KFMChannelTarget.Rotation))
			node_scale = get_scale(kfm_node.get(KFMChannelTarget.Scale))

			loc = mathutils.Vector(node_trans)
			rot = mathutils.Quaternion(node_rot)
			scale = mathutils.Vector(node_scale)

			edit_bone.matrix = mathutils.Matrix.LocRotScale(loc, rot, scale)

		bones.append(edit_bone.name)

		if node.header.parent_index != 0xffff:
			edit_bone.parent = armature.edit_bones[bones[node.header.parent_index]]

	bpy.ops.object.mode_set(mode='OBJECT')
	blend_obj["mage_bones"] = bones

	return blend_obj, bones
