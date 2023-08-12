from project.user import User


class MovieApp:
    def __init__(self):
        self.movies_collection = []
        self.users_collection = []

    def find_user_by_username(self, name):
        return [u for u in self.users_collection if u.username == name]

    def register_user(self, username, age):
        user = self.find_user_by_username(username)

        if not user:
            new_user = User(username, age)
            self.users_collection.append(new_user)
            return f"{username} registered successfully."

        current_user = user[0]
        if current_user in self.users_collection:
            raise Exception("User already exists!")

    def upload_movie(self, username, movie):
        user = self.find_user_by_username(username)

        if not user:
            raise Exception("This user does not exist!")

        current_user = user[0]

        if movie.owner.username != current_user.username:
            raise Exception(f"{username} is not the owner of the movie {movie.title}!")

        if movie in self.movies_collection:
            raise Exception("Movie already added to the collection!")

        if current_user == movie.owner:
            self.movies_collection.append(movie)
            current_user.movies_owned.append(movie)
            return f"{username} successfully added {movie.title} movie."

    def edit_movie(self, username, movie, **kwargs):
        user = self.find_user_by_username(username)[0]

        if movie not in self.movies_collection:
            raise Exception(f"The movie {movie.title} is not uploaded!")

        if movie.owner.username != user.username:
            raise Exception(f"{username} is not the owner of the movie {movie.title}!")

        for current_attr, new_value in kwargs.items():
            setattr(movie, current_attr, new_value)

        return f"{username} successfully edited {movie.title} movie."

    def delete_movie(self, username, movie):
        user = self.find_user_by_username(username)[0]

        if movie not in self.movies_collection:
            raise Exception(f"The movie {movie.title} is not uploaded!")

        if movie.owner.username != user.username:
            raise Exception(f"{username} is not the owner of the movie {movie.title}!")

        self.movies_collection.remove(movie)
        user.movies_owned.remove(movie)
        return f"{username} successfully deleted {movie.title} movie."

    def like_movie(self, username, movie):
        user = self.find_user_by_username(username)[0]

        if movie.owner.username == user.username:
            raise Exception(f"{username} is the owner of the movie {movie.title}!")

        if movie in user.movies_liked:
            raise Exception(f"{username} already liked the movie {movie.title}!")

        movie.likes += 1
        user.movies_liked.append(movie)
        return f"{username} liked {movie.title} movie."

    def dislike_movie(self, username, movie):
        user = self.find_user_by_username(username)[0]

        if movie not in user.movies_liked:
            raise Exception(f"{username} has not liked the movie {movie.title}!")

        movie.likes -= 1
        user.movies_liked.remove(movie)
        return f"{user.username} disliked {movie.title} movie."

    def display_movies(self):
        if not self.movies_collection:
            return "No movies found."

        else:
            sorted_movies = sorted(self.movies_collection, key=lambda m: (-m.year, m.title))
            return '\n'.join([el.details() for el in sorted_movies])

    def __str__(self):
        if not self.users_collection:
            result = "All users: No users."
        else:
            all_users = ', '.join([u.username for u in self.users_collection])
            result = f"All users: {all_users}"

        if not self.movies_collection:
            result += "\nAll movies: No movies."
        else:
            all_movies = ', '.join([m.title for m in self.movies_collection])
            result += f"\nAll movies: {all_movies}"

        return result
