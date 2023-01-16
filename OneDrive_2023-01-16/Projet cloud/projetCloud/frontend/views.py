from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import os
# Create your views here.

def index(request):
    user = User.objects.order_by('identifiant_secret')
    if user[0].isLogged == False:
        return Login_view(request)
    else:
        mydict = {'liste': range(1,51)}
        #return HttpResponse("Hello World")
        return render(request, 'search.html', context= mydict)
 
def Login_view(request):
    form = Login()
    
    if request.method == 'POST':
        form = Login(request.POST)

        if form.is_valid():
            print("VALIDATION SUCCESS!")
            print("Identifiant: "+ form.cleaned_data['identifiant_secret'])
            if request.POST.get('identifiant_secret') == "195.154.19.215":
                user = User.objects.all()[0]
                user.isLogged = True
                user.save()
                return SearchForm_view(request)
            form.clean()
            id = User.objects.all()[0].id
            
    
    return render(request, 'index.html',{'form':form})

    

def SearchForm_view(request, user = None):
    
    users = User.objects.order_by('identifiant_secret')
    path = "/Users/thierrynjike/Documents/Polytech Mons/MA2/MultiRetrievCloud/Projet cloud/projetCloud/frontend/static/images/mir_dataset/araignees/tarantula"
    liste = os.listdir(path)
    #print(liste)
    if user == None:
        user = users[0]
    tops = Top.objects.order_by('value')
    normes = Norme.objects.order_by('name')
    descripteurs = Descripteur.objects.order_by('id')
    
    if user.isLogged == False:
        return Login_view(request) 
    else:
        
        if request.method =="POST":
            if "Déconnexion" in request.POST and user != None:
                user = User.objects.all()[0]
                user.isLogged = False
                user.save()
                return SearchForm_view(request, user)
            elif "identifiant_secret" in request.POST:
                return render(request, 'search.html', {'descripteurs': descripteurs, 'tops':tops, 'normes':normes})
            elif "Rechercher" in request.POST:
                print("filename : ", request.POST.get('norme'))
                print("filename : ", request.POST.get('top'))
                print("filename : ", request.FILES['image_upload'])
                image = request.FILES['image_upload']

                return render(request, 'search.html', {'image': image, 'liste': liste, 'descripteurs': descripteurs, 'tops':tops, 'normes':normes})

                

        return render(request, 'search.html', {'liste': liste, 'descripteurs': descripteurs, 'tops':tops, 'normes':normes})


def LogoutUser(request, id):
    user = User.objects.get(id = id)
    user.setAttributes(False, "195.154.19.215")
    user.save
    
    return Login_view(request)

def LoginUser(request, id):
    user = User.objects.get(id = id)
    user.isLogged = False
    print(request.POST.get('identifiant_secret')) 
    if request.POST.get('identifiant_secret') == "195.154.19.215":
        user.isLogged = True
        user.save()
        

    return SearchForm_view(request, user)


def Recherche(request):
    norme = request.POST.get('norme')
    top = request.POST.get('top')
    filename = request.FILES('image_upload')
    
    