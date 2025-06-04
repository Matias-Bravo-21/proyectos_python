import cv2
import mediapipe as mp
import numpy as np
import os
import json
import sys
from hand_detection import HandGestureDetector

class DataCollector:
    def __init__(self):
        try:
            self.detector = HandGestureDetector()
            self.data_dir = "dataset"
            self.gestures = {
                '0': 'puño',
                '1': 'palma_abierta',
                '2': 'paz',
                '3': 'pulgar_arriba',
                '4': 'señalar'
            }
            
            # Crear directorio de dataset si no existe
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
                
            # Crear o cargar el archivo de datos
            self.data_file = os.path.join(self.data_dir, "gesture_data.json")
            self.data = self.load_data()
            
        except Exception as e:
            print(f"Error al inicializar DataCollector: {str(e)}")
            raise

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                # Validar estructura del archivo
                if not isinstance(data, dict) or 'gestures' not in data or 'labels' not in data:
                    raise ValueError("Formato de archivo de datos inválido")
                return data
            return {"gestures": [], "labels": []}
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON. Creando nuevo archivo.")
            return {"gestures": [], "labels": []}
        except Exception as e:
            print(f"Error al cargar datos: {str(e)}")
            return {"gestures": [], "labels": []}

    def save_data(self):
        try:
            # Validar datos antes de guardar
            if not isinstance(self.data, dict) or 'gestures' not in self.data or 'labels' not in self.data:
                raise ValueError("Datos inválidos para guardar")
                
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f)
        except Exception as e:
            print(f"Error al guardar datos: {str(e)}")
            raise

    def validate_landmarks(self, landmarks):
        """Validar que los landmarks tengan el formato correcto"""
        if not landmarks or len(landmarks) == 0:
            return False
        
        landmarks_flat = np.array(landmarks[0]).flatten()
        return landmarks_flat.shape[0] == 63  # 21 puntos x 3 coordenadas

    def collect_samples(self, gesture_id, num_samples=50):
        if gesture_id not in self.gestures:
            print(f"Gesto no válido. Opciones disponibles: {self.gestures}")
            return

        print(f"Recolectando muestras para el gesto: {self.gestures[gesture_id]}")
        print("Presiona 'c' para capturar una muestra, 'q' para terminar")

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo acceder a la cámara")
            return
            
        samples_collected = 0
        invalid_samples = 0
        max_invalid_samples = 10

        try:
            while samples_collected < num_samples:
                ret, frame = cap.read()
                if not ret or frame is None:
                    print("Error: No se pudo leer el frame de la cámara")
                    break

                try:
                    # Detectar manos
                    frame, hand_landmarks = self.detector.detect_hands(frame)

                    # Mostrar información en el frame
                    cv2.putText(frame, f"Gesto: {self.gestures[gesture_id]}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Muestras: {samples_collected}/{num_samples}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    if not hand_landmarks:
                        cv2.putText(frame, "No se detectan manos", (10, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            
                    cv2.imshow('Recolección de Datos', frame)
                    key = cv2.waitKey(1)

                    if key == ord('q'):
                        break
                    elif key == ord('c'):
                        if hand_landmarks and self.validate_landmarks(hand_landmarks):
                            # Guardar los datos de los landmarks
                            landmarks_flat = np.array(hand_landmarks[0]).flatten().tolist()
                            self.data["gestures"].append(landmarks_flat)
                            self.data["labels"].append(int(gesture_id))
                            samples_collected += 1
                            print(f"Muestra {samples_collected} capturada")
                            invalid_samples = 0  # Resetear contador de muestras inválidas
                        else:
                            invalid_samples += 1
                            print("Muestra inválida: No se detectaron manos correctamente")
                            if invalid_samples >= max_invalid_samples:
                                print("\nDemasiados intentos fallidos. Asegúrate de que:")
                                print("1. Tu mano esté visible en la cámara")
                                print("2. La iluminación sea adecuada")
                                print("3. Estés realizando el gesto correctamente")
                                if input("\n¿Deseas continuar? (s/n): ").lower() != 's':
                                    break
                                invalid_samples = 0

                except Exception as e:
                    print(f"Error en el procesamiento del frame: {str(e)}")
                    continue

        finally:
            cap.release()
            cv2.destroyAllWindows()
            
        if samples_collected > 0:
            try:
                self.save_data()
                print(f"\nRecolección completada. {samples_collected} muestras guardadas.")
            except Exception as e:
                print(f"Error al guardar los datos: {str(e)}")
        else:
            print("\nNo se recolectaron muestras.")

def main():
    try:
        collector = DataCollector()
        print("Sistema de recolección de datos para gestos de manos")
        print("\nGestos disponibles:")
        for key, value in collector.gestures.items():
            print(f"{key}: {value}")

        while True:
            gesture_id = input("\nIngrese el número del gesto a recolectar (o 'q' para salir): ")
            if gesture_id.lower() == 'q':
                break
            
            if gesture_id in collector.gestures:
                collector.collect_samples(gesture_id)
            else:
                print("Gesto no válido")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 