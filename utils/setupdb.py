import pickle
from . import create_database

def create_pickle(movie_path):
    data_dict = create_database.create_db_keyframes(movie_path)

    with open("keyframedata.pkl", "wb") as file:
        pickle.dump(data_dict, file)
    


