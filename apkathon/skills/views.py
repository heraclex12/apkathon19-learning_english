from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from django import forms
from django.views.decorators.csrf import csrf_protect
from grammarbot import GrammarBotClient

# Create your views here.
class WritingContent(forms.Form):
    text = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control'}), label='' )



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
    return render(request, 'about.html',{})  