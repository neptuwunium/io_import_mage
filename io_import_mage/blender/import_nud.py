# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import bpy
import math
import numpy as np

from io_import_mage.blender.import_mnt import create_skeleton
from io_import_mage.format.nud import NUDTriangleStream, NUDVertexStream
from io_import_mage.format.vertex_info import NUDVertexSkinType


def create_material(name):
	if name in bpy.data.materials:
		return bpy.data.materials[name]
	return bpy.data.materials.new(name=name)


def import_nud(nud, mnt, mop, name, super_root, shared):
	if not nud.valid: return

	(root, bones) = create_skeleton(mnt, mop, super_root, shared)
	if not root:
		root = super_root
	bone_count = len(bones)

	for obj in nud.objects:
		positions = []
		triangles = []
		uvs = {}
		colors = []
		normals = []
		weights = []
		joints = []
		material_indices = []
		groups = []
		vertex_offset = 0
		material_lookup = {}

		mesh = bpy.data.meshes.new(obj.name)
		blend_obj = bpy.data.objects.new(obj.name, mesh)
		blend_obj.parent = root

		has_weights = False
		for prim in obj.primitives:
			if prim.vertex_type.skin_type != NUDVertexSkinType.I0:
				has_weights = True
				break

		if has_weights:
			assert obj.header.mnt_index == 0xffff
			armature = blend_obj.modifiers.new('Armature', 'ARMATURE')
			armature.object = root
			for bone in bones:
				groups.append(blend_obj.vertex_groups.new(name=bone))
		elif obj.header.mnt_index < bone_count:
			blend_obj.parent_type = 'BONE'
			blend_obj.parent_bone = bones[obj.header.mnt_index]
			blend_obj.parent_bone_head_tail_factor = 0

		# todo: this blows up if the primitives aren't samey, check what values need to be zeroed
		for prim_idx, prim in enumerate(obj.primitives):
			vert = NUDVertexStream(nud, prim)
			tri = NUDTriangleStream(nud, prim)

			positions.append(vert.position)
			triangles.append(np.array(tri.triangles) + vertex_offset)

			if has_weights:
				weights.append(vert.weights)
				joints.append(vert.joints)

			primary_material = prim.materials[0]
			if primary_material is not None:
				material_name = f'{name}_{hex(primary_material.unique_id)}'
				if material_name in material_lookup:
					material_idx = material_lookup[material_name]
				else:
					material_idx = len(mesh.materials)
					material_lookup[material_name] = material_idx
					mesh.materials.append(create_material(material_name))
			else:
				material_name = f'{obj.name}_PRIM{prim_idx}'
				material_idx = len(mesh.materials)
				material_lookup[material_name] = material_idx
				mesh.materials.append(create_material(material_name))

			material_indices.append(np.full(len(tri.triangles), material_idx, dtype=np.int32))

			for uv_index in range(len(vert.uv)):
				if uv_index not in uvs:
					uvs[uv_index] = []
				uvs[uv_index].append(vert.uv[uv_index])

			if vert.color is not None:
				colors.append(vert.color)

			if vert.normal is not None:
				normals.append(vert.normal)

			vertex_offset += len(vert.position)

		positions_cat = np.concatenate(positions)
		triangles_cat = np.concatenate(triangles)

		mesh.from_pydata(positions_cat, [], triangles_cat, shade_flat=True)
		bpy.context.view_layer.active_layer_collection.collection.objects.link(blend_obj)

		if material_indices:
			mat_indices_cat = np.concatenate(material_indices)
			mesh.polygons.foreach_set('material_index', mat_indices_cat)

		loop_vert_indices = np.empty(len(mesh.loops), dtype=np.int32)
		mesh.loops.foreach_get('vertex_index', loop_vert_indices)

		for uv_index, uv_list in uvs.items():
			combined_uvs = np.concatenate(uv_list)
			loop_uvs = combined_uvs[loop_vert_indices]
			layer = mesh.uv_layers.new(name=f'TEXCOORD_{uv_index}')
			layer.uv.foreach_set('vector', loop_uvs.flatten())

		if colors:
			combined_colors = np.concatenate(colors)
			layer = mesh.color_attributes.new('Color', 'FLOAT_COLOR', 'POINT')
			layer.data.foreach_set('color', combined_colors.flatten())

		if weights and joints:
			weights = np.concatenate(weights)
			joints = np.concatenate(joints)

			for vertex_index in range(weights.shape[0]):
				for joint_index in range(weights.shape[1]):
					weight = float(weights[vertex_index, joint_index])
					if weight > 0.0:
						bone_index = int(joints[vertex_index, joint_index])
						groups[bone_index].add([vertex_index], weight, 'REPLACE')

		mesh.update()

		if normals:
			combined_normals = np.concatenate(normals)
			mesh.validate(clean_customdata=False)
			mesh.update(calc_edges=True)
			mesh.normals_split_custom_set_from_vertices(combined_normals.tolist())

	bpy.context.view_layer.update()


if __name__ == '__main__':
	import sys
	from io_import_mage.format import *
	from io_import_mage.format.structs.enums import MageFileType

	nud_root = bpy.data.objects.new("NUD", None)
	nud_root.rotation_euler = (math.pi / 2, 0, 0)
	bpy.context.collection.objects.link(nud_root)

	with open(sys.argv[-1], 'rb') as f:
		if sys.argv[-1].endswith('.mage'):
			with MageFile(f) as mage:
				nud_root.name = mage.name
				nud_count = mage.get_count(MageFileType.Mesh)
				mnt_count = mage.get_count(MageFileType.Node)
				mop_count = mage.get_count(MageFileType.Motion)

				shared_mnt = nud_count != mnt_count
				for index in range(mage.get_count(MageFileType.Mesh)):
					nud_file = NUDFile(mage.get_mesh(index))
					if not nud_file.valid: continue
					mnt_index = MNTFile.determine_mnt_index(index, nud_count, mnt_count)
					mnt_file = MNTFile(mage.get_node(mnt_index))
					with MOPFile(mage.get_motion(mnt_index)) as mop_file:
						import_nud(nud_file, mnt_file, mop_file, mage.name or 'nud', nud_root, shared_mnt)
		else:
			import_nud(NUDFile(f), None, None, 'nud', nud_root, False)
