from ultralytics import YOLO
from pathlib import Path


def main():
    base = Path(__file__).parent
    model = YOLO("yolov8n.pt")

    model.train(
        data=str(base / "datasets" / "Deportivo" / "data.yaml"),
        epochs=50,        # suficiente para una prueba
        imgsz=640,
        batch=8,          # si da error de memoria, baja a 4
        workers=2,
        device=0,         # usa tu GPU
        project=str(base / "runs"),
        name="deportivo",
    )


if __name__ == "__main__":
    main()