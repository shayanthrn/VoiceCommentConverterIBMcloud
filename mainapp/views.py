from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from .models import *
from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1, LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions



#speech to text api key = QlJZzVYlb1TWo0KIfyXBGpzgAQvxkU-U28OB3G75lJ57
# url value = https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/78a7d230-f0f1-42e3-8e9b-f5701de02223

#natural lan.. api key = Wkmdn7Ya2_xf6S7265SzBAfaTm_cC-dUzwuLNj3vgXVw
#url value = https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/75db1c41-901f-4588-a4a9-270b6eb3c354

#lang translator api key = EmKWWuZif-qv1NZ5CCnJkn2Hd2S0RNiG-zRFeKaHuU2g
#url value = https://api.us-south.language-translator.watson.cloud.ibm.com/instances/448f7a1b-3ead-48ed-a303-f2b5010e9a27

class listofmovies(View):

    def get(self,request):
        posts = Post.objects.all()
        context = {'posts' : posts}
        return render(request,"mainapp/index.html",context)
    
    def post(self,request):
        return HttpResponseBadRequest('This view can not handle method POST', status=405)

class selectlang(View):
    def get(self,request,id):
        return render(request,"mainapp/selectlang.html",context={'id':id})
    
    def post(self,request,id):
        return HttpResponseBadRequest('This view can not handle method POST', status=405)


class listofcomments(View):
    def get(self,request,id,lang):
        comments = Comment.objects.filter(moviename_id=id)
        if(lang=="EN"):
            comments = Comment.objects.filter(moviename_id=id)
            context = {'comments' : comments}
            return render(request,"mainapp/comments.html",context)
        else:
            authenticator = IAMAuthenticator('EmKWWuZif-qv1NZ5CCnJkn2Hd2S0RNiG-zRFeKaHuU2g')
            language_translator = LanguageTranslatorV3(
                version='2018-05-01',
                authenticator=authenticator
            )
            modelid = 'en-'+lang.lower()
            language_translator.set_service_url('https://api.us-south.language-translator.watson.cloud.ibm.com/instances/448f7a1b-3ead-48ed-a303-f2b5010e9a27')
            for comment in comments:
                content= comment.content
                translation = language_translator.translate(
                    text=content,
                    model_id=modelid).get_result()['translations'][0]['translation']
                comment.content = translation
            context = {'comments' : comments}
            return render(request,"mainapp/comments.html",context)
    
    def post(self,request):
        return HttpResponseBadRequest('This view can not handle method POST', status=405)

class uploadvoicecomment(View):
    def get(self,request,id):
        return HttpResponseBadRequest('This view can not handle method GET', status=405)

    def post(self,request,id):
        uploadwav = request.FILES['voice']
        username =  request.POST['name']

        authenticator_stotext = IAMAuthenticator('QlJZzVYlb1TWo0KIfyXBGpzgAQvxkU-U28OB3G75lJ57')
        speech_to_text = SpeechToTextV1(
            authenticator=authenticator_stotext
        )
        speech_to_text.set_service_url('https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/78a7d230-f0f1-42e3-8e9b-f5701de02223')


        rawtext = speech_to_text.recognize(
        audio=uploadwav.open(),
        content_type='audio/wav',
        model='en-US_BroadbandModel').get_result()['results'][0]['alternatives'][0]['transcript']

        authenticator_natural = IAMAuthenticator('Wkmdn7Ya2_xf6S7265SzBAfaTm_cC-dUzwuLNj3vgXVw')
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=authenticator_natural
        )
        natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/75db1c41-901f-4588-a4a9-270b6eb3c354')
        dictofvalues = natural_language_understanding.analyze(
            text=rawtext,
            features=Features(emotion=EmotionOptions())).get_result()['emotion']['document']['emotion']
        angerlevel = dictofvalues['anger']
        disgustlevel = dictofvalues['disgust']
        if(angerlevel>0.7 or disgustlevel>0.7):
            return HttpResponse("Your comment is inappropriate!")
        else:
            comment = Comment.objects.create(content=rawtext,username=username,moviename_id=id)
            return redirect('main')