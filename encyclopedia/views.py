import logging
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django import forms
from . import util

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewTaskForm(forms.Form):
    title = forms.CharField(label="New Encyclopedia Title")
    content = forms.CharField(label="New Encyclopedia Content   ")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)

    if content:
        return render(request, 'encyclopedia/entry.html', {'content': content, 'title': title})
    else:
        return HttpResponse("Page not found", status=404)

def search(request):
    q = request.GET.get('q')
    content = util.get_entry(q)
    if content:
        return redirect('entry', title=q)
    else:
        entries = util.list_entries()
        filtered_entries = [entry for entry in entries if q.lower() in entry.lower()]
        logging.info(f"Content for entries '{filtered_entries}'")   
        return render(request, 'encyclopedia/search.html', {'entries': filtered_entries})

# def new(request):
#     return render(request, 'encyclopedia/new.html')

# def add(request):
#     title = request.POST.get('title')
#     content = request.POST.get('content')
#     util.save_entry(title, content)
#     return redirect('entry', title=title)

def new(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": "An encyclopedia entry with this title already exists."
                })
            else:
                util.save_entry(title, content)
                return redirect('entry', title=title)
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewTaskForm()
        })