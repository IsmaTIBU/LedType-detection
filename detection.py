# Detección YOLO11 - Simple y elegante
import cv2
from ultralytics import YOLO

# Cargar modelo
model = YOLO('best.pt')

# Seleccion de camara predefinida (0)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("🎥 Detección iniciada. Presiona 'ESC' para salir")

while True:
    ret, frame = cap.read()
    if not ret:
       break
   
    results = model(frame, verbose=False)
   
    circles = 0
    squares = 0
   
    for box in results[0].boxes or []:
        if box.conf[0] > 0.5:
           x1, y1, x2, y2 = map(int, box.xyxy[0])
           cls = int(box.cls[0])
           conf = float(box.conf[0])
           label = f"{model.names[cls]}: {conf:.2f}"
           
            # Si cls=0 es un circulo, si cls=1 es cuadrado
           if cls == 0:
               circles += 1
               color = (0, 255, 0)
           else:
               squares += 1
               color = (255, 0, 0)
           
           cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
           cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
   
    cv2.putText(frame, f"Circles: {circles}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Squares: {squares}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
   
    if squares > circles:
       led_type = "Squared LEDs"
    elif circles > squares:
       led_type = "Circular LEDs"
    else:
       led_type = ""

    cv2.putText(frame, led_type, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
   
    cv2.imshow('YOLO11 Detection', frame)
    if cv2.waitKey(1) & 0xFF == 27:
       break

cap.release()
cv2.destroyAllWindows()