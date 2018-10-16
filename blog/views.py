from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .models import PostModel
from django.shortcuts import get_object_or_404
from .forms import PostalForm
from django.contrib import messages
from django.db.models import Q

def home(request):
    # return HttpResponse("<h1>Hello World</h1>")
    qs = PostModel.objects.all()

    if request.GET.get('search') is not None:
        qs = PostModel.objects.filter(
            Q(title__icontains=request.GET.get('search')) |
            Q(content__icontains=request.GET.get('search'))
            )


    context={
        'object_list':qs,
        'title':'List-View'
    }
    return render(request,'list-view.html',context)


def detail(request,id=None):

    qs = PostModel.objects.get(id=id)
    # qs = get_object_or_404(PostModel,id=id)
    #
    # try:
    #     qs = PostModel.objects.get(id=id)
    # except:
    #     raise Http404
    #
    # qs = PostModel.objects.filter(id=id)
    #
    # if not qs.exists():
    #     raise Http404


    context={
        'object':qs,
        'title':'Detail-View'
    }
    return render(request,'detail-view.html',context)



def create(request):
    form = PostalForm(request.POST or None)
    if form.is_valid():
        obj=form.save()
        messages.success(request,"new post is created!!")
        return redirect('blog:detail',id=obj.id)
    context={
        'form':form,
        'title':'Create View'
    }
    return render(request, 'create-view.html', context)


def update(request,id=None):

    form = PostalForm(request.POST or None,instance=PostModel.objects.get(id=id))
    if form.is_valid():
        obj = form.save()
        messages.success(request, "new post is updated!!")
        return redirect('blog:detail', id=obj.id)
    context = {
        'form': form,
        'title': 'Update View'
    }
    return render(request, 'updated-view.html', context)


def delete(request, id=None):
    qs = PostModel.objects.get(id=id)
    # form = PostalForm(request.POST or None, instance=PostModel.objects.get(id=id))
    if request.method == 'POST':
        qs.delete()
        messages.success(request, "new post is deleted!!")
        return redirect('blog:home')
    context = {
        'object': qs,
        'title': 'Delete View'
    }
    return render(request, 'delete-view.html', context)