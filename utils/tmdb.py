import requests
API_KEY = "349fd8fee0afbc7a6fcd207d59c746e7"

def get_movie(movie_name):
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': API_KEY,
        'query': movie_name
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Get the first result, if available
        if data['results']:
            movie = data['results'][0]
            return {
                'title': movie['title'],
                'overview': movie['overview'],
                'release_date': movie['release_date'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
                'backdrop_path': f"https://image.tmdb.org/t/p/w500{movie['backdrop_path']}" if movie['backdrop_path'] else None
            }
        else:
            return None
    else:
        return None
    


