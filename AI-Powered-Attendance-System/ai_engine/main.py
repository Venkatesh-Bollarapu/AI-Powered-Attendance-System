
import cv2
import numpy as np
import face_recognition
import pickle
import time
import mediapipe as mp
import requests

mp_face = mp.solutions.face_mesh

face_find = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=5,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

with open('encodings.pickle', 'rb') as f:
    data = pickle.load(f)

known_encodings = data['encodings']
mapping = data['labels']

program_start_time = time.time()
dict_individual_time = {}
records = []

for value in mapping.values():
    dict_individual_time[value] = {'total': 0}

last_frame_time = time.time()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

_, frame = cap.read()
black_img = np.zeros_like(frame).astype('uint8')

text = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current = time.time()
    frame_time = current - last_frame_time
    last_frame_time = current

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_find.process(frame_rgb)

    location = []

    if results.multi_face_landmarks:
        for face_landmark in results.multi_face_landmarks:
            xs, ys = [], []
            for lm in face_landmark.landmark:
                xs.append(int(lm.x * w))
                ys.append(int(lm.y * h))
            location.append((min(ys), max(xs), max(ys), min(xs)))

    face_encodings = face_recognition.face_encodings(frame_rgb, location)
    names = []

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.55)
        distances = face_recognition.face_distance(known_encodings, encoding)
        best_index = np.argmin(distances)
        name = mapping[best_index] if matches[best_index] else "unknown"
        names.append(name)

    detected = set(names)

    for person in dict_individual_time:
        if person in detected:
            dict_individual_time[person]['total'] += frame_time

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], 50), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
    cv2.putText(
        frame,
        "ATTENDANCE TRACKING",
        (10, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    for (top, right, bottom, left), name in zip(location, names):
        color = (0, 0, 255) if name == "unknown" else (0, 255, 0)
        label = "Unknown" if name == "unknown" else f"{name}  {dict_individual_time[name]['total']:.1f}s"

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(
            frame,
            label,
            (left, top - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    cv2.imshow("frame", frame)

    if time.time() - program_start_time >= 30:
        for person, data in dict_individual_time.items():
            status = "Present" if data['total'] > 20 else "Absent"
            text += f'{person}   {data["total"]:.2f} sec   {status}\n'
            records.append(
                {
                    "name": person,
                    "attended_time": data['total'],
                    "status": status
                }
            )
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.putText(
    black_img,
    "ATTENDANCE SUMMARY",
    (black_img.shape[1] // 2 - 220, 80),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.1,
    (0, 255, 255),
    3
)

y = black_img.shape[0] // 2 - (len(text.split("\n")) * 20)

for line in text.strip().split("\n"):
    (tw, th), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    x = (black_img.shape[1] - tw) // 2
    cv2.putText(black_img, line, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    y += 40

try:
    response = requests.post("http://127.0.0.1:5000/attendance", json=records)
    if response.status_code == 200:
        print("added to the database successfully")
except Exception as e:
    print(e)

cv2.imshow("frame", black_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(text)
