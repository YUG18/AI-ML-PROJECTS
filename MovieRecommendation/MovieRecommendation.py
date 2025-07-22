import requests


API_KEY = '08bd585c46575b374141fe2402515fa0'
#Dictionaries for movie and TV genres
#genre id's as tmdb uses id's for genres
MOVIE_GENRES = {
    "action": 28,
    "comedy": 35,
    "drama": 18,
    "horror": 27,
    "romance": 10749,
    "sci-fi": 878
}

TV_GENRES = {
    "action & adventure": 10759,
    "animation": 16,
    "comedy": 35,
    "drama": 18,
    "sci-fi & fantasy": 10765,
    "mystery": 9648
}

def fetch_movie(genre_name):
    genre_name = genre_name.lower()
    genre_id = MOVIE_GENRES[genre_name]
    if genre_name not in MOVIE_GENRES:
        print("Available genres : ",",".join(MOVIE_GENRES))
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "language": "en-US"
    }
    response = requests.get(url,params=params)
    if response.status_code == 200:
        data = response.json()
        return [(m['title'],m['original_title']) for m in data['results'][:20]]
    else:
        print("Unable to fetch movies...")
        return []

def fetch_series(genre_name,limit = 100):
    collected = []
    page = 1
    while(len(collected)<limit):
        genre_name = genre_name.lower()
        genre_id = TV_GENRES[genre_name]
        if genre_name not in TV_GENRES:
            print("Available genres : ", ",".join(TV_GENRES))
        url = "https://api.themoviedb.org/3/discover/tv"
        params = {
            "api_key": API_KEY,
            "with_genres": genre_id,
            "sort_by": "popularity.desc",
            "language": "en-US",
            "page": page
        }
        response = requests.get(url,params=params)
        if response.status_code != 200:
            break
        data = response.json()
        results = data.get('results',[])
        for show in results:
            name = show['name']
            original_name = show['original_name']
            collected.append((name,original_name))
            if len(collected)>=limit:
                break
        page+=1
        if page > data.get("total_pages",1):
            break
    return collected

def show_recommendations(recommendation):
    if not recommendation:
        print("No recommendations found")
        return
    else:
        for name,original_name in recommendation:
            if name != original_name :
                print(f"{name} - ({original_name})")
            else:
                print(f"{name}")

def main():
    while True:
        print("1 : Movies")
        print("2 : Series")
        print("3 : To break")
        user_choice = input("Enter 1,2 or 3: ")
        if user_choice == "1":
            print("Available genres : ", ",".join(MOVIE_GENRES))
            genre = input("Enter your option : ")
            results = fetch_movie(genre)
            show_recommendations(results)
        elif user_choice == "2":
            print("Available genres : ",",".join(TV_GENRES))
            genre = input("Enter your choice : ")
            results = fetch_series(genre)
            show_recommendations(results)
        elif user_choice == "4":
            break
        else:
            print("Invalid input enter a number amongst 1,2 and 3")
if __name__ == "__main__":
    main()