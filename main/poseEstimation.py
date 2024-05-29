import cv2
import mediapipe as mp
from sklearn.discriminant_analysis import StandardScaler


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils


def extract_pose_features(video_path):
    cap = cv2.VideoCapture(video_path)
    features = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        landmarks = get_pose_landmarks(frame)
        if landmarks:
            frame_features = []
            for landmark in landmarks:
                frame_features.extend([landmark.x, landmark.y, landmark.z])
            features.append(frame_features)

    cap.release()
    return np.array(features)

def preprocess_features(features):
    scaler = StandardScaler()
    return scaler.fit_transform(features)

def get_pose_landmarks(image):
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        return landmarks
    return None



def check_alignment(landmarks, exercise):
    if exercise == 'bench_press':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - left_elbow.y) < 0.1 and abs(left_elbow.y - left_wrist.y) < 0.1 and
            abs(right_shoulder.y - right_elbow.y) < 0.1 and abs(right_elbow.y - right_wrist.y) < 0.1):
            return True
        return False

    elif exercise == 'squat':
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        if (left_hip.y > left_knee.y > left_ankle.y and
            right_hip.y > right_knee.y > right_ankle.y):
            return True
        return False

    elif exercise == 'deadlift':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        if (left_shoulder.y < left_hip.y < left_knee.y < left_ankle.y and
            right_shoulder.y < right_hip.y < right_knee.y < right_ankle.y):
            return True
        return False

    elif exercise == 'push_up':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - left_elbow.y) < 0.1 and abs(left_elbow.y - left_wrist.y) < 0.1 and
            abs(right_shoulder.y - right_elbow.y) < 0.1 and abs(right_elbow.y - right_wrist.y) < 0.1):
            return True
        return False

    elif exercise == 'plank':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        if (abs(left_shoulder.y - left_hip.y) < 0.1 and abs(left_hip.y - left_ankle.y) < 0.1 and
            abs(right_shoulder.y - right_hip.y) < 0.1 and abs(right_hip.y - right_ankle.y) < 0.1):
            return True
        return False

    elif exercise == 'lat_pulldown':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - right_shoulder.y) < 0.1 and
            left_elbow.y > left_shoulder.y and right_elbow.y > right_shoulder.y and
            left_wrist.y > left_elbow.y and right_wrist.y > right_elbow.y):
            return True
        return False

    elif exercise == 'barbell_biceps_curl':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.x - left_elbow.x) < 0.1 and abs(left_shoulder.z - left_elbow.z) < 0.1 and
            abs(right_shoulder.x - right_elbow.x) < 0.1 and abs(right_shoulder.z - right_elbow.z) < 0.1):
            return True
        return False

    elif exercise == 'chest_fly_machine':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        if (abs(left_shoulder.y - right_shoulder.y) < 0.1 and abs(left_elbow.y - right_elbow.y) < 0.1):
            return True
        return False

    elif exercise == 'shoulder_press':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - right_shoulder.y) < 0.1 and abs(left_elbow.y - right_elbow.y) < 0.1 and abs(left_wrist.y - right_wrist.y) < 0.1):
            return True
        return False

    elif exercise == 'decline_bench_press':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - left_elbow.y) < 0.1 and abs(left_elbow.y - left_wrist.y) < 0.1 and
            abs(right_shoulder.y - right_elbow.y) < 0.1 and abs(right_elbow.y - right_wrist.y) < 0.1):
            return True
        return False

    elif exercise == 'hammer_curl':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.x - left_elbow.x) < 0.1 and abs(left_shoulder.z - left_elbow.z) < 0.1 and
            abs(right_shoulder.x - right_elbow.x) < 0.1 and abs(right_shoulder.z - right_elbow.z) < 0.1):
            return True
        return False

    elif exercise == 'hip_thrust':
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        if (abs(left_hip.y - left_shoulder.y) < 0.1 and left_knee.y > left_hip.y and
            abs(right_hip.y - right_shoulder.y) < 0.1 and right_knee.y > right_hip.y):
            return True
        return False

    elif exercise == 'incline_bench_press':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - left_elbow.y) < 0.1 and abs(left_elbow.y - left_wrist.y) < 0.1 and
            abs(right_shoulder.y - right_elbow.y) < 0.1 and abs(right_elbow.y - right_wrist.y) < 0.1):
            return True
        return False

    elif exercise == 'lateral_raises':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - left_elbow.y) < 0.1 and abs(left_elbow.y - left_wrist.y) < 0.1 and
            abs(right_shoulder.y - right_elbow.y) < 0.1 and abs(right_elbow.y - right_wrist.y) < 0.1):
            return True
        return False

    elif exercise == 'leg_extension':
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        if (left_hip.y > left_knee.y > left_ankle.y and
            right_hip.y > right_knee.y > right_ankle.y):
            return True
        return False

    elif exercise == 'leg_raises':
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        if (abs(left_hip.y - left_shoulder.y) < 0.1 and left_knee.y > left_hip.y and
            abs(right_hip.y - right_shoulder.y) < 0.1 and right_knee.y > right_hip.y):
            return True
        return False

    elif exercise == 'pull_up':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - left_elbow.y) < 0.1 and left_elbow.y > left_shoulder.y and left_wrist.y > left_elbow.y and
            abs(right_shoulder.y - right_elbow.y) < 0.1 and right_elbow.y > right_shoulder.y and right_wrist.y > right_elbow.y):
            return True
        return False

    elif exercise == 'romanian_deadlift':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        if (left_shoulder.y < left_hip.y < left_knee.y < left_ankle.y and
            right_shoulder.y < right_hip.y < right_knee.y < right_ankle.y):
            return True
        return False

    elif exercise == 'russian_twist':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        if (abs(left_shoulder.y - left_hip.y) < 0.1 and abs(left_elbow.y - left_hip.y) < 0.1 and
            abs(right_shoulder.y - right_hip.y) < 0.1 and abs(right_elbow.y - right_hip.y) < 0.1):
            return True
        return False

    elif exercise == 't_bar_row':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        if (left_shoulder.y < left_hip.y < left_knee.y and
            right_shoulder.y < right_hip.y < right_knee.y):
            return True
        return False

    elif exercise == 'tricep_dips':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - left_elbow.y) < 0.1 and abs(left_elbow.y - left_wrist.y) < 0.1 and
            abs(right_shoulder.y - right_elbow.y) < 0.1 and abs(right_elbow.y - right_wrist.y) < 0.1):
            return True
        return False

    elif exercise == 'tricep_pushdown':
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if (abs(left_shoulder.y - left_elbow.y) < 0.1 and abs(left_elbow.y - left_wrist.y) < 0.1 and
            abs(right_shoulder.y - right_elbow.y) < 0.1 and abs(right_elbow.y - right_wrist.y) < 0.1):
            return True
        return False

    return True

def process_video(video_path, exercise):
    cap = cv2.VideoCapture(video_path)
    analysis_results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        landmarks = get_pose_landmarks(frame)
        if landmarks:
            alignment_status = check_alignment(landmarks, exercise)
            analysis_results.append(alignment_status)
            # Draw landmarks for visualization
            mp_drawing.draw_landmarks(frame, landmarks, mp_pose.POSE_CONNECTIONS)
    
    cap.release()
    return analysis_results
