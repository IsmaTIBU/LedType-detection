import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(2)
cv2.namedWindow("HSV")
cv2.createTrackbar("H_min", "HSV", 14, 179, nothing)
cv2.createTrackbar("S_min", "HSV", 80, 255, nothing)
cv2.createTrackbar("V_min", "HSV", 208, 255, nothing)
cv2.createTrackbar("H_max", "HSV", 44, 179, nothing)
cv2.createTrackbar("S_max", "HSV", 255, 255, nothing)
cv2.createTrackbar("V_max", "HSV", 255, 255, nothing)

while True:
    _, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    hsv= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hmin= cv2.getTrackbarPos("H_min", "HSV")
    smin= cv2.getTrackbarPos("S_min", "HSV")
    vmin= cv2.getTrackbarPos("V_min", "HSV")
    hmax= cv2.getTrackbarPos("H_max", "HSV")
    smax= cv2.getTrackbarPos("S_max", "HSV")
    vmax= cv2.getTrackbarPos("V_max", "HSV")

    lower_yellow=np.array([hmin, smin, vmin])
    upper_yellow=np.array([hmax, smax, vmax])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    circ=0
    cuad=0
    for cnt in contours:
        aprox= cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        x=aprox.ravel()[0]
        y=aprox.ravel()[1]-10

        # Detectar rectángulos y cuadrados
        if len(aprox) == 4:
            x, y, w, h = cv2.boundingRect(aprox)
            aspect_ratio = float(w) / h
        
            cv2.putText(frame, "Square", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cuad+=1
        else:
            cv2.putText(frame, "Circle", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            circ+=1

        cv2.drawContours(frame, [aprox], 0, (0, 0, 255), 3)

    if cuad > circ:
        cv2.putText(frame, "Squared leds", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Circular leds", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    cv2.putText(frame, f"Squares:{cuad}, Circles:{circ}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)

    key=cv2.waitKey(50)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()