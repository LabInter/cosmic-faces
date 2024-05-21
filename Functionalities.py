import os
import cv2
import ast
import random
import mediapipe as mp

face_info = [None, None, None]
face_detected = False
phrases = [
    [
        "Are some technical objects just in the background, while the closer one gets to an epistemic situation, the more attention needs to be paid to the technical objects that are implied",
        "Machinic creativity not as the attribute of a technical individual, but as an operation of regulation of the technical assemblage",
        "Thinking the living being in the Technical Milieu and as a medium"
    ],
    [
        "What are the particular spatial conditions that allow for epistemic phenomena to occur? Would a word such as “density” or “saturation” be appropriate to convey how those minute moments and events seem to pull the experiment together?",
        "The aspiration to follow technical objects in their evolution is driven by an anthropological and ethical interest. Techniques have meaning and express life",
        "To understand techniques as an expression of life should not be mistaken as an esoteric claim: Technical objects are the result of 'social' actions, since they are actions of human beings. Within the realm of the social, technical objects transform and structural human practices"
    ],
    [
        "Binarisms that, mistaken for veritable states in and of themselves, can mislead our self-conceptions and lead us to believe that we are not metastable, but moving inexorably towards an a priori set point",
        "Far from conquering nature or reshaping his environment, primitive man’s first concern was to utilize his overdeveloped, intensely active nervous system, and to give form to a human self, set apart from his original animal self by the fabrication of symbols",
        "We and our tools have become “hybrids”—“cyborgs”"
    ],
    [
        "Technology is not anthropologically universal, being enabled and constrained by particular cosmologies, which go beyond functionalities and utilities",
        "This transfer from intuition to calculation and construction can be interpreted as ”an emancipation of human beings from their conditions earthly animals” “transcendentally”, on the other hand, such a crisis “remains to be thought through”",
        "Whenever we construct knowledge around an unfamiliar Other, we make what is local and familiar to them familiar to us through a process of reduction by passing what is observed through our own concepts of the world, in what amounts to a “globalization” of knowledge"
    ],
    [
        "We should be aware that the concepts we hold to be very familiar and “natural” can themselves be subject to other interpretations and consequently, reductions, when viewed from the perspective of a cosmological or cultural Other",
        "Under the impression of a penetration of technical phenomena into the deeper layers of human relations of being, as cybernetic machines have made obvious, one is forced to see technology as a possible solution to that anthropologically determinable disproportion [between man and nature]. Through technology, man creates for himself an environment appropriate to his dual role as a natural and spiritual being",
        "The cybernetic extension of modern technology means its extension under the skin of the world; Technology can no longer be considered in any way isolated (objectified) from the world process and its sociological, ideological, and vital phases. It involves everything, it has been taken on an intensified consuming character. Literature, art, music take on its features"
    ],
    [
        "These socio-technological systems are less a fact, however, than an invention through which digital cultures, deeply rooted in technological forms of cooperation, can come into existence",
        "Not that comparisons between the animal and human worlds are anything particularly novel; what is new is the fact that today they are meant seriously, that the anthropological supremacy of the human is no longer capable of upholding itself in the current technical-organic overall structure.",
        "Such a rewriting of art history and sound art practices will have to be acutely aware of issues of globalization, postcolonialism, and decolonization; it will need to integrate representations on the Internet with those of live concerts, installations, and interviews; it must reach out toward anthropological methods; and it should make aesthetic considerations central to its analysis"
    ],
    [
        "Where there is presence and affect, there remains abundance, excess and the possibility of recording",
        "The “technique” of an action refers to the means employed as opposed to the meaning or end to which the action is, in the last analysis, oriented",
        "“Rational” technique is a choice of means which is consciously and systematically oriented to the experience and reflection of the actor, which consists, at the highest level of rationality, in scientific knowledge"
    ],
    [
        "In such a negative anthropological situation, belief means the ability to project possibilities for bifurcation, in a system that is on the way to becoming closed and requires a change that by itself the system cannot calculate. Such possibilities are those prescribed and certified by work-knowledge, life-knowledge, and conceptual knowledge, that is, by knowledge of how to live, do, and think",
        "Some anthropological data suggest that the concept of 'person' is not limited to the human class, but that animals or objects may possess 'person' qualities in that they are perceived as origins and causes of changes in the field, as endowed with a power of their own",
        "Relation must be understood as something that precedes the formation of the terms of the relation (subject, object, individual, groups, indeed all forms of collective human and nonhuman agents): predominantly, it must traverse all modes and levels of Being, from the micro to the macro, meaning that it is a 'modality of being'"
    ],
]

# "constantes"
SMALL_DISTANCE = 120
BIG_DISTANCE = 70

# Salvar a imagem de captura de a cada 10 rostos.
def main_loop(cap, face_mesh, cont):
    global face_info
    global face_detected

    while cap.isOpened():
        try:
            success, image = cap.read()

            if not success:
                raise Exception("Não foi possível abrir a câmera.")
            
            image.flags.writeable = False
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            image.flags.writeable = True

            if results.multi_face_landmarks:
                #resultados = reversed(results.multi_face_landmarks)

                cont = handle_faces(reversed(results.multi_face_landmarks), image, cont)
            else:
                face_detected = False
                face_info = [None, None, None]

            cv2.imshow('MediaPipe FaceMesh', image)
            
            # Caso seja pressionado "esc", encerra a execução do programa.
            key = cv2.waitKey(5) & 0xFF
            if key == 27:
                break
        except Exception as e:
            print(f"Erro: {e}")
    return cont

# Gerencia os rostos que estão sendo identificados
# para cada um ser tratado individualmente
def handle_faces(multi_face_landmarks, image, cont):
    global face_info
    image_copy = image.copy()

    # Variáveis para a criação da mascara.
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing_styles = mp.solutions.drawing_styles

    for idx, face_landmarks in enumerate(multi_face_landmarks):
        cont = handle_face(idx, face_landmarks, image, image_copy, cont)

    for i in range(3):
        if i > idx:
            face_info[i] = None

    for info in face_info:
        if info:
            make_landmarks(mp_drawing, mp_face_mesh, mp_drawing_styles, image, info['landmarks'])
            cv2.putText(image, info['frase'], (info['x_text'], info['y_text']), cv2.FONT_HERSHEY_SIMPLEX, info['font_size'], info['color'], 2, cv2.LINE_AA)

    return cont

# Constrói o vetor de informações necessárias sobre o rosto
# Salva um print do rosto que foi detectado.
# OBS: Recebe um rosto por vez.
def handle_face(idx, face_landmarks, image, image_copy, cont):
    global face_info
    global face_detected
    distance, x_forehead, y_forehead, coordenadas = get_positions(face_landmarks, image)

    try:
        if face_info[idx] == None:
            i = random.randint(0, 74)
            face_detected = True
        else:
            i = face_info[idx]['i']
    except:
        i = random.randint(0, 74)
        face_detected = True
    
    frase, color, font_size = get_text_and_color(distance, i, SMALL_DISTANCE, BIG_DISTANCE)
    x, y = set_text_position(x_forehead, y_forehead, frase, font_size)

    # Armazene as informações do rosto atual
    face_info[idx] = {
        'frase': frase,
        'color': color,
        'font_size': font_size,
        'x_text': x,
        'y_text': y,
        'i': i,
        'landmarks': face_landmarks,
        'coordenadas': coordenadas
    }

    if face_detected and cont is not None:
        print_image(image_copy, cont)
        save_coordenadas(coordenadas, cont)
        cont += 1
        face_detected = False

    return cont

# Retorna o cálculo da distância entre a testa e o queixo para saber se o rosto está próximo ou distante.
# Retorna também as coordenadas (x, y) da testa para posicionar a frase
def get_positions(face_landmarks, image):
    pt_forehead = 10  # Ponto da testa
    pt_chin = 152  # Ponto do queixo

    x_forehead = face_landmarks.landmark[pt_forehead].x * image.shape[1]
    y_forehead = face_landmarks.landmark[pt_forehead].y * image.shape[0]
    x_chin = face_landmarks.landmark[pt_chin].x * image.shape[1]
    y_chin = face_landmarks.landmark[pt_chin].y * image.shape[0]

    distance = ((x_forehead - x_chin)**2 + (y_forehead - y_chin)**2)**0.5

    pontos = [
        103, 67, 109, 10, 338, 297, 332, 284, 251, 389, 
        356, 454, 323, 401, 361, 435, 288, 397, 365, 379, 
        378, 400, 377, 152, 148, 176, 149, 150, 136, 172,
        58, 132, 93, 234, 127, 162, 21, 54
    ]

    lista_coordenadas = []

    for p in pontos:
        x = face_landmarks.landmark[p].x * image.shape[1]
        y = face_landmarks.landmark[p].y * image.shape[0]

        lista_coordenadas.append((x, y))

    return distance, x_forehead, y_forehead, lista_coordenadas

# Retorna uma frase aleatória
# E a cor e o tamanho da fonte com base na distância que o rosto está.
# TODO: phrases é um vetor que ocupa muito espaço, armazenar de uma maneira diferente.
def get_text_and_color(distance, i, marca_prox, marca_dist):
    colors = [(0, 255, 0), (0, 255, 255), (0, 0, 255)]  # Verde, Amarelo, Vermelho

    if distance > marca_prox:
        frase = phrases[i][0] # ...[0] indica a versão amigável da frase
        color = colors[0]  # Verde
        font_size = 1.15  # Tamanho padrão da fonte
    elif distance < marca_prox and distance > marca_dist:
        frase = phrases[i][1] # ...[1] indica a versão razoável da frase
        color = colors[1]  # Amarelo
        font_size = 1.4  # Tamanho médio da fonte
    elif distance < marca_dist:
        frase = phrases[i][2] # ...[2] indica a versão agressiva da frase
        color = colors[2]  # Vermelho
        font_size = 1.8  # Tamanho grande da fonte

    return frase, color, font_size

# Com base nas coordenadas (x, y) do ponto da testa e do tamanho da frase
# define a posição na tela.
def set_text_position(x_forehead, y_forehead, frase, font_size):
    text_width, _ = cv2.getTextSize(frase, cv2.FONT_HERSHEY_SIMPLEX, font_size, 2)[0]

    x = int(x_forehead - text_width // 2)
    y = int(y_forehead) - 50

    return x, y

# "Tira um print" da tela e salva no formato imageX.png
def print_image(image_copy, cont):
    folder_name = "images"
    folder_path = os.path.join(".", folder_name)
    image_path = os.path.join(folder_path, f"image{cont}.png")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    cv2.imwrite(image_path, image_copy)

def save_coordenadas(coordenadas, cont):
    folder_name = "coordenadas"
    folder_path = os.path.join(".", folder_name)
    file_path = os.path.join(folder_path, "coordenadas.txt")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, 'a') as file:
        linha = f"{cont}:{coordenadas}\n"
        file.write(linha)

def load_coordenadas(file_path):
    coordenadas = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            coordenadas = file.readlines()
    else:
        print("Arquivo de coordenadas não encontrado.")

    return coordenadas

# Utiliza os landmarks para desenhar a máscara
def make_landmarks(mp_drawing, mp_face_mesh, mp_drawing_styles, image, face_landmarks):
    white_color = (255, 255, 255) 
    drawing_style = mp_drawing.DrawingSpec(color=white_color, thickness=1, circle_radius=1)

    mp_drawing.draw_landmarks(
        image=image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=drawing_style
    )
    mp_drawing.draw_landmarks(
        image=image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_IRISES,
        landmark_drawing_spec=None,
        connection_drawing_spec=drawing_style
    )

    
def is_face_near_edge(x_forehead, y_forehead, x_chin, y_chin, image_shape, margin=50):
    # Obtém as dimensões da imagem
    height, width = image_shape

    # Verifica se o rosto está muito próximo da borda da imagem com a margem especificada
    if (
        x_forehead < margin
        or y_forehead < margin
        or width - x_chin < margin
        or height - y_chin < margin
    ):
        return True
    else:
        return False