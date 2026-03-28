import random


class Review:
    def __init__(self, rating, text):
        self.rating = rating
        self.text = text

    def pretty_print(self):
        # little sloppy formatting, but readable
        return f"({self.rating}/5) {self.text}"


class Movie:
    def __init__(self, title):
        self.title = title
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def average_rating(self):
        if not self.reviews:
            return 0
        total = sum(r.rating for r in self.reviews)
        return total / len(self.reviews)

    def display_reviews(self):
        print("Reviews for", self.title)
        for r in self.reviews:
            print("-", r.pretty_print())

    def best_review(self):
        if not self.reviews:
            return None
        best_score = max(r.rating for r in self.reviews)
        bests = [r for r in self.reviews if r.rating == best_score]
        return random.choice(bests)

    def worst_review(self):
        if not self.reviews:
            return None
        worst_score = min(r.rating for r in self.reviews)
        worsts = [r for r in self.reviews if r.rating == worst_score]
        return random.choice(worsts)


# driver code (kinda quick and messy)
movie_titles = [
    "Avengers",
    "avengers infinity war",
    "avengers end game",
    "thor",
    "iron man 2",
]

for title in movie_titles:
    movie = Movie(title)
    movie.add_review(Review(5, "Loved it, cheesy but amazing."))
    movie.add_review(Review(2, "Plot was thin and a lil boring."))
    movie.add_review(Review(4, "Pretty good, actors were solid."))
    movie.add_review(Review(2, "Not my vibe, but had some fun moments"))
    movie.add_review(Review(5, "Best movie ever? maybe."))

    movie.display_reviews()
    print("Average rating:", movie.average_rating())

    best = movie.best_review()
    worst = movie.worst_review()

    print("Best review:", best.pretty_print() if best else "none")
    print("Worst review:", worst.pretty_print() if worst else "none")
    print()
