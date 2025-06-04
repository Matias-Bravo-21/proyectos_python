# Sistema de Reconocimiento de Gestos de Manos

Este proyecto implementa un sistema de reconocimiento de gestos de manos en tiempo real utilizando Python, MediaPipe y PyTorch.

## Requisitos

Asegúrate de tener instaladas todas las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

- `hand_detection.py`: Contiene la implementación principal del detector de manos y el clasificador de gestos
- `collect_data.py`: Script para recolectar datos de entrenamiento
- `train_model.py`: Script para entrenar el modelo de reconocimiento
- `requirements.txt`: Lista de dependencias del proyecto

## Gestos Soportados

El sistema puede reconocer 5 gestos diferentes:
1. Puño
2. Palma abierta
3. Paz (señal de victoria)
4. Pulgar arriba
5. Señalar

## Uso

### 1. Recolección de Datos

Para recolectar datos de entrenamiento, ejecuta:

```bash
python collect_data.py
```

Sigue las instrucciones en pantalla para capturar muestras de cada gesto. Para cada gesto:
- Presiona 'c' para capturar una muestra
- Presiona 'q' para terminar la captura del gesto actual
- El sistema guardará automáticamente las muestras

### 2. Entrenamiento del Modelo

Una vez que hayas recolectado suficientes datos, entrena el modelo con:

```bash
python train_model.py
```

El modelo entrenado se guardará como `modelo_gestos.pth`

### 3. Reconocimiento en Tiempo Real

Para iniciar el reconocimiento en tiempo real, ejecuta:

```bash
python hand_detection.py
```

- El sistema mostrará el gesto reconocido en tiempo real
- Presiona 'q' para salir

## Notas Importantes

- Asegúrate de tener una buena iluminación para mejor detección
- Mantén tu mano dentro del campo de visión de la cámara
- Realiza los gestos de manera clara y consistente
- Se recomienda recolectar al menos 50 muestras por gesto

## Solución de Problemas

1. Si la cámara no se inicia, verifica que esté correctamente conectada y que no esté siendo usada por otra aplicación
2. Si el reconocimiento no es preciso, considera:
   - Recolectar más datos de entrenamiento
   - Asegurar que los gestos sean consistentes durante la recolección de datos
   - Mejorar la iluminación
   - Ajustar la posición de la mano frente a la cámara 