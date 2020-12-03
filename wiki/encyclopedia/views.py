from django.shortcuts import render, redirect

from . import util
from markdown2 import markdown
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def title(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        content = "##Page not found"
    return render(request, "encyclopedia/title.html", {
        "content": markdown(content),
        "title": title
        })



def search(request):
    search = request.GET.get('q').strip()
    if search in util.list_entries():
        return redirect("title", title=search)
    return render(request, "encyclopedia/search.html", {"entries": util.search(search), "q": search,})
        



def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/add.html", {"message": "Can't save empty field", 
                                                             "title": title,
                                                             "content": content})
        if title in util.list_entries():
            return render(request, "encyclopedia/add.html", {"message": "Title already exist. Try another one",
                                                             "title": title,
                                                             "content": content})
        util.save_entry(title, content)
        return redirect("title", title=title)
    return render(request, "encyclopedia/add.html")
            



def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {"error": "404 not found"})
    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Can't save empty field", 
                                                              "title": title,
                                                              "content": content})
        util.save_entry(title, content)
        return redirect("title", title=title )
    return render(request, "encyclopedia/edit.html", {"title": title, "content": content})
        

def random(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries)-1)].strip()
    return redirect("title", title=title)