import cv2
import mediapipe as mp
import numpy as np
import torch
import torch.nn as nn
import sys

class HandGestureDetector:
    def __init__(self):
        # Inicializar MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        if frame is None or frame.size == 0:
            raise ValueError("Frame inválido o vacío")
            
        # Convertir la imagen a RGB (MediaPipe requiere RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar el frame
        results = self.hands.process(rgb_frame)
        
        # Lista para almacenar los puntos de referencia de las manos
        hand_landmarks_list = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar los puntos de referencia en el frame
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Extraer coordenadas
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.append([landmark.x, landmark.y, landmark.z])
                hand_landmarks_list.append(landmarks)
                
        return frame, hand_landmarks_list

# Modelo simple de red neuronal para clasificación de gestos
class GestureClassifier(nn.Module):
    def __init__(self, input_size=63, num_classes=5):  # 21 puntos x 3 coordenadas = 63
        super(GestureClassifier, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.model(x)

class GestureRecognizer:
    def __init__(self, model_path="modelo_gestos.pth", num_classes=5):
        self.detector = HandGestureDetector()
        self.model = GestureClassifier(num_classes=num_classes)
        
        try:
            # Cargar el modelo entrenado
            if torch.cuda.is_available():
                self.model.load_state_dict(torch.load(model_path))
                self.device = torch.device('cuda')
            else:
                self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
                self.device = torch.device('cpu')
                
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            print(f"Error al cargar el modelo: {str(e)}")
            raise
        
        # Diccionario de gestos
        self.gestures = {
            0: 'puño',
            1: 'palma_abierta',
            2: 'paz',
            3: 'pulgar_arriba',
            4: 'señalar'
        }

    def predict_gesture(self, landmarks):
        if not landmarks:
            return None
            
        try:
            # Preparar datos para la predicción
            landmarks_flat = np.array(landmarks[0]).flatten()
            if landmarks_flat.shape[0] != 63:  # Validar dimensiones
                print(f"Error: Dimensiones incorrectas de landmarks: {landmarks_flat.shape[0]}")
                return None
                
            input_tensor = torch.FloatTensor(landmarks_flat).unsqueeze(0).to(self.device)
            
            # Realizar predicción
            with torch.no_grad():
                outputs = self.model(input_tensor)
                _, predicted = torch.max(outputs, 1)
                
            return self.gestures[predicted.item()]
        except Exception as e:
            print(f"Error en la predicción: {str(e)}")
            return None

    def run_recognition(self):
        # Inicializar la cámara
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo acceder a la cámara")
            return
            
        try:
            while True:
                ret, frame = cap.read()
                if not ret or frame is None:
                    print("Error: No se pudo leer el frame de la cámara")
                    break
                    
                try:
                    # Detectar manos y obtener landmarks
                    frame, hand_landmarks = self.detector.detect_hands(frame)
                    
                    # Predecir gesto si se detectan manos
                    if hand_landmarks:
                        gesture = self.predict_gesture(hand_landmarks)
                        if gesture:
                            # Mostrar predicción en el frame
                            cv2.putText(frame, f"Gesto: {gesture}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Mostrar frame
                    cv2.imshow('Reconocimiento de Gestos', frame)
                except Exception as e:
                    print(f"Error en el procesamiento del frame: {str(e)}")
                    continue
                
                # Salir con 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            cap.release()
            cv2.destroyAllWindows()

def main():
    try:
        recognizer = GestureRecognizer()
        print("Iniciando reconocimiento de gestos...")
        print("Presiona 'q' para salir")
        recognizer.run_recognition()
    except FileNotFoundError:
        print("Error: No se encontró el modelo entrenado.")
        print("Por favor, ejecute primero collect_data.py y luego train_model.py")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 