import os, sys
import extract
import CNN_feature_extraction
import create_database
from scipy.spatial.distance import cosine
import shutil


def closest_movie_match_per_frame(frame_vector, data_dict):
    """
    Calculates the cosine similarity between the frame vector and the vectors in the data dictionary.
    """
    # Initialize variables
    max_similarity = float('-inf')
    max_movie = ''
    
    # Iterate through the data dictionary
    for movie, movie_vectors in data_dict.items():
        for movie_vector in movie_vectors:
            similarity = 1 - cosine(frame_vector, movie_vector)
            if similarity > max_similarity:
                max_similarity = similarity
                max_movie = movie
    return  max_movie, max_similarity


def create_inp_keyframes(inp_path):
    """
    Extracts keyframes from input video and saves them as images.
    """
    # Extract scenes
    scene_list = extract.extract_scenes(inp_path)
    for i, scene in enumerate(scene_list):
        print('Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
            i + 1,
            scene[0].get_timecode(), scene[0].get_frames(),
            scene[1].get_timecode(), scene[1].get_frames()))

    # Set output directory for keyframes
    name = inp_path.split('_')[0]
    output_path = os.path.join('keyframes', 'temp')
    extract.extract_middle_keyframes(inp_path, scene_list, output_path)
    return output_path

def find_best_movie(inp_path, data_dict):
    """
    Finds the movie with the highest cosine similarity to the input video.
    """
    # Create keyframes from input video
    keyframe_dir = create_inp_keyframes(inp_path)
    similarity_scores = []

    # Load feature vectors from data dictionary
    with os.scandir(keyframe_dir) as entries:
        for keyframe in entries:
            vector = CNN_feature_extraction.create_img_vector(keyframe.path)
            movie_name, similarity = closest_movie_match_per_frame(vector, data_dict)
            similarity_scores.append((movie_name, similarity))

    # similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    return similarity_scores

def main(argv):
    """
    Main function to find the best matching movie.
    """
    if len(argv) < 2:
        print("Usage: python script.py <input_video_path>")
        return
    
    data_video_path = argv[1]
    data_dict = create_database.create_db_keyframes(data_video_path)
    print(data_dict)
    while True:
        input_video_path = input("Enter the path of the input video (or 'q' to quit): ")
        if input_video_path == 'q':
            break
        sim_scores = find_best_movie(input_video_path, data_dict)
        print(sim_scores)
        best_movie, best_score = sim_scores[0][0], sim_scores[0][1]
        if best_score < 0.6:
            print("No matching movie found.")
        else:
            print(f"The best matching movie is: {best_movie}")
        shutil.rmtree("keyframes/temp")
        

if __name__ == '__main__':
    main(sys.argv)