from sentence_transformers import SentenceTransformer, util

class MovieFinder():
    """
    TBD
    """
    def __init__(self, query, sentence_transformer_model = 'all-MiniLM-L6-v2', movie_data):
        self.model = SentenceTransformer(sentence_transformer_model)
        self.query = query
        return
    def show_me_a_movie(self, data, n):
        self.query_embedding = model.encode(self.query)
        movie_data["similarity_score"] = movie_data.apply(lambda row: util.cos_sim(query_emb, model.encode(row["overview"])).item(), axis=1)
movie_data.sort_values("similarity_score", ascending=False, inplace=True)
movie_data.head(25)