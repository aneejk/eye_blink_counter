
import cv2
import mediapipe as mp
import sys
import math
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
def GetFaceMeshCord(image,draw = True):
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    AllMesh = []
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5) as face_mesh:
      #for idx, file in enumerate(IMAGE_FILES):
        image = image
        image_height,image_width = image.shape[0:2]
        # Convert the BGR image to RGB before processing.
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print and draw face mesh landmarks on the image.
        if not results.multi_face_landmarks:
          return [[],[]]
        annotated_image = image.copy()
        for face_landmarks in results.multi_face_landmarks:
          count = 0
          face_points = []
          for ldmark in face_landmarks.landmark:
            x_px = min(math.floor(ldmark.x * image_width), image_width - 1)
            y_px = min(math.floor(ldmark.y * image_height), image_height - 1)
            face_points.append((x_px,y_px))
          print('point')
          AllMesh.append(face_points)
          if draw :
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style())
    return AllMesh,annotated_image
def points_Distance(p1, p2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)

        return length

