import onnx

model_path = "/home/pedro/Documents/mlops/24-2-mlops-project-car_object_detection/models/runs/detect/train3/weights/best.onnx"

model_onnx = onnx.load(model_path)

print(model_onnx.ir_version)