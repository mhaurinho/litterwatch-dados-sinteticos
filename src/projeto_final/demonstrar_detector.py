"""Gera exemplos visuais do detector LitterWatch no conjunto de teste."""

from pathlib import Path

from ultralytics import YOLO


PROJECT_DIR = Path("/home/mauro/Projetos/fastcamp-dados-sinteticos")
RUNS_DIR = PROJECT_DIR / "outputs" / "projeto_final" / "yolo_runs"
MODELO = RUNS_DIR / "litterwatch_yolo26n" / "weights" / "best.pt"
IMAGENS = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "projeto_final_litterwatch"
    / "images"
    / "test"
)


def main():
    modelo = YOLO(MODELO)
    resultados = modelo.predict(
        source=str(IMAGENS),
        imgsz=320,
        conf=0.05,
        max_det=1,
        device="cpu",
        project=str(PROJECT_DIR / "outputs" / "projeto_final"),
        name="predicoes_teste",
        exist_ok=True,
        save=True,
        verbose=False,
    )
    detectadas = sum(bool(resultado.boxes) for resultado in resultados)
    print(f"Imagens analisadas: {len(resultados)}")
    print(f"Imagens com detecção: {detectadas}")


if __name__ == "__main__":
    main()
