# import spacy
# from spacy.lang.en import English

# nlp = English()  # just the language with no model
# sentencizer = nlp.create_pipe("sentencizer")
# nlp.add_pipe(sentencizer)
# doc = nlp("who is president's mother")
# for sent in doc:
#     print(sent.text)

for i, l in enumerate(wh_qs):
        if i == 0:
            continue
        w1 = l[0]
        w2 = wh_qs[i-1][-1]
        if w1 == w2:
            wh_qs[i-1].pop(-1)