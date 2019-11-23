from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from django import forms
from django.views.decorators.csrf import csrf_protect
from grammarbot import GrammarBotClient
import re
from googletrans import Translator
import speech_recognition as sr
# Create your views here.
class WritingContent(forms.Form):
    text = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control'}), label='' )

class PickupWords(forms.Form):
    word = forms.CharField(max_length=100, label='')
    word.widget.attrs.update({'id': 'input', 'class' : 'form-control', 'readonly' : 'readonly'})

@csrf_protect
def writing(request, article_id):
    if request.method == "POST":
        form = WritingContent(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            text = text.strip("\n\t\r .,?!;")
            client = GrammarBotClient(api_key='KS9C5N3Y')
            res_js = client.check(text).raw_json
            tokens = text.count(" ") + 1
            sens = text.count(".") + text.count("?") + text.count("!") + text.count(";") + 1
            result = []
            cnt_spelling = 0
            cnt_grammar = 0
            warn_start = "<span style=\"background-color:yellow\">"
            error_start = "<span style=\"background-color:red\">"
            we_end = "</span>"
            conflict = 0
            cnt_error = 0
            for messeage in res_js['matches']:
                offset = messeage['offset'] + conflict
                leng = messeage['length']
                if messeage['rule']['issueType'] == 'non-conformance':
                    text = text[0:offset] + warn_start + text[offset:offset+leng] + we_end + text[offset+leng:]
                    conflict += 44
                    error = {}
                    error['id'] = cnt_error
                    error['id2'] = cnt_error * 1000
                    error['msg'] = messeage['message']
                    try:
                        error['dst'] = messeage['description']
                    except:
                        error['dst'] = ""
                    error['rep'] = messeage['replacements']
                    cnt_error += 1
                    result.append(error)

                elif messeage['rule']['issueType'].find("grammar") != -1 or messeage['rule']['issueType'].find("misspelling") != -1:
                    if messeage['rule']['issueType'].find("grammar") != -1:
                        cnt_grammar += 1
                    else:
                        cnt_spelling += 1
            
                    text = text[0:offset] + error_start + text[offset:offset+leng] + we_end + text[offset+leng:]
                    conflict += 41
                    error = {}
                    error['id'] = cnt_error
                    error['id2'] = cnt_error * 1000
                    error['msg'] = messeage['message']
                    try:
                        error['dst'] = messeage['description']
                    except:
                        error['dst'] = ""
                    error['rep'] = messeage['replacements']
                    cnt_error += 1
                    result.append(error)
                point = {'grammar' : (1 - (cnt_grammar // sens))*100, 'spelling' : (1 - (cnt_spelling // tokens))*100, 'total' : int((1 - 0.5*(cnt_grammar // sens) + 0.5* (cnt_spelling // tokens))*100) }
            return render(request, 'writing_results.html', {'errors' : result, 'fixed' : text, 'point' : point})
        else:
            conn = MongoClient()
            db = conn.MyProject
            collection = db.Writing
            records = collection.find()
            topics = list(records)
            context = {'topic' : topics[article_id], 'form' : WritingContent()}
            return render(request, 'writing.html', context)
    else:    
        conn = MongoClient()
        db = conn.MyProject
        collection = db.Writing
        records = collection.find()
        topics = list(records)
        context = {'topic' : topics[article_id], 'form' : WritingContent()}
        return render(request, 'writing.html', context)

def index(request):
    return render(request, 'index.html',{})

def about(request):
    return render(request, 'about.html',{})  

def home_writing(request):
    return render(request, 'home_writing.html',{})  

def listening(request):
    return render(request, 'listening.html', {})

def speaking(request, article_id):
    conn = MongoClient()
    db = conn.MyProject
    collection = db.Speaking
    records = collection.find()
    topics = list(records)
    if request.method == "POST":
        mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
        sample_rate = 48000

        chunk_size = 2048
        r = sr.Recognizer() 

        mic_list = sr.Microphone.list_microphone_names() 
        for i, microphone_name in enumerate(mic_list): 
            if microphone_name == mic_name: 
                device_id = i

        print(topics[article_id - 1])
        transcript = topics[article_id - 1]['text']
        print(transcript)
        with sr.Microphone(sample_rate = sample_rate, chunk_size = chunk_size) as source: 
            r.adjust_for_ambient_noise(source) 
            print("Say Something")
            audio = r.listen(source)  
            try: 
                text = r.recognize_google(audio) 
                print("you said: " + text )
                saved_text = text
                transcript = " ".join(re.sub(r"[^a-zA-z0-9 ]", "", transcript.lower()).split())
                text = " ".join(re.sub(r"[^a-zA-z0-9 ]", "", text.lower()).split())
                tokens_script = transcript.split(" ")
                tokens_text = text.split(" ")
                correct_token = []
                i = -1
                tmp_index = 0
                subtract_index = 0
                while i + 1 < len(tokens_script) and tokens_script and tokens_text:
                    i = i + 1
                    word_A = tokens_script[i]
                    flag = True
                    for k in range(i-3, i+4):
                        if k >= 0 and k < len(tokens_text):
                            word_B = tokens_text[k]
                            if word_A == word_B:
                                tokens_script = tokens_script[i + 1:]
                                tokens_text = tokens_text[k + 1:]
                                correct_token.append((word_A, tmp_index, k + tmp_index + subtract_index))
                                i = -1
                                flag = False
                                break
                    if flag:
                        subtract_index -= 1
                    tmp_index += 1
                start_span = "<span style=\"color:green\">"
                end_span = "</span>"
                saved_text = saved_text.split()
                for _, _, index_text in correct_token:
                    saved_text[index_text] = start_span + saved_text[index_text] + end_span
                saved_text = " ".join(saved_text)
                return render(request, 'speaking.html', {'topic' : {'type' : 'article', 'text' : saved_text}})
            except sr.UnknownValueError: 
                print("Google Speech Recognition could not understand audio") 
            
            except sr.RequestError as e: 
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
        return render(request, 'speaking.html', {'topic' : topics[article_id - 1]})
    else:
        return render(request, 'speaking.html', {'topic' : topics[article_id - 1]})

@csrf_protect
def reading(request, article_id):
    conn = MongoClient()
    db = conn.MyProject
    translator = Translator()
    if request.method == "POST":
        form = PickupWords(request.POST)
        if form.is_valid():
            collection = db.Pickup
            text = form.cleaned_data['word']
            vi_text = translator.translate(text, dest="vi").text
            collection.insert_one({'user': 'admin', 'en' : text, 'vi' : vi_text})
            collection = db.Reading
            records = collection.find()
            topics = list(records)
            topic = topics[article_id - 1]
            en_text = re.sub(r"[A-Z]{1}[\.]", "</br> - ", topic['en'])
            topic['vi'] = re.sub(r"[A-Z]{1}[\.]", "</br> - ", topic['vi'])
            if 'words' in topic:
                for element in topic['words']:
                    en_word = element['en'].strip()
                    css_tag = '<span class="tool font-weight-bold" data-toggle="tooltip" title="' + element['vi'] + '">'
                    en_text = en_text.replace(en_word, css_tag + en_word + "</span>")
            topic['en'] = en_text
            return render(request, 'reading.html', {'topic' : topic, 'form' : PickupWords()})
    else:    
        collection = db.Reading
        records = collection.find()
        topics = list(records)
        topic = topics[article_id - 1]
        en_text = re.sub(r"[A-Z]{1}[\.]", "</br> - ", topic['en'])
        topic['vi'] = re.sub(r"[A-Z]{1}[\.]", "</br> - ", topic['vi'])
        if 'words' in topic:
            for element in topic['words']:
                en_word = element['en'].strip()
                css_tag = '<span class="tool font-weight-bold" data-toggle="tooltip" title="' + element['vi'] + '">'
                en_text = en_text.replace(en_word, css_tag + en_word + "</span>")
        topic['en'] = en_text
        return render(request, 'reading.html', {'topic' : topic, 'form' : PickupWords()})

def home_speaking(request):
    return render(request, 'home_speaking.html', {})