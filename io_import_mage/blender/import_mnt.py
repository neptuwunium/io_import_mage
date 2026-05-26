# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import bpy

from io_import_mage.format import KFMFile, MOPFile


def create_skeleton(mnt, kfm, root):
	if not (mnt and mnt.valid):
		return None, []

	if isinstance(kfm, MOPFile):
		kfm = kfm.load('basepose')

	assert isinstance(kfm, KFMFile)

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

		if kfm and kfm.valid:
			pass
		else:
			edit_bone.head = (0, 0, 0)
			edit_bone.tail = (0, 0, 0.1)
		bones.append(edit_bone.name)

		if node.header.parent_index != 0xffff:
			edit_bone.parent = armature.edit_bones[bones[node.header.parent_index]]

	if kfm:
		# prettify_bones
		pass

	bpy.ops.object.mode_set(mode='OBJECT')

	return blend_obj, bones
