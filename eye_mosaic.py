import cv2
import mediapipe as mp
import numpy as np

# Mediapipeの初期化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# 動画キャプチャの初期化
cap = cv2.VideoCapture(0)  # カメラをオープン

if not cap.isOpened():
    print("Error: カメラを開けませんでした。")
    exit()

# ウィンドウサイズを変更するスケール
resize_scale = 1.0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: フレームを取得できませんでした。")
        break

    # フレームの高さと幅を取得
    height, width, _ = frame.shape

    # フレームサイズを縮小
    small_frame = cv2.resize(frame, (int(width * resize_scale), int(height * resize_scale)))

    # BGRからRGBに変換
    frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Mediapipeで骨格検出を実行
    result = pose.process(frame_rgb)

    if result.pose_landmarks:
        # ランドマーク座標の取得
        landmarks = result.pose_landmarks.landmark
        left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE_OUTER]
        right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE_OUTER]

        # 座標をピクセル単位に変換
        left_eye_x, left_eye_y = int(left_eye.x * width), int(left_eye.y * height)
        right_eye_x, right_eye_y = int(right_eye.x * width), int(right_eye.y * height)

        # 目尻を結ぶ線（ベクトル）を計算
        eye_vector = np.array([right_eye_x - left_eye_x, right_eye_y - left_eye_y])
        eye_length = np.linalg.norm(eye_vector)
        eye_unit_vector = eye_vector / eye_length if eye_length != 0 else np.array([1, 0])

        # 垂線の方向ベクトルを計算（目ベクトルの垂直方向）
        perpendicular_vector = np.array([-eye_unit_vector[1], eye_unit_vector[0]])

        # 目の距離に基づいて四角形のサイズを計算
        eye_distance = eye_length  # 左目と右目の間の距離
        rect_width = int(eye_distance * 1.0)  # 距離に応じて幅を決定（例: 距離の1.2倍）
        rect_height = int(eye_distance * 0.3)  # 距離に応じて高さを決定（例: 距離の0.4倍）

        # 四角形の頂点を計算
        rect_top_left = (
            np.array([left_eye_x, left_eye_y])
            - eye_unit_vector * rect_width / 2
            - perpendicular_vector * rect_height
        )
        rect_top_right = (
            np.array([right_eye_x, right_eye_y])
            + eye_unit_vector * rect_width / 2
            - perpendicular_vector * rect_height
        )
        rect_bottom_left = (
            np.array([left_eye_x, left_eye_y])
            - eye_unit_vector * rect_width / 2
            + perpendicular_vector * rect_height
        )
        rect_bottom_right = (
            np.array([right_eye_x, right_eye_y])
            + eye_unit_vector * rect_width / 2
            + perpendicular_vector * rect_height
        )

        # 頂点を整数に変換
        rect_points = np.array(
            [rect_top_left, rect_top_right, rect_bottom_right, rect_bottom_left],
            dtype=np.int32,
        )

        # 四角形を描画（塗りつぶし）
        cv2.fillPoly(small_frame, [rect_points], (0, 0, 0))

    # 縮小されたフレームを表示
    cv2.imshow('Pose Detection', small_frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()
