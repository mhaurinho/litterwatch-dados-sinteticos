"""Cria a cena-base do LitterWatch com gato e caixa de areia."""

from pathlib import Path
from math import radians

import bpy
from mathutils import Vector


PROJECT_DIR = Path("/home/mauro/Projetos/fastcamp-dados-sinteticos")
OUTPUT_DIR = PROJECT_DIR / "outputs" / "projeto_final"


def material(nome, cor, roughness=0.55):
    mat = bpy.data.materials.new(nome)
    mat.diffuse_color = (*cor, 1.0)
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (*cor, 1.0)
    principled.inputs["Roughness"].default_value = roughness
    return mat


def aplicar_material(objeto, mat):
    objeto.data.materials.append(mat)


def criar_cubo(nome, local, escala, mat, pai=None):
    bpy.ops.mesh.primitive_cube_add(location=local)
    obj = bpy.context.object
    obj.name = nome
    obj.scale = escala
    aplicar_material(obj, mat)
    obj.parent = pai
    bevel = obj.modifiers.new("Bordas", "BEVEL")
    bevel.width = 0.06
    bevel.segments = 2
    return obj


def criar_esfera(nome, local, escala, mat, pai=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=local)
    obj = bpy.context.object
    obj.name = nome
    obj.scale = escala
    aplicar_material(obj, mat)
    obj.parent = pai
    bpy.ops.object.shade_smooth()
    return obj


def criar_gato(mat_gato):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    gato = bpy.context.object
    gato.name = "Gato"

    partes = [
        criar_esfera("Gato_Corpo", (0, 0, 1.45), (0.65, 1.05, 0.72), mat_gato, gato),
        criar_esfera("Gato_Cabeca", (0, -0.9, 2.1), (0.55, 0.5, 0.52), mat_gato, gato),
        criar_esfera("Gato_Pata_FE", (-0.38, -0.62, 0.62), (0.2, 0.22, 0.65), mat_gato, gato),
        criar_esfera("Gato_Pata_FD", (0.38, -0.62, 0.62), (0.2, 0.22, 0.65), mat_gato, gato),
        criar_esfera("Gato_Pata_TE", (-0.42, 0.58, 0.62), (0.24, 0.28, 0.65), mat_gato, gato),
        criar_esfera("Gato_Pata_TD", (0.42, 0.58, 0.62), (0.24, 0.28, 0.65), mat_gato, gato),
    ]

    for nome, x in (("Gato_Orelha_E", -0.3), ("Gato_Orelha_D", 0.3)):
        bpy.ops.mesh.primitive_cone_add(
            vertices=3,
            radius1=0.24,
            radius2=0,
            depth=0.48,
            location=(x, -0.91, 2.62),
        )
        orelha = bpy.context.object
        orelha.name = nome
        aplicar_material(orelha, mat_gato)
        orelha.parent = gato
        partes.append(orelha)

    # Cauda formada por segmentos curvos para manter o modelo leve.
    for i in range(5):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.12 - i * 0.012,
            depth=0.58,
            location=(0.52 + i * 0.15, 0.78 + i * 0.18, 1.25 + i * 0.25),
            rotation=(radians(-32), radians(18 + i * 8), 0),
        )
        segmento = bpy.context.object
        segmento.name = f"Gato_Cauda_{i}"
        aplicar_material(segmento, mat_gato)
        segmento.parent = gato
        partes.append(segmento)

    return gato, partes


def criar_caixa(mat_caixa, mat_areia):
    caixa = []
    caixa.append(criar_cubo("Caixa_Base", (0, 0, 0.18), (2.25, 1.75, 0.18), mat_caixa))
    caixa.append(criar_cubo("Caixa_Frente", (0, -1.67, 0.58), (2.25, 0.1, 0.58), mat_caixa))
    caixa.append(criar_cubo("Caixa_Tras", (0, 1.67, 0.58), (2.25, 0.1, 0.58), mat_caixa))
    caixa.append(criar_cubo("Caixa_Esquerda", (-2.17, 0, 0.58), (0.1, 1.75, 0.58), mat_caixa))
    caixa.append(criar_cubo("Caixa_Direita", (2.17, 0, 0.58), (0.1, 1.75, 0.58), mat_caixa))
    criar_cubo("Areia", (0, 0, 0.42), (2.02, 1.5, 0.08), mat_areia)
    return caixa


def olhar_para(objeto, ponto):
    objeto.rotation_euler = (
        Vector(ponto) - objeto.location
    ).to_track_quat("-Z", "Y").to_euler()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    mat_gato = material("Pelo_Laranja", (0.72, 0.2, 0.04))
    mat_caixa = material("Caixa_Azul", (0.05, 0.28, 0.7))
    mat_areia = material("Areia_Bege", (0.58, 0.42, 0.22), 0.9)
    mat_piso = material("Piso", (0.16, 0.18, 0.21), 0.8)

    criar_caixa(mat_caixa, mat_areia)
    gato, partes = criar_gato(mat_gato)
    gato.location = (0, 0, 0.45)

    bpy.ops.mesh.primitive_plane_add(size=18, location=(0, 0, -0.02))
    aplicar_material(bpy.context.object, mat_piso)

    bpy.ops.object.light_add(type="AREA", location=(-4, -5, 8))
    luz = bpy.context.object
    luz.data.energy = 1200
    luz.data.size = 6

    bpy.ops.object.camera_add(location=(7.5, -9, 6.5))
    camera = bpy.context.object
    olhar_para(camera, (0, 0, 1.2))
    bpy.context.scene.camera = camera

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 3
    scene.render.resolution_x = 640
    scene.render.resolution_y = 480
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(OUTPUT_DIR / "cena_base.png")

    assert len(partes) == 13
    assert "Gato" in bpy.data.objects
    assert "Caixa_Base" in bpy.data.objects

    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_DIR / "cena_base.blend"))
    bpy.ops.render.render(write_still=True)
    print("Cena-base validada e renderizada.")


if __name__ == "__main__":
    main()
