import os
from sentence_transformers import SentenceTransformer, util

model: SentenceTransformer = None


def init():
    global model
    if not model:
        model = SentenceTransformer(os.environ.get('MODEL_PATH'))


def encode(sentences: list[str]):
    init()
    return model.encode(sentences)


def compute_similarity(sentences: list[str]):
    init()
    embeddings = model.encode(sentences, convert_to_tensor=True)
    scores = util.cos_sim(embeddings, embeddings)
    resp = []
    for i in range(len(sentences)-1):
        for j in range(i+1, len(sentences)):
            resp.append(
                {"sentence1": sentences[i],
                 "sentence2": sentences[j],
                 "score": scores[i][j].item()})
    return resp
