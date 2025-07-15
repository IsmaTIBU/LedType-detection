> A tener en cuenta: Este proyecto fue desarrollado para una aplicación industrial específica que involucra detección de LEDs. El código sirve como ejemplo educativo de técnicas de detección de formas con OpenCV y puede requerir ajustes de parámetros para diferentes casos de uso.

<table>
<tr>
<td><img src="images/squaredLed.jpg" alt="Led Cuadrado" width="300"/></td>
<td><img src="images/circularLed.jpg" alt="Led Circular" width="300"/></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Tipos de LEDs a detectar</em></td>
</tr>
</table>

# Indice:
### - [Deteccion con OpenCV](#detección-de-formas-en-tiempo-real-con-opencv)
### - [Deteccion con Yolov11](#detección-de-formas-en-tiempo-real-con-yOLO11)

# Detección de Formas en Tiempo Real con OpenCV

Un proyecto de visión por computador que detecta y clasifica formas geométricas (cuadrados y círculos) en tiempo real usando OpenCV y Python. El sistema utiliza filtrado de color HSV y análisis de contornos para identificar formas y proporcionar retroalimentación de conteo en vivo.

## Características

- **Detección de formas en tiempo real** desde la alimentación de cámara
- **Filtrado de color HSV** con barras de seguimiento ajustables
- **Clasificación geométrica** (cuadrados vs círculos)
- **Conteo en vivo** y visualización comparativa
- **Reducción de ruido** y estabilización de imagen

## Requisitos

```bash
pip install opencv-python numpy
```

## Uso

1. Conecta tu cámara (se recomienda cámara USB RGB de 5MP)
2. Ejecuta el script y ajusta las barras de seguimiento HSV para afinar la detección de color
3. Presiona `ESC` para salir

*Nota: Este proyecto fue desarrollado para detección específica de LEDs en un entorno industrial. Los parámetros pueden necesitar ajustes para diferentes objetos o condiciones de iluminación.*

## Implementación Técnica

### Funciones Principales de OpenCV Explicadas

#### **1. Captura de Video y Preprocesamiento**
```python
cap = cv2.VideoCapture(2)
frame = cv2.GaussianBlur(frame, (5, 5), 0)
```
- **VideoCapture(2)**: Accede al dispositivo de cámara (ajustar índice según necesidad)
- **GaussianBlur()**: Reduce el ruido y variaciones de iluminación para detección estable

#### **2. Conversión de Espacio de Color**
```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```
- **Espacio de color HSV**: Más robusto que RGB para detección basada en color
- Maneja mejor las variaciones de iluminación

#### **3. Barras de Seguimiento HSV para Filtrado Dinámico**
```python
cv2.createTrackbar("H_min", "HSV", 14, 179, nothing)
cv2.createTrackbar("S_min", "HSV", 80, 255, nothing)
cv2.createTrackbar("V_min", "HSV", 208, 255, nothing)
```
- **Ajuste interactivo**: Sintonización en tiempo real de parámetros de detección de color
- **H (Matiz)**: Tipo de color (0-179)
- **S (Saturación)**: Intensidad del color (0-255)
- **V (Valor)**: Brillo (0-255)

#### **4. Enmascaramiento de Color**
```python
mask = cv2.inRange(hsv, lower_bound, upper_bound)
```
- **Creación de máscara binaria**: Aísla píxeles dentro del rango HSV especificado
- Píxeles blancos = color objetivo, Píxeles negros = fondo

#### **5. Operaciones Morfológicas**
```python
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Rellenar huecos
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Eliminar ruido
mask = cv2.erode(mask, kernel)                          # Reducir objetos
```
- **MORPH_CLOSE**: Rellena pequeños agujeros dentro de objetos detectados
- **MORPH_OPEN**: Elimina pequeños puntos de ruido
- **Erode**: Reduce el tamaño del objeto para eliminar irregularidades de borde

#### **6. Detección de Contornos**
```python
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
- **RETR_EXTERNAL**: Solo encuentra contornos exteriores (ignora agujeros)
- **CHAIN_APPROX_SIMPLE**: Comprime contornos eliminando puntos redundantes

#### **7. Clasificación de Formas**
```python
approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
```
- **Aproximación poligonal**: Simplifica el contorno a vértices clave
- **Epsilon = 4%**: Equilibrio entre precisión y estabilidad
- **4 vértices = Cuadrado/Rectángulo**
- **Más vértices = Círculo/Otras formas**

#### **8. Dibujo de Contornos y Visualización de Texto**
```python
cv2.drawContours(frame, [approx], 0, (0, 0, 255), 3)
cv2.putText(frame, "Square", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
```
- **Retroalimentación visual**: Resalta formas detectadas con bordes coloreados
- **Etiquetas de clasificación**: Identificación de formas en tiempo real

## Controles

| Control | Función |
|---------|----------|
| **H_min/H_max** | Ajustar rango de matiz (tipo de color) |
| **S_min/S_max** | Ajustar rango de saturación (intensidad del color) |
| **V_min/V_max** | Ajustar rango de valor (brillo) |
| **Tecla ESC** | Salir de la aplicación |

## Flujo del Algoritmo

1. **Capturar** → Leer frame de la cámara web
2. **Difuminar** → Aplicar filtro Gaussiano para reducción de ruido
3. **Convertir** → Transformar BGR a espacio de color HSV
4. **Filtrar** → Crear máscara binaria usando umbrales HSV
5. **Limpiar** → Aplicar operaciones morfológicas
6. **Detectar** → Encontrar contornos en máscara procesada
7. **Clasificar** → Analizar vértices para determinar tipo de forma
8. **Mostrar** → Mostrar resultados con conteos y etiquetas

## Resultados del Proyecto

<table>
<tr>
<td><img src="images/DetectionHSV.png" alt="Barras de Seguimiento HSV" width="300"/></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Interfaz interactiva de ajuste HSV</em></td>
</tr>
</table>

<table>
<tr>
<td><img src="images/SquareDetection.png" alt="Detección de Cuadrados" width="300"/></td>
<td><img src="images/SquareDetectionMask.png" alt="Máscara de Cuadrados" width="300"/></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Detección de LEDs cuadrados independientemente de la posición</em></td>
</tr>
</table>

<table>
<tr>
<td><img src="images/CircleDetection.png" alt="Detección de Círculos" width="300"/></td>
<td><img src="images/CircleDetectionMask.png" alt="Máscara de Círculos" width="300"/></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Detección de LEDs circulares independientemente de la posición</em></td>
</tr>
</table>

# Detección de Formas en Tiempo Real con YOLO11

Un enfoque de aprendizaje profundo para detectar y clasificar formas geométricas (cuadrados y círculos) en tiempo real utilizando YOLO11 y modelos entrenados personalizados. Esta implementación proporciona una precisión y robustez superiores en comparación con los métodos tradicionales de visión por computadora.  
El etiquetado del dataset se hizo con [Roboflow.com](https://roboflow.com/), una plataforma que facilita la gestión, anotación, preprocesamiento y entrenamiento de modelos de visión por computadora, especialmente para detección de objetos, clasificación y segmentación de imágenes. Permite crear datasets personalizados y entrenar modelos de forma sencilla, incluso sin experiencia previa en machine learning.  
Este modelo fue entrenado con una NVIDIA RTX A4000 utilizando [RunPod.io](https://www.runpod.io/), una plataforma de computación en la nube que proporciona instancias de GPU bajo demanda y asequibles para aprendizaje automático, entrenamiento de IA, inferencia y otras tareas computacionales intensivas.

## Características

- **Modelo YOLO11 personalizado** entrenado específicamente para detección de formas de LEDs
- **Inferencia en tiempo real** con soporte de aceleración por GPU
- **Detección de alta precisión** (99.5% mAP50)
- **Conteo y clasificación en vivo** con retroalimentación instantánea
- **Robusto ante variaciones de iluminación** y ángulos de visión

## Requisitos

```bash
pip install -r required.txt
```

## Uso
### Ejecutar detección en tiempo real:
1. Ve a la sección "Releases" de este repositorio y descarga [Yolo11_Model](https://github.com/IsmaTIBU/LedType_detection/releases/tag/Yolo11_Model) y cárgalo en el mismo directorio que detect.py
2. Ejecuta ``` detect.py ```

## Entrenamiento del Modelo
### El modelo YOLO11 fue entrenado en un conjunto de datos personalizado que contiene:

- 102 imágenes de entrenamiento (81 entrenamiento, 21 validación, 10 prueba)
- ≈500 instancias etiquetadas (círculos y cuadrados)
- 20 épocas con parada temprana
- Tamaño de lote: 8 para rendimiento óptimo

### Resultados del Entrenamiento
| Métrica | Valor | Descripción | 
|---------|-------|-------------|
| **mAP50** | 99.5% | Precisión Promedio Media al 50% IoU |  
| **mAP50-95** | 78.1% | Precisión Promedio Media (50-95% IoU) |  
| **Precisión** | 99.9% | Exactitud de las predicciones positivas |  
| **Recall** | 100% | Capacidad para encontrar todas las instancias positivas |  

### Progreso del Entrenamiento

<table>
<tr>
<td><img src="images/labels.jpg" width="600"/></td>
<td><img src="images/labels_correlogram.jpg"  width="600"/></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Etiquetado</em></td>
</tr>
</table>

<table>
<tr>
<td><img src="images/confusion_matrix.png" width="600"/></td>
<td><img src="images/confusion_matrix_normalized.png" width="600"/></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Matrices de confusión (Sin normalizar/Normalizada)</em></td>
</tr>
</table>

<table>
<tr>
<td><img src="images/P_curve.png" width="400"/></td>
<td><img src="images/PR_curve.png" width="400"/></td>
<td><img src="images/R_curve.png" width="400"/></td>
</tr>
<tr>
<td colspan="3" align="center"><em>Curvas de confianza (Precisión/Precisión-Recall/Recall)</em></td>
</tr>
</table>

<table>
<tr>
<td><img src="images/Square_anglepic.png" width="900"/></td>
<td><img src="images/squarepic.png" width="900"/></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Cuadrados: Se logra una detección correcta de LEDs incluso con hasta 60° de inclinación de cámara respecto a la placa.</em></td>
</tr>
</table>

<table>
<tr>
<td><img src="images/circle_anglepic.png" width="900"/></td>
<td><img src="images/circlepic.png" width="900"/></td>
</tr>
<tr>
<td colspan="2" align="center"><em>Círculos: Se logra una detección correcta de LEDs incluso con hasta 70°-75° de inclinación de cámara respecto a la placa.</em></td>
</tr>
</table>

## Conclusión: 
Aunque tanto la detección basada en OpenCV como el modelo YOLOv11 funcionan razonablemente bien, existe una diferencia notable en su versatilidad bajo diversas condiciones del mundo real.  
El modelo YOLOv11 supera consistentemente al enfoque de OpenCV—no solo en precisión de detección sino especialmente en su robustez a través de configuraciones diversas. Probé ambos métodos usando varias cámaras (variando en conteo de megapíxeles y saturación de color) y bajo diferentes condiciones de iluminación. En todos los escenarios, el modelo YOLOv11 demostró una adaptabilidad superior y una detección de LEDs más confiable, independientemente de la cámara o variabilidad de iluminación.
