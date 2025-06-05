import mediapipe as mp
import cv2
import time
import winsound
from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email import encoders
# from email.mime.base import MIMEBase
from email.message import EmailMessage
import smtplib

sender_email = "indrajithpg10@gmail.com"
receiver_email = "raveenaramesh3003@gmail.com"
password = "wwij izva qmwp nxbn"

subject = "Human detected"
body = ""


def send_email_with_attachment(filename):
    try:
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M:%S")
        body=f"human detected at {formatted}💀💀💀 ⚠️⚠️⚠️"
        msg.set_content(body)

        with open(filename, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=filename)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)

        print("✅ Email sent with screenshot.")
    except Exception as e:
        print("❌ Failed to send email:", e)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    if results.pose_landmarks:
        cv2.putText(frame, 'Human detected', (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        filename = f"screenshot_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        winsound.Beep(1000,500)
        send_email_with_attachment(filename)
    cv2.imshow('Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()