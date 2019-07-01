# minimal example from:
# http://flask.pocoo.org/docs/quickstart/

import pickle as pkl
import numpy as np
from sklearn.metrics import pairwise_distances
import flask
from flask import render_template, request, Flask

# create instance of Flask class
app = Flask(__name__, static_url_path='')  

with open('books_df.pkl', 'rb') as file:
    books_df = pkl.load(file)

topic_dict = {0: 'Long-Term Commitment', 1: 'Initial Contact', 2: 'Boundaries',
3: 'Behavioral Psychology', 4: 'Life Appreciation', 5: 'Attractive Behavior',
6: 'Phases of Dating', 7: 'Meeting People', 8: 'Online Dating', 9: 'Escalation',
10: 'Communication Styles', 11: 'Heartbreak', 12: 'Dreaming Big', 13: 'Science of Seduction',
14: 'Primal Instincts', 15: 'Family', 16: 'Personality Types', 17: 'Being Alpha'}

@app.route("/dating_book_home")
def home():

""" Main landing page """

    return render_template('dating_book_home.html')

@app.route("/dating_book_recommendation", methods=["POST", "GET"])
def recommend():

""" 
Takes user inputs of interests in author gender, audience, and topics in order
to recommend books to the user. Author gender and target audience are filtering
mechanisms, while topics of interest are assessed using cosine similarity. 
"""

    df = books_df.copy()

    # author_gender values are 'male', 'female', or '0'
    author_gender = request.args.get('author_gender', '0')

    # audience values are 'men', 'women', 'unisex', '0'
    audience = request.args.get('audience', '0')

    # filter by author gender and audience selections
    if author_gender != '0':
        df = df[df['author_gender'] == author_gender]

    if audience not in ['unisex', '0']:
        df = df[df['audience'] == audience]

    # extract only topic values from the DataFrame
    book_vectors = df[['topic_0', 'topic_1', 'topic_2', 
                       'topic_3', 'topic_4', 'topic_5',
                       'topic_6', 'topic_7', 'topic_8', 
                       'topic_9', 'topic_10', 'topic_11',
                       'topic_12', 'topic_13', 'topic_14', 
                       'topic_15', 'topic_16', 'topic_17']].values
    
    # each user can select up to 3 topics that they are interested in
    topics_list = []   
    for topic_num in range(18):
        if request.args.get(f'topic_{topic_num}', 0):
            topics_list.append(topic_num)    # max length of 3

    """ 
    user vectors are created by first extracting the vectors of the 
    books with the highest proportion of the respective topics, 
    then averaged over those vectors
    """
    user_vector = np.zeros((len(topics_list), 18))
    for ix, topic in enumerate(topics_list):
        user_vector[ix] = book_vectors[book_vectors[:, topic].argsort()[:-2:-1]]
    user_vector = np.mean(user_vector, axis=0)

    """ 
    find pairwise distances between user vectors and all book vectors, then
    sort to recommend most similar books based on cosine similarity
    """ 
    user_book_distances = pairwise_distances(user_vector.reshape(1,-1), 
                                             book_vectors, metric='cosine')
    recs = user_book_distances.argsort()[0][:4]
    
    picture_urls = df.iloc[recs]['picture_url'].tolist()
    purchase_urls = df.iloc[recs]['purchase_url'].tolist()
    titles = df.iloc[recs]['title'].tolist()
    
    # percentage match of the top 4 books 
    percentages = np.round((1 - np.sort(user_book_distances)[0][:4]) * 100, 2)
    topic_names = [topic_dict[topic] for topic in topics_list]

    return flask.render_template('dating_book_recommendation.html',
        picture_urls=picture_urls,
        purchase_urls=purchase_urls, 
        percentages=percentages,
        topic_names=topic_names)

if __name__ == '__main__':
    app.run()
