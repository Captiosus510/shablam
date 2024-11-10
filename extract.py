import scenedetect
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
import cv2
import os
import sys

THRESHOLD = 30

def extract_scenes(video_path):
    """
    Detects scenes in the video and returns a list of scene start and end timecodes.
    """
    # Initialize video manager and scene manager
    video_manager = open_video(video_path)
    scene_manager = SceneManager()

    # Add ContentDetector algorithm (constructor takes threshold as argument)
    scene_manager.add_detector(ContentDetector(threshold=THRESHOLD))

    # Detect scenes
    video_manager.seek(0)
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    # Print scene boundaries (start/end timecodes)
    return scene_list

def extract_middle_keyframes(video_path, scene_list, output_path='keyframes'):
    """
    Extracts the middle frame from each detected scene and saves it as an image.
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    video_capture = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    # Iterate over each scene and save the middle frame
    for i, (start, end) in enumerate(scene_list):
        middle_frame = start.get_frames() + (end.get_frames() - start.get_frames()) // 2
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
        ret, frame = video_capture.read()
        if not ret:
            print(f"Warning: Could not read frame at {middle_frame} in scene {i+1}")
            continue
        # Save frame to output path
        path_to_write = os.path.join(output_path, f'keyframe_{i+1}.jpg')
        cv2.imwrite(path_to_write, frame)
        print(f"Saved keyframe for scene {i+1} at {path_to_write}")

    video_capture.release()

def main(argv):
    """
    Main function to run scene detection and keyframe extraction.
    """
    if len(argv) < 3:
        print("Usage: python script.py <video_path> <movie_name>")
        return
    
    video_path = argv[1]
    movie_name = argv[2]

    # Extract scenes
    scene_list = extract_scenes(video_path)
    for i, scene in enumerate(scene_list):
        print('Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
            i + 1,
            scene[0].get_timecode(), scene[0].get_frames(),
            scene[1].get_timecode(), scene[1].get_frames()))

    # Set output directory for keyframes
    output_path = os.path.join('keyframes', movie_name)
    extract_middle_keyframes(video_path, scene_list, output_path)

if __name__ == '__main__':
    main(sys.argv)
