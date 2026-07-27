"""Valida os rótulos YOLO e cria amostras com as caixas desenhadas."""

import csv
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_DIR = Path("/home/mauro/Projetos/fastcamp-dados-sinteticos")
DATASET_DIR = PROJECT_DIR / "data" / "processed" / "projeto_final_litterwatch"
PREVIEW_DIR = PROJECT_DIR / "outputs" / "projeto_final" / "anotacoes"


def ler_rotulo(caminho):
    partes = caminho.read_text(encoding="utf-8").strip().split()
    if len(partes) != 5:
        raise ValueError(f"Rótulo inválido: {caminho}")
    classe = int(partes[0])
    valores = tuple(float(valor) for valor in partes[1:])
    if classe != 0 or not all(0.0 <= valor <= 1.0 for valor in valores):
        raise ValueError(f"Valores fora do formato YOLO: {caminho}")
    if valores[2] <= 0 or valores[3] <= 0:
        raise ValueError(f"Caixa sem área: {caminho}")
    return valores


def desenhar_caixa(imagem_path, rotulo_path, destino, estado):
    imagem = Image.open(imagem_path).convert("RGB")
    largura, altura = imagem.size
    x, y, w, h = ler_rotulo(rotulo_path)
    x1 = (x - w / 2) * largura
    y1 = (y - h / 2) * altura
    x2 = (x + w / 2) * largura
    y2 = (y + h / 2) * altura
    desenho = ImageDraw.Draw(imagem)
    desenho.rectangle((x1, y1, x2, y2), outline=(255, 40, 40), width=3)
    desenho.text((x1 + 4, max(2, y1 - 14)), f"gato — {estado}", fill=(255, 255, 0))
    imagem.save(destino)


def main():
    imagens = sorted((DATASET_DIR / "images").glob("*/*.png"))
    rotulos = sorted((DATASET_DIR / "labels").glob("*/*.txt"))
    if len(imagens) != 60 or len(rotulos) != 60:
        raise ValueError("O dataset deve possuir 60 imagens e 60 rótulos.")

    stems_imagens = {(p.parent.name, p.stem) for p in imagens}
    stems_rotulos = {(p.parent.name, p.stem) for p in rotulos}
    if stems_imagens != stems_rotulos:
        raise ValueError("Há imagens ou rótulos sem par correspondente.")

    for rotulo in rotulos:
        ler_rotulo(rotulo)

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    with (DATASET_DIR / "metadata.csv").open(encoding="utf-8") as arquivo:
        registros = list(csv.DictReader(arquivo))

    for estado in ("dentro", "proximo", "fora"):
        registro = next(item for item in registros if item["estado"] == estado)
        split = registro["split"]
        nome = registro["arquivo"]
        desenhar_caixa(
            DATASET_DIR / "images" / split / f"{nome}.png",
            DATASET_DIR / "labels" / split / f"{nome}.txt",
            PREVIEW_DIR / f"exemplo_{estado}.png",
            estado,
        )

    print("Validação concluída: 60 pares corretos e 3 previews gerados.")


if __name__ == "__main__":
    main()
