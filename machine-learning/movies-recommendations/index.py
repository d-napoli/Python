import pandas as pd
import numpy as np

def vector_distance(a, b):
    return np.linalg.norm(a - b)

def user_ratings(user):
    user_ratings = ratings.query("userId=={}".format(user))
    user_ratings = user_ratings[["movieId", "rating"]].set_index("movieId")
    return user_ratings

def users_distance(user_id1, user_id2, minimum = 5):
    ratings1 = user_ratings(user_id1)
    ratings2 = user_ratings(user_id2)

    users_diff = ratings1.join(ratings2, lsuffix="_left", rsuffix="_right").dropna()

    if( len(users_diff) < minimum ):
        return None

    distance = vector_distance(users_diff["rating_left"], users_diff["rating_right"])
    return [user_id1, user_id2, distance]

def all_users_distances(from_user_id, amount_of_users = None):
    all_users = ratings["userId"].unique()
    if amount_of_users:
        all_users = all_users[:amount_of_users]
    distances = [ users_distance(from_user_id, user_id) for user_id in all_users ]
    distances = list( filter(None, distances) )
    distances = pd.DataFrame(distances, columns = ["from_user_id", "another_user", "distance"])
    return distances

def closest_users_from(from_user_id, k_closest_to = 10, amount_of_users = None):
    distances = all_users_distances(from_user_id, amount_of_users)
    distances = distances.sort_values("distance")
    distances = distances.set_index("another_user").drop(from_user_id, errors='ignore')
    return distances.head(k_closest_to)

def user_suggestions(from_user_id, amount_of_users = None):
    from_ratings = user_ratings(from_user_id)
    watched_movies = from_ratings.index

    similar_user = closest_users_from(from_user_id, amount_of_users)
    similar_user_id = similar_user.iloc[0].name
    similar_user_ratings = user_ratings(similar_user_id)
    similar_user_ratings = similar_user_ratings.drop(from_ratings.index, errors='ignore')

    return similar_user_ratings.join(movies)

def knn(from_user_id, k_closest_to = 10, amount_of_users = None):
    watched_movies = user_ratings(from_user_id).index

    similars = closest_users_from(my_user_id, k_closest_to = k_closest_to, amount_of_users = amount_of_users)
    similar_users = similars.index

    similar_users_ratings = ratings.set_index("userId").loc[similar_users]
    recomendations = similar_users_ratings.groupby("movieId").mean()[["rating"]]
    appears = similar_users_ratings.groupby("movieId").count()[['rating']]

    recomendations = recomendations.join(appears, lsuffix="_average_from_users", rsuffix="_appears_in_users")

    min_filter = k_closest_to / 2

    recomendations = recomendations.query("rating_appears_in_users >= %.2f" % min_filter)

    recomendations = recomendations.sort_values("rating_average_from_users", ascending = False)
    recomendations = recomendations.drop(watched_movies, errors='ignore')
    return recomendations.join(movies)

def new_user(data):
    new_user = ratings['userId'].max() + 1
    new_user_rating = pd.DataFrame(data, columns=["movieId", "rating"])
    new_user_rating['userId'] = new_user
    return pd.concat([ratings, new_user_rating])

movies = pd.read_csv("./data/movies.csv")
movies = movies.set_index("movieId")

ratings = pd.read_csv("./data/ratings.csv")

ratings = new_user([[356, 5], [364, 4], [78499, 3], [4306, 3], [163645, 4], [88125, 2], [74458, 4], [1219, 5], [1246, 4], [2324, 4]])

my_user_id = 611
k_closest_to = 20
# amount_of_users = None

print( knn(my_user_id, k_closest_to = k_closest_to).head(100) ) 

# print( movies.sample(100) )