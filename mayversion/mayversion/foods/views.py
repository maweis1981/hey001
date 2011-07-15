from django.shortcuts import render_to_response, get_object_or_404,HttpResponse,get_list_or_404
from django.http import HttpResponse
from foods.forms import UploadFoodForm
from foods.models import Foods

def handle_uploaded_file(f):
    destination = open('/Users/peter/Desktop/food.jpg', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def upload(request):
    return render_to_response('foods/upload.html', locals())

def uploadPhoto(request):
    if request.method == 'POST':
        form = UploadFoodForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            # handle_uploaded_file(request.FILES['photo'])
            form.save(1)
            return HttpResponse('done')
        else:
            return HttpResponse('form not valid')
    else:
        form = UploadFoodForm()
    return HttpResponse('ok')

def uploadAvatar(request):
    if request.method == 'POST':

        # handle_uploaded_file(request.FILES['photo'])

        food = Foods()
        food.set_user_id(1)

        food.name = 'food'
        food.price = '3.20'
        # f = open('/Users/peter/Desktop/food.jpg','wb+')
        food.photo.save('aaa.jpg',request.FILES['photo'])
        food.save()
    return HttpResponse('ok')



def showFoods(request):
    foods = Foods.objects.order_by('-create_datetime')
    return render_to_response('foods/all.html',locals())
