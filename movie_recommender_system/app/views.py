import pandas as pd
import pickle
from django.shortcuts import render
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Load the dataset and vectorizer once (you can optimize further using caching)
df_path = "C:/Users/Kunal/OneDrive/Desktop/movie_recommender_system/app/pickle_files/Ready_Netflix_movies_data.csv" # Change to your CSV path
pkl_path = "C:/Users/Kunal/OneDrive/Desktop/movie_recommender_system/app/pickle_files/tfid.pkl"          # Change to your pickle path

#app\pickle_files\Ready_Netflix_movies_data.csv

df_2 = pd.read_csv(df_path)
df_2['tag'] = df_2['tag'].astype(str)

# Load vectorizer from file
with open(pkl_path, "rb") as f:
    vectorizer = pickle.load(f)

# Transform tags and compute similarity
tag_matrix = vectorizer.transform(df_2['tag'])
similarity = cosine_similarity(tag_matrix)

def recommend_view(request):
    context = {}

    if request.method == "POST":
        title = request.POST.get("title")

        all_titles = df_2['title'].tolist()
        best_match, score = process.extractOne(title, all_titles)

        if score < 60:
            context['error'] = f"No close match found for '{title}'. Try another title."
        else:
            idx = df_2[df_2['title'] == best_match].index[0]
            sim_scores = list(enumerate(similarity[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

            recommendations = []
            for i, (index, sim_score) in enumerate(sim_scores):
                movie = df_2.iloc[index]
                recommendations.append({
                    "title": movie['title'],
                    "genres": movie['genres'],
                    "tag": movie['tag'],
                    "score": round(sim_score, 3)
                })

            context['best_match'] = best_match
            context['match_score'] = score
            context['recommendations'] = recommendations

    return render(request, "app/templates/index.html", context)
