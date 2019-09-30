from sklearn.externals import joblib
import cv2
import numpy as np
import face_recognition

# photo_model = joblib.load("/home/botree/study/practice/dipak-api/face_recognize/print_attack_anti_spoofing.pkl")
video_model = joblib.load("replay_attack_anti_spoofing.pkl")
def calc_hist(img):
    histogram = [0] * 3
    for j in range(3):
        histr = cv2.calcHist([img], [j], None, [256], [0, 256])
        histr *= 255.0 / histr.max()
        histogram[j] = histr
    return np.array(histogram)

def detect_spoof(img_gray):
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_ycrcb = cv2.cvtColor(img_gray, cv2.COLOR_BGR2YCR_CB)
    img_luv = cv2.cvtColor(img_gray, cv2.COLOR_BGR2LUV)
    ycrcb_hist = calc_hist(img_ycrcb)
    luv_hist = calc_hist(img_luv)

    feature_vector = np.append(ycrcb_hist.ravel(), luv_hist.ravel())
    feature_vector = feature_vector.reshape(1, len(feature_vector))

    # photo_prediction = photo_model.predict_proba(feature_vector)
    video_prediction = video_model.predict_proba(feature_vector)
    # photo_prob = photo_prediction[0][1]
    video_prob = video_prediction[0][1]

    # print(photo_prob,video_prob)
    return True if video_prob>=0.7 else False

# img = cv2.imread("/home/botree/study/practice/team.jpg")
# cap = cv2.VideoCapture(0)
# while True:
#     ret, img = cap.read()
#     # faces = face_recognition.face_locations(img)
#     # # print(faces)
#     # for i, (top, r, bottom, l) in enumerate(faces):
#     #     cv2.rectangle(img, (l, top), (r, bottom), (255, 0, 0), 2)
#     cv2.imshow('img_rgb', img)
#     key = cv2.waitKey(1)
#     if key & 0xFF == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()
# # print(img)
# cv2.imwrite("detect.jpg",img)
# faces = face_recognition.face_locations(img)
# print(faces)
# for i, (top, r, bottom, l) in enumerate(faces):
#     cv2.rectangle(img, (l, top), (r, bottom), (255, 0, 0), 2)
#     cv2.imwrite("detect.jpg",img)
#     face = img[top:bottom, l:r]
#     cv2.imwrite("t.jpg",face)
#     detect_spoof(face)
# # print(faces)
# # # detect_spoof(img)
