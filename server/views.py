from django.shortcuts import render
from django.http import JsonResponse
from .models import tableEmpilhadeira
import base64
from io import BytesIO
from PIL import Image
import torch
import cv2
import tensorflow as tf
import numpy as np
from django.views.decorators.csrf import csrf_exempt
import json

# View existente para listar os dados
def listar_dados(request):
    dados = tableEmpilhadeira.objects.all().values()  # Retorna todos os registros da tabela
    return JsonResponse(list(dados), safe=False)

# Função auxiliar para realizar a inferência
def init_model(model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details

def non_max_suppression(boxes, scores, score_threshold, iou_threshold):
    indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold, iou_threshold)
    if len(indices) > 0:
        indices = indices.flatten()
    return indices

# Nova view para inferência com o modelo Torch
@csrf_exempt
def inferencia_model_ia(request):
    if request.method == 'POST':
        try:
            # Extrair a imagem codificada em base64 do corpo da requisição
            data = json.loads(request.body)
            img_data = data.get('image', '')
            
            if not img_data:
                return JsonResponse({'error': 'No image provided'}, status=400)
            
            # Decodificar a imagem
            img_data = base64.b64decode(img_data)
            img = Image.open(BytesIO(img_data))
            print(f"imagem decoficada")

            # Classes
            class_names = {0: 'Garfo Vazio'}
            print(f"classe carregada")

            # Convertendo a imagem para um array numpy
            frame = np.array(img)
            print(f"imagem convertida para numpy")

            # Inicializando o modelo
            model_path = r'C:\Users\Weliton\Desktop\Servidor WML\server_wml\best_float16.tflite'
            print(f"Modelo inicializado: {model_path}")
            interpreter, input_details, output_details = init_model(model_path)

            # Pré-processamento da imagem
            input_shape = input_details[0]['shape']
            input_tensor = cv2.resize(frame, (input_shape[2], input_shape[1]))
            input_tensor = np.expand_dims(input_tensor, axis=0)
            input_tensor = (input_tensor / 255.0).astype(np.float32)
            print(f"Pré processamento da imagem realizado")

            print(f"Iniciado processamento")
            interpreter.set_tensor(input_details[0]['index'], input_tensor)
            interpreter.invoke()

            output_data = interpreter.get_tensor(output_details[0]['index'])

            detection_threshold = 0.9
            iou_threshold = 0.9
            num_detections = output_data.shape[2]

            boxes = []
            confidences = []
            class_ids = []

            for i in range(num_detections):
                x, y, w, h, confidence = output_data[0, :, i]
                if confidence > detection_threshold:
                    xmin = int((x - w / 2) * frame.shape[1])
                    xmax = int((x + w / 2) * frame.shape[1])
                    ymin = int((y - h / 2) * frame.shape[0])
                    ymax = int((y + h / 2) * frame.shape[0])
                    boxes.append([xmin, ymin, xmax - xmin, ymax - ymin])
                    confidences.append(float(confidence))
                    class_ids.append(int(output_data[0, 0, i]))

            # Aplicando Non-Max Suppression para evitar múltiplas detecções do mesmo objeto
            if len(boxes) > 0:
                indices = non_max_suppression(boxes, confidences, detection_threshold, iou_threshold)

                detected_objects = []
                for i in indices:
                    box = boxes[i]
                    class_id = class_ids[i]
                    class_name = class_names.get(class_id, 'Desconhecida')
                    detected_objects.append({
                        'class': class_name,
                        'confidence': confidences[i],
                        'box': box
                    })
                print(f"Finalizado processamento")
                return JsonResponse({'detected_objects': detected_objects})
            else:
                print(f"message': 'No objects detected")
                return JsonResponse({'message': 'No objects detected'})

        except Exception as e:
            print(f"error': '{str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    print({'error': 'Invalid request method'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)