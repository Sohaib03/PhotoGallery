import photos
from django.shortcuts import render, redirect
from .models import Category, Photo

def gallery(request):

    category = request.GET.get('category')

    if category==None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name__contains=category[1:-1])


    categories = Category.objects.all()
    context = {'categories' : categories, 'photos' : photos}
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, key):
    photo = Photo.objects.get(id=key)
    context = {
        'photo' : photo,
    }
    return render(request, 'photos/photo.html', context)




def addPhoto(request):

    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('Image')


        if data['Category'] != 'none':
            category = Category.objects.get(id=data['Category'])
        elif data['NewCategory'] != '':
            category, created = Category.objects.get_or_create(name=data['NewCategory'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['Description'],
            image=image
        )


        return redirect('gallery')
    return render(request, 'photos/add.html', context)
