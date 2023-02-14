from sentence_transformers import SentenceTransformer, util

class MovieFinder():
    """
    TBD
    """
    def __init__(self, query, sentence_transformer_model = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(sentence_transformer_model)
        self.query = query
        return
    def get_n_matches(self, data, col, n):
        self.query_embedding = self.model.encode(self.query)
        data["similarity_score"] = data.apply(
            lambda row: util.cos_sim(
                self.query_embedding, 
                self.model.encode(row["overview"])
            ).item(), axis=1)
        data.sort_values("similarity_score", ascending=False, inplace=True)
        self.top_matches = data.head(n)
        return