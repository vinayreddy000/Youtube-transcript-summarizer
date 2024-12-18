from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/process_url', methods=['POST'])
def process_url():
    url = request.json.get('url')
    id_video=url.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(id_video,languages=['en','en-US'])
    doc = ""
    for line in transcript:
        doc =doc+ ' ' + line['text']
    doc=[]
    for line in transcript:
        if "\n" in line['text']:
            x=line['text'].replace("\n"," ")
            doc.append(x)
        else:
            doc.append(line['text'])
    paragraph=" ".join(doc)
    mytext= paragraph
    stops = set(stopwords.words('english'))
    word_array = word_tokenize(mytext)

    wordfreq=dict()
    for word in word_array:
        word=word.lower()
        if word in stops:
            continue
        elif word in wordfreq:
            wordfreq[word]+=1
        else:
            wordfreq[word]=1
    sent_array=sent_tokenize(mytext)

    sentfreq=dict()
    for sentence in sent_array:
        for word,freq in wordfreq.items():
            if word in sentence.lower():
                if sentence in sentfreq:
                    sentfreq[sentence]+=freq
                else:
                    sentfreq[sentence]=freq  
    averageval=0
    for sentence in sentfreq:
        averageval+=sentfreq[sentence]
 
    average=int(averageval/len(sentfreq))
    summary=''
    for sentence in sent_array:
        if(sentence in sentfreq) and (sentfreq[sentence]>(1.5*average)):
            summary=summary+" "+sentence
    summ={'summary':summary}
    return jsonify(summ)

if __name__ == '__main__':
    app.run(debug=True)