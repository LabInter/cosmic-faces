import cv2
import os
import Functionalities as func

mp_face_mesh = func.mp.solutions.face_mesh

# Tentativa de acesso à camera com tratamento se der erro (except)
try:
    cap = cv2.VideoCapture(0)

except Exception as e:
    print(f"Erro ao abrir a câmera: {e}")

cont_file = 'cont.txt'
if not os.path.exists(cont_file):
    with open(cont_file, "w") as file:
        file.write("0")
    cont = 0
else:
    with open(cont_file, "r") as file:
        cont = int(file.read().strip())
    
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5) as face_mesh:

    cv2.namedWindow('MediaPipe FaceMesh', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('MediaPipe FaceMesh', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cont = func.main_loop(cap, face_mesh, cont)
        
cap.release()
cv2.destroyAllWindows()
with open("cont.txt", "w") as file:
    file.write(str(cont))