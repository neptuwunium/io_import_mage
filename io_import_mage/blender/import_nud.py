# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import bpy
import numpy as np

from io_import_mage.format.nud import NUDFile, NUDTriangleStream, NUDVertexStream


def create_material(name: str) -> bpy.types.Material:
	if name in bpy.data.materials:
		return bpy.data.materials[name]
	return bpy.data.materials.new(name=name)

def import_nud(nud: NUDFile, name: str):
	root = bpy.data.objects.new(name, None)
	bpy.context.view_layer.active_layer_collection.collection.objects.link(root)

	for obj in nud.objects:
		positions = []
		triangles = []
		uvs = {}
		colors = []
		normals = []
		material_indices = []
		vertex_offset = 0
		material_lookup = {}

		mesh = bpy.data.meshes.new(obj.name)
		blend_obj = bpy.data.objects.new(obj.name, mesh)
		blend_obj.parent = root

		for prim_idx, prim in enumerate(obj.primitives):
			vert = NUDVertexStream(nud, prim)
			tri = NUDTriangleStream(nud, prim)

			positions.append(vert.position)
			triangles.append(np.array(tri.triangles) + vertex_offset)

			if prim.materials[0] is not None:
				material_name = f'{name}_{hex(prim.materials[0].unique_id)}'
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

			for index in range(len(vert.uv)):
				if index not in uvs:
					uvs[index] = []
				uvs[index].append(vert.uv[index])

			if vert.color is not None:
				colors.append(vert.color)

			if vert.normal is not None:
				normals.append(vert.normal)

			vertex_offset += len(vert.position)

		positions_cat = np.concatenate(positions)
		triangles_cat = np.concatenate(triangles)

		mesh.from_pydata(positions_cat, [], triangles_cat)
		bpy.context.view_layer.active_layer_collection.collection.objects.link(blend_obj)

		if material_indices:
			mat_indices_cat = np.concatenate(material_indices)
			mesh.polygons.foreach_set("material_index", mat_indices_cat)

		loop_vert_indices = np.empty(len(mesh.loops), dtype=np.int32)
		mesh.loops.foreach_get("vertex_index", loop_vert_indices)

		for index, uv_list in uvs.items():
			combined_uvs = np.concatenate(uv_list)
			loop_uvs = combined_uvs[loop_vert_indices]
			layer = mesh.uv_layers.new(name=f'TEXCOORD_{index}')
			layer.uv.foreach_set("vector", loop_uvs.flatten())

		if colors:
			combined_colors = np.concatenate(colors)
			layer = mesh.color_attributes.new("Color", 'FLOAT_COLOR', 'POINT')
			layer.data.foreach_set("color", combined_colors.flatten())

		mesh.update()

		if normals:
			combined_normals = np.concatenate(normals)
			mesh.validate(clean_customdata=False)
			mesh.update(calc_edges=True)
			mesh.normals_split_custom_set_from_vertices(combined_normals.tolist())

	bpy.context.view_layer.update()


if __name__ == '__main__':
	import sys

	with open(sys.argv[-1], 'rb') as f:
		if sys.argv[-1].endswith('.mage'):
			from io_import_mage.format.mage import MageFile

			mage = MageFile(f)
			nud_file = NUDFile(mage.get_mesh(0))
			import_nud(nud_file, mage.name or "nud")
		else:
			nud_file = NUDFile(f)
			import_nud(nud_file, "nud")
