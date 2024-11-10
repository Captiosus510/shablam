from . import extract, CNN_feature_extraction
import os
import sys

def create_movie_keyframes(video_path):
    """
    Extracts keyframes from a video and saves them to a directory.
    """
    # Extract scenes
    scene_list = extract.extract_scenes(video_path)
    for i, scene in enumerate(scene_list):
        print('Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
            i + 1,
            scene[0].get_timecode(), scene[0].get_frames(),
            scene[1].get_timecode(), scene[1].get_frames()))

    # Set output directory for keyframes
    output_path = os.path.join('keyframes', os.path.basename(video_path))
    extract.extract_middle_keyframes(video_path, scene_list, output_path)

def create_db_keyframes(movie_scene_path):
    # Create a folder of keyframes for all the movie scenes in the movie sceenes directory
    keyframe_dict = {}
    with os.scandir(movie_scene_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.mp4') and not os.path.exists(f'keyframes/{entry.name}'):
                create_movie_keyframes(entry.path)
            else:
                print(f"Keyframes for {entry.name} already exist")

    # takes each keyframe and turns it into a feature vector, each vector is then added to a dictionary with the movie names as the keys
    with os.scandir('keyframes') as entries:
        for entry in entries:
            movie_name = entry.name.split('_')[0]
            keyframe_dict[movie_name] = []
            with os.scandir(entry.path) as keyframes:
                for keyframe in keyframes:
                    vector = CNN_feature_extraction.create_img_vector(keyframe.path)
                    keyframe_dict[movie_name].append(vector)

    return keyframe_dict


def main(argv):
    """
    Main function to run keyframe extraction.
    """
    if len(argv) < 2:
        print("Usage: python script.py <movie_scene_path>")
        return
    
    movie_scene_path = argv[1]
    keyframe_dict = create_db_keyframes(movie_scene_path)
    
    print(keyframe_dict)
    

if __name__ == '__main__':
    main(sys.argv)