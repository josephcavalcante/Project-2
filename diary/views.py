from django.shortcuts import render, redirect
from .models import Diary, People
from django.db.models import Count
from datetime import datetime, timedelta

def index(request):
    texts = Diary.objects.all().order_by('-date')[:3]
    people_with_counting = People.objects.annotate(amount_diaries=Count('diary'))
    names = [person.name for person in people_with_counting]
    amount = [person.amount_diaries for person in people_with_counting]
    tags_with_counting = Diary.objects.values('tags').annotate(total_diaries=Count('id'))
    tags = [entry['tags'] for entry in tags_with_counting]
    total_diaries = [entry['total_diaries'] for entry in tags_with_counting]
    return render(request, 'diary/index.html', {'texts': texts, 'names': names, 'amount': amount, 'tags': tags, 'total_diaries': total_diaries})

def write(request):
    if request.method == 'GET':
        people_list = People.objects.all()
        return render(request, 'diary/write.html', {'people': people_list})
    elif request.method == 'POST':
        title = request.POST.get('title')
        tags = request.POST.getlist('tags')
        people_ids = request.POST.getlist('people')
        text = request.POST.get('text')
        
        if len(title.strip()) == 0 or len(text.strip()) == 0:
            return render(request, 'diary/write.html', {'message': 'Please fill in all fields.'})
        
        diary_entry = Diary(
            title=title,
            text=text,
        )
        diary_entry.set_tags(tags)
        diary_entry.save()
        
        people_list = People.objects.filter(id__in=people_ids)
        diary_entry.people.add(*people_list)
        
        return render(request, 'diary/write.html', {'message': 'Your diary has been saved!'})

def people_view(request):
    if request.method == 'GET':
        people_list = People.objects.all()
        return render(request, 'diary/people.html', {'people': people_list})
    elif request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        new_person = People(name=name, image=image)
        new_person.save()
        return redirect('people')

def day(request):
    date = request.GET.get('date')
    date_format = datetime.strptime(date, '%Y-%m-%d')
    diaries = Diary.objects.filter(date__gte=date_format).filter(date__lte=date_format + timedelta(days=1))

    return render(request, 'diary/day.html', {'diaries': diaries, 'total': diaries.count(), 'date': date})

def delete_day(request):
    day = datetime.strptime(request.GET.get('date'), '%Y-%m-%d')
    diaries = Diary.objects.filter(date__gte=day).filter(date__lte=day + timedelta(days=1))
    diaries.delete()
    return redirect('write')