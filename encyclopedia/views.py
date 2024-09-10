import logging
from django.shortcuts import redirect, render
from django.http import HttpResponse
from . import util

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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