import scenedetect
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
import cv2
import os

def extract_scenes(video_path):
    # Initialize video manager and scene manager
    video_manager = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=30))

    # Detect scenes
    video_manager.seek(0)
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    # Print scene boundaries (start/end timecodes)
    return scene_list

def extract_middle_keyframes(video_path, scene_list, output_path='keyframes'):
    os.makedirs('keyframes', exist_ok=True)
    video_capture = cv2.VideoCapture(video_path)
    for i, (start, end) in enumerate(scene_list):
        middle_sub_frame = start.get_frames() + (end.get_frames() - start.get_frames()) // 2
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, middle_sub_frame)
        ret, frame = video_capture.read()
        if not ret:
            continue
        path_to_write = os.path.join(output_path, f'keyframe_{i}.jpg')
        cv2.imwrite(path_to_write, frame)

def main():
    video_path = '../Inception_scene.mp4'
    scene_list = extract_scenes(video_path)
    for i, scene in enumerate(scene_list):
        print('Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
            i+1,
            scene[0].get_timecode(), scene[0].get_frames(),
            scene[1].get_timecode(), scene[1].get_frames()))
        
    extract_middle_keyframes(video_path, scene_list)
        

if __name__ == '__main__':
    main()
