from sentence_transformers import SentenceTransformer
import scipy.spatial
class bert:
    def __init__(self):
        self.embedder = SentenceTransformer('bert-base-nli-mean-tokens')
     
    def similarity(self,entence1, sentence2):
        embeddings = self.embedder.encode([sentence1,sentence2])
        return 1 - scipy.spatial.distance.cosine(embeddings[0], embeddings[1])
