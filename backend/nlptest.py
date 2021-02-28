from scipy import spatial
from sentence_transformers import SentenceTransformer
# from backend.unique_symptoms import ambigious

def get_sent_similarity(question, answer, similarity_model):
    question_encodings = similarity_model.encode([question])[0]
    ans_encodings = similarity_model.encode([answer])[0]
    result = 1 - spatial.distance.cosine(ans_encodings, question_encodings)
    return result

ambigious = [
'muscle pain',
'stomach cramps',
'back pain',
'stomach pain',
'neck swelling',
'loss of appetite',
'muscle weakness',
'loss of balance',
'fast heart rate',
'facial pain',
'chest pain',
'difficulty in speaking',
'eye pain',
'joint pain',
'difficulty in moving joints',
'forgetfulness',
'inflammed eyes',
'difficulty in concentration',
'irritability'
]

def set_symptom(symptom, similarity_model):
    # symptom = "pain in joints"
    new_symp = ""
    max_match = 0
    if "breath" in symptom:
        new_symp = "difficulty in breathing"
    elif "recognize" in symptom:
        new_symp = "unable to recognize common things"
    else:
        for s in ambigious:
            match = get_sent_similarity(s, symptom, similarity_model)
            if match > max_match:
                print(str(match) + " " + s)
                new_symp = s
                max_match = match
    return new_symp

