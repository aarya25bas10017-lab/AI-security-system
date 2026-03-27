import cv2
import time
import os

print("AI Security System Started...")

# Create folder
folder = "threat_captures"
if not os.path.exists(folder):
    os.makedirs(folder)

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("❌ Camera not opened")
    exit()

ret, frame1 = cap.read()
ret, frame2 = cap.read()

last_capture = 0

while True:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    threat = "LOW"
    threat_color = (0,255,0)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 2000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)

        if area < 5000:
            threat = "MEDIUM"
            threat_color = (0,255,255)
        else:
            threat = "HIGH"
            threat_color = (0,0,255)

    # Show threat level
    cv2.putText(frame1, f"Threat: {threat}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, threat_color, 2)

    # Show project title
    cv2.putText(frame1, "AI SMART SECURITY SYSTEM", (10,70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("AI Security Camera", frame1)

    current_time = time.time()

    # Save only HIGH threat
    if threat == "HIGH" and current_time - last_capture > 5:
        filename = f"{folder}/THREAT_{int(current_time)}.jpg"

        if cv2.imwrite(filename, frame1):
            print("🚨 THREAT DETECTED! Saved:", filename)
        else:
            print("❌ Save failed")

        last_capture = current_time

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
