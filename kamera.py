from ultralytics import YOLO
import cv2
import serial
import time

# =====================================
# MEGA 2560
# =====================================

mega = serial.Serial(
    port="COM6",
    baudrate=115200,
    timeout=1
)

time.sleep(2)

print("Mega 2560 baglandi!")

# =====================================
# YOLO
# =====================================

model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(0)

# Son gönderilen veri
last_message = ""

while True:

    ret, frame = cap.read()

    if not ret:
        print("Kamera goruntusu alinamadi!")
        break

    # YOLO
    results = model(frame)

    # Kutuları görüntüye çiz
    annotated_frame = results[0].plot()

    # =================================
    # NESNELERI TOPLA
    # =================================

    objects = {}

    for box in results[0].boxes:

        class_id = int(box.cls[0])
        object_name = model.names[class_id]

        confidence = float(box.conf[0])
        confidence_percent = int(confidence * 100)

        if object_name not in objects:

            objects[object_name] = {
                "count": 0,
                "confidence": confidence_percent
            }

        objects[object_name]["count"] += 1

        if confidence_percent > objects[object_name]["confidence"]:
            objects[object_name]["confidence"] = confidence_percent

    # =================================
    # MEGA'YA GONDER
    # =================================

    if objects:

        # Şimdilik en yüksek güvenli nesneyi seç
        best_object = max(
            objects,
            key=lambda x: objects[x]["confidence"]
        )

        count = objects[best_object]["count"]
        confidence = objects[best_object]["confidence"]

        message = f"{best_object.upper()},{count},{confidence}\n"

        # Aynı veriyi tekrar tekrar gönderme
        if message != last_message:

            mega.write(message.encode())

            print(
                "Mega'ya gonderildi:",
                message.strip()
            )

            last_message = message

    else:

        # Hiç nesne yoksa
        message = "YOK,0,0\n"

        if message != last_message:

            mega.write(message.encode())

            print(
                "Mega'ya gonderildi:",
                message.strip()
            )

            last_message = message

    # =================================
    # GORUNTU
    # =================================

    cv2.imshow(
        "YOLO + MEGA + NEXTION",
        annotated_frame
    )

    # Q = çık
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
mega.close()

cv2.destroyAllWindows()