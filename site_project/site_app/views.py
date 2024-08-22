from django.shortcuts import render

posts = [
    {
        'author': 'Админ',
        'title': 'Это первый пост',
        'content': 'Содержание первого поста.',
        'image': 'image.jpg',
        'date_posted': '22 августа, 2024'
    },
    {
        'author': 'Пользователь',
        'title': 'Это второй пост',
        'content': 'Подробное содержание второго поста.',
        'image': 'image.jpg',
        'date_posted': '22 августа, 2024'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request,
                  'site/home.html',
                  context)


def about(request):
    return render(request,
                  'site/about.html',
                  {'title': 'О распознавании котиков'})