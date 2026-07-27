"""Treina um detector pequeno para o MVP LitterWatch."""

from pathlib import Path

from ultralytics import YOLO


PROJECT_DIR = Path("/home/mauro/Projetos/fastcamp-dados-sinteticos")
DATASET_YAML = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "projeto_final_litterwatch"
    / "data.yaml"
)
RUNS_DIR = PROJECT_DIR / "outputs" / "projeto_final" / "yolo_runs"


def main():
    # Transfer learning com o menor modelo disponível para reduzir o custo em CPU.
    model = YOLO("yolo26n.pt")
    model.train(
        data=str(DATASET_YAML),
        epochs=8,
        imgsz=320,
        batch=2,
        device="cpu",
        workers=0,
        cache=False,
        project=str(RUNS_DIR),
        name="litterwatch_yolo26n",
        exist_ok=True,
        seed=20260727,
        deterministic=True,
        plots=True,
        verbose=False,
    )

    melhor = YOLO(RUNS_DIR / "litterwatch_yolo26n" / "weights" / "best.pt")
    melhor.val(
        data=str(DATASET_YAML),
        split="test",
        imgsz=320,
        batch=2,
        device="cpu",
        workers=0,
        project=str(RUNS_DIR),
        name="litterwatch_teste",
        plots=True,
    )


if __name__ == "__main__":
    main()
