import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
import os
import sys
from hand_detection import GestureClassifier

class GestureDataset(Dataset):
    def __init__(self, gestures, labels):
        if len(gestures) != len(labels):
            raise ValueError("El número de gestos y etiquetas no coincide")
        self.gestures = torch.FloatTensor(gestures)
        self.labels = torch.LongTensor(labels)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.gestures[idx], self.labels[idx]

def load_data(data_file):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            
        gestures = np.array(data['gestures'])
        labels = np.array(data['labels'])
        
        # Validar dimensiones de los datos
        if len(gestures) == 0 or len(labels) == 0:
            raise ValueError("Conjunto de datos vacío")
            
        if gestures.shape[1] != 63:  # 21 puntos x 3 coordenadas
            raise ValueError(f"Dimensiones incorrectas de los gestos: {gestures.shape}")
            
        # Validar etiquetas
        unique_labels = set(labels)
        if min(unique_labels) < 0 or max(unique_labels) > 4:
            raise ValueError(f"Etiquetas fuera de rango: {unique_labels}")
            
        return gestures, labels
        
    except json.JSONDecodeError:
        raise ValueError("Error al decodificar el archivo JSON")
    except Exception as e:
        raise Exception(f"Error al cargar los datos: {str(e)}")

def train_model(model, train_loader, num_epochs=100, learning_rate=0.001):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Mover modelo a GPU si está disponible
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    print(f"Iniciando entrenamiento en {device}...")
    best_accuracy = 0.0
    best_model_state = None
    
    try:
        for epoch in range(num_epochs):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0
            
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
            
            epoch_loss = running_loss / len(train_loader)
            accuracy = 100 * correct / total
            
            # Guardar el mejor modelo
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model_state = model.state_dict().copy()
            
            if (epoch + 1) % 10 == 0:
                print(f'Época [{epoch+1}/{num_epochs}], Pérdida: {epoch_loss:.4f}, Precisión: {accuracy:.2f}%')
        
        # Restaurar el mejor modelo
        model.load_state_dict(best_model_state)
        print(f"\nMejor precisión alcanzada: {best_accuracy:.2f}%")
        
    except Exception as e:
        print(f"Error durante el entrenamiento: {str(e)}")
        raise

def main():
    try:
        # Cargar datos
        data_file = "dataset/gesture_data.json"
        if not os.path.exists(data_file):
            print("Error: No se encontró el archivo de datos. Primero ejecute collect_data.py")
            return

        print("Cargando datos de entrenamiento...")
        gestures, labels = load_data(data_file)
        
        if len(gestures) < 50:  # Mínimo recomendado de muestras
            print(f"Advertencia: Conjunto de datos pequeño ({len(gestures)} muestras)")
            respuesta = input("¿Desea continuar? (s/n): ")
            if respuesta.lower() != 's':
                return

        # Crear dataset y dataloader
        print("Preparando datos para el entrenamiento...")
        dataset = GestureDataset(gestures, labels)
        train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

        # Crear y entrenar el modelo
        num_classes = len(set(labels))
        print(f"Creando modelo con {num_classes} clases...")
        model = GestureClassifier(input_size=63, num_classes=num_classes)
        
        train_model(model, train_loader)

        # Guardar el modelo
        model_path = "modelo_gestos.pth"
        torch.save(model.state_dict(), model_path)
        print(f"\nModelo guardado en {model_path}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 