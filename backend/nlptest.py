# import spacy
# nlp = spacy.load('en')
# w1 = nlp('difficulty in breathing')
# w2 = nlp('difficult to breathe')
# print(w1.similarity(w2))
# print(w1.similarity(w2))
# print(w1.similarity(w2))
# print(w1.similarity(w2))
# print(w1.similarity(w2))

from scipy import spatial
from sentence_transformers import SentenceTransformer

print("BEFORE LOADING")
similarity_model = SentenceTransformer('bert-base-nli-mean-tokens')
print("AFTER LOADING")

def get_sent_similarity(question, answer):
    question_encodings = similarity_model.encode([question])[0]
    ans_encodings = similarity_model.encode([answer])[0]
    result = 1 - spatial.distance.cosine(ans_encodings, question_encodings)
    return result

print(get_sent_similarity('fluid discharge or blood discharge', ' blood discharge'))
print(get_sent_similarity('difficulty in breathing', 'difficult to breathe'))