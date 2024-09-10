import logging
import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewTaskForm(forms.Form):
    title = forms.CharField(label="New Encyclopedia Title")
    content = forms.CharField(label="New Encyclopedia Content   ")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

class EditTaskForm(forms.Form):
    content = forms.CharField(label="New Encyclopedia Content   ")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    title = title.lower() 
    content = util.get_entry(title)

    if content:
        return render(request, 'encyclopedia/entry.html', {'content': content, 'title': title.lower()})
    else:
        return HttpResponse("Page not found", status=404)

def search(request):
    q = request.GET.get('q')
    content = util.get_entry(q)
    if content:
        return redirect('encyclopedia:entry', title=q)
    else:
        entries = util.list_entries()
        filtered_entries = [entry for entry in entries if q.lower() in entry.lower()]
        # logging.info(f"Content for entries '{filtered_entries}'")   
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
            title = form.cleaned_data["title"].lower()
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": "An encyclopedia entry with this title already exists."
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewTaskForm()
        })
    

def edit(request, title):
    if request.method == "POST":
        form = EditTaskForm(request.POST)
       
        if form.is_valid():
            content = form.cleaned_data["content"]
            logging.info(f"form::: '{content}'")   
            if content.strip():
                util.save_entry(title, content)
                return redirect('encyclopedia:entry', title=title)
            else:
                form.add_error('content', 'Content cannot be empty.')
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title
        })
    else:
        logging.info(f"form>>> get request ")   
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })
        form = NewTaskForm(initial={"title": title, "content": content})
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title
        })
    
def random_page(request):
    entries = util.list_entries()
    if entries:
        current_title = request.GET.get('current_title')
        logging.info(f"current_title::: '{current_title}'")
        if current_title:
            entries = [entry for entry in entries if entry.lower() != current_title.lower()]
        if not entries:
            return render(request, "encyclopedia/error.html", {
                "message": "No other entries found."
            })
        random_entry = random.choice(entries)
        # return HttpResponseRedirect(reverse("encyclopedia:entry", args=[random_entry.lower()]))
        return redirect('encyclopedia:entry', title=random_entry.lower())
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries found."
        })