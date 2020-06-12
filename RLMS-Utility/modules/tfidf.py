from .utils import fetch_faq_data, clean_sentence

from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = list(text.ENGLISH_STOP_WORDS) + ["all","another", "any" ,"anybody", "anyone", "anything", "as", "ought", "both" ,"each", "each other" ,"either", "enough", "everybody","everyone","everything" ,"few", "he","her","hers" ,"herself" ,"him" ,"himself", "his", "I", "idem", "it", "its" ,"itself" ,"many" ,"me", "mine", "most" ,"my" ,"myself" ,"naught" ,"neither" ,"one","nobody",  "nothing", "nought" ,"one", "one another","other", "others ought" ,"our" ,"ours", "ourself", "ourselves", "several" ,"she", "some" ,"somebody", "someone" ,"something", "somewhat", "such" ,"such like",  "thee", "their", "theirs", "theirself", "theirselves", "them","themself", "themselves" ,"there", "these", "they", "thine", "this", "those", "thou", "thy", "thyself", "us", "we" ,"whatnot", "whence",   "ye", "yon", "yonder", "you" ,"your", "yours", "yourself" ,"yourselves"]

def get_tfidf_response(input_string, section):
    global stop_words

    questions, answers = fetch_faq_data(section)
    clean_input_string = clean_sentence(input_string)

    vectorizer = TfidfVectorizer(stop_words)
    vectors = vectorizer.fit_transform(questions + [clean_input_string])

    scores = [round(score,4) for score in cosine_similarity(vectors[-1], vectors).tolist()[0]]
    scores, responses = (list(t) for t in zip(*sorted(zip(scores, answers), reverse=True)))

    return {
        "response1": responses[0], "confidence1": scores[0],
        #"response2": responses[1], "confidence2": scores[1]
        #"response3": responses[2], "confidence2": scores[2]
        #"response4": responses[3], "confidence2": scores[3]
        }

if __name__ == "__main__":
    print(get_tfidf_response("what is escrow"))
