"""Gera o dataset sintético YOLO do projeto LitterWatch."""

from __future__ import annotations

import csv
import random
import sys
from pathlib import Path
from math import radians

import bpy
from bpy_extras.object_utils import world_to_camera_view


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import cena_base as base  # noqa: E402


PROJECT_DIR = Path("/home/mauro/Projetos/fastcamp-dados-sinteticos")
DATASET_DIR = PROJECT_DIR / "data" / "processed" / "projeto_final_litterwatch"
SEED = 20260727
SPLITS = {"train": 48, "val": 6, "test": 6}
TOTAL = sum(SPLITS.values())
CLASS_ID = 0
CLASS_NAME = "gato"


def preparar_pastas():
    for split in SPLITS:
        (DATASET_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
        (DATASET_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)


def plano_splits():
    plano = [split for split, quantidade in SPLITS.items() for _ in range(quantidade)]
    random.Random(SEED + 1).shuffle(plano)
    return plano


def caixa_yolo_composta(scene, camera, objetos):
    pontos = []
    for objeto in objetos:
        for canto in objeto.bound_box:
            coordenada = world_to_camera_view(
                scene, camera, objeto.matrix_world @ base.Vector(canto)
            )
            pontos.append((coordenada.x, coordenada.y))

    x_min = max(0.0, min(x for x, _ in pontos))
    x_max = min(1.0, max(x for x, _ in pontos))
    y_min = max(0.0, min(y for _, y in pontos))
    y_max = min(1.0, max(y for _, y in pontos))

    largura = x_max - x_min
    altura = y_max - y_min
    if largura <= 0 or altura <= 0:
        raise ValueError("O gato ficou fora do enquadramento da câmera.")

    x_centro = (x_min + x_max) / 2
    # Blender mede Y de baixo para cima; YOLO mede de cima para baixo.
    y_centro = 1.0 - ((y_min + y_max) / 2)
    return x_centro, y_centro, largura, altura


def sortear_posicao(estado):
    if estado == "dentro":
        return (random.uniform(-0.8, 0.8), random.uniform(-0.45, 0.45), 0.45)
    if estado == "proximo":
        lado = random.choice((-1, 1))
        return (lado * random.uniform(2.7, 3.3), random.uniform(-1.2, 1.2), 0.0)
    lado = random.choice((-1, 1))
    return (lado * random.uniform(3.5, 4.3), random.uniform(-2.0, 2.0), 0.0)


def alterar_cor_gato(material):
    cores = [
        (0.72, 0.2, 0.04, 1.0),
        (0.08, 0.08, 0.09, 1.0),
        (0.55, 0.52, 0.48, 1.0),
        (0.82, 0.76, 0.62, 1.0),
        (0.3, 0.16, 0.08, 1.0),
    ]
    cor = random.choice(cores)
    material.diffuse_color = cor
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = cor
    return cor[:3]


def configurar_cena():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    mat_gato = base.material("Pelo_Gato", (0.72, 0.2, 0.04))
    mat_caixa = base.material("Caixa", (0.05, 0.28, 0.7))
    mat_areia = base.material("Areia", (0.58, 0.42, 0.22), 0.9)
    mat_piso = base.material("Piso", (0.16, 0.18, 0.21), 0.8)
    base.criar_caixa(mat_caixa, mat_areia)
    gato, partes = base.criar_gato(mat_gato)

    bpy.ops.mesh.primitive_plane_add(size=22, location=(0, 0, -0.02))
    base.aplicar_material(bpy.context.object, mat_piso)

    bpy.ops.object.light_add(type="AREA", location=(-4, -5, 8))
    luz = bpy.context.object
    luz.data.size = 6

    bpy.ops.object.camera_add(location=(9.5, -12, 8.2))
    camera = bpy.context.object
    camera.data.lens = 43
    base.olhar_para(camera, (0, 0, 1.0))
    bpy.context.scene.camera = camera

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 3
    scene.render.resolution_x = 320
    scene.render.resolution_y = 320
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    return scene, gato, partes, camera, luz, mat_gato


def escrever_yaml():
    conteudo = (
        f"path: {DATASET_DIR}\n"
        "train: images/train\n"
        "val: images/val\n"
        "test: images/test\n"
        "names:\n"
        f"  {CLASS_ID}: {CLASS_NAME}\n"
    )
    (DATASET_DIR / "data.yaml").write_text(conteudo, encoding="utf-8")


def main():
    random.seed(SEED)
    preparar_pastas()
    scene, gato, partes, camera, luz, mat_gato = configurar_cena()
    splits = plano_splits()
    estados = ["dentro", "proximo", "fora"] * (TOTAL // 3)
    random.shuffle(estados)
    registros = []

    for indice, (split, estado) in enumerate(zip(splits, estados)):
        gato.location = sortear_posicao(estado)
        gato.rotation_euler[2] = radians(random.uniform(0, 360))
        luz.data.energy = random.uniform(650, 1300)
        luz.location.x = random.uniform(-5, 5)
        cor = alterar_cor_gato(mat_gato)
        camera.location.z = random.uniform(7.5, 9.0)
        base.olhar_para(camera, (0, 0, 1.0))
        bpy.context.view_layer.update()

        bbox = caixa_yolo_composta(scene, camera, partes)
        nome = f"litterwatch_{indice:03d}"
        imagem = DATASET_DIR / "images" / split / f"{nome}.png"
        rotulo = DATASET_DIR / "labels" / split / f"{nome}.txt"
        scene.render.filepath = str(imagem)
        bpy.ops.render.render(write_still=True)
        rotulo.write_text(
            f"{CLASS_ID} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n",
            encoding="utf-8",
        )
        registros.append(
            {
                "arquivo": nome,
                "split": split,
                "estado": estado,
                "gato_x": round(gato.location.x, 4),
                "gato_y": round(gato.location.y, 4),
                "rotacao_z": round(gato.rotation_euler[2], 4),
                "cor_r": cor[0],
                "cor_g": cor[1],
                "cor_b": cor[2],
                "bbox_x": round(bbox[0], 6),
                "bbox_y": round(bbox[1], 6),
                "bbox_w": round(bbox[2], 6),
                "bbox_h": round(bbox[3], 6),
            }
        )
        print(f"[{indice + 1:02d}/{TOTAL}] {split} — {estado}")

    with (DATASET_DIR / "metadata.csv").open("w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=registros[0].keys())
        escritor.writeheader()
        escritor.writerows(registros)

    escrever_yaml()
    bpy.ops.wm.save_as_mainfile(filepath=str(DATASET_DIR / "litterwatch.blend"))
    print(f"Dataset concluído: {DATASET_DIR}")


if __name__ == "__main__":
    main()
