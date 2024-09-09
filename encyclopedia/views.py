import logging
from django.shortcuts import render
from django.http import HttpResponse
from . import util

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    # logging.info(f"Content for title '{title}': {content}")
    if content:
        return render(request, 'encyclopedia/entry.html', {'content': content, 'title': title})
    else:
        return HttpResponse("Page not found", status=404)