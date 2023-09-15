import cv2
import time
import numpy as np

#Para guardar el output en un archivo output.avi.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Iniciar la cámara web.
cap = cv2.VideoCapture(0)

#Permitir a la cámara web iniciar. haciendo al código "dormir" o esperar por 2 segundos.
time.sleep(2)
bg = 0

#Capturar el fondo por 60 cuadros.
for i in range(60):
    ret, bg = cap.read()
#Voltear el fondo.
bg = np.flip(bg, axis=1)

#Leer el cuadro capturado hasta que la cámara esté abierta.
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    #Voltear la imagen para que haya concordancia.
    img = np.flip(img, axis=1)

     #Convertir el color de BGR a HSV.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Generar la máscara para detectar el color rojo (los valores se pueden cambiar).
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255,255])
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)
    
    mask_1 = mask_1 + mask_2

    cv2.imshow("mask_1", mask_1)

    #Abrir y expandir la imagen donde está mask 1 (color).
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    
   #Seleccionar solo la parte que no tiene mask 1 y guardarla en mask 2.
    mask_2=cv2.bitwise_not(mask_1)

    res_1=cv2.bitwise_and(img, img, mask=mask_2)
    res_2 = cv2.bitwise_and(bg, bg, mask=mask_1)

    #Guardar solo la parte de las imágenes sin color rojo. 
    #(o cualquier otro color que hayas escogido)
   

    #Guardar solo la parte de las imágenes con color rojo.
   

    #Generar el output final
    final_output = cv2.addWeighted(res_1,1,res_2,1,0)
    output_file.write(final_output)
    
    #Mostrar el output al usuario
    # cv2.imshow("magia", final_output)
    cv2.imshow("magia", final_output)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()
