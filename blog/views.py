from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.http import HttpResponse,Http404
from .models import PostModel
from django.shortcuts import get_object_or_404
from .forms import PostalForm,Postaltest
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.views.generic.edit import FormMixin,FormView,ModelFormMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from blog.models import PostModel
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


@login_required
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




##### class based views

## TempalteView CBV






class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class UsingTemplateView(LoginRequiredMixin,TemplateView):
    template_name = 'about.html'

    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['title'] = 'About Page'
        return context

    # @method_decorator(login_required())
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)




class BlogListView(ListView):
    model = PostModel
    template_name = 'postmodel_list.html'


class BlogDetailView(ModelFormMixin,DetailView):
    # model = PostModel
    form_class = PostalForm
    template_name = 'detail-view.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='DetailCBV'
        context['buttontitle'] = 'Create'
        context['form']=self.get_form()
        # print(context)
        return context




    def get_success_url(self):
        return reverse('blog:detail2',kwargs={'id':self.kwargs.get('id')})

    def get_object(self, queryset=None):
        return PostModel.objects.get(id=self.kwargs.get('id'))

    # def post(self,request,*args,**kwargs):
    #     form = self.get_form()
    #     if form.is_valid():


    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            # print(self.object)
            self.object = self.get_object()
            # print(self.object)
            form = self.get_form()


            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        # print(self)

        return super().form_valid(form)

    def form_invalid(self, form):
        print(self)
        return super().form_invalid(form)



class BlogCreateView(SuccessMessageMixin,CreateView):

    # model = PostModel

    template_name = 'create-view.html'
    form_class = PostalForm

    success_url = '/'
    success_message = "%(title)s is created! with %(tete)s"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='createCBV'
        context['buttontitle'] = 'Create'
        print(context)
        return context

    def form_valid(self, form):
        form.instance.view_count = 23
        # messages.success(self.request,"the blog is created !")
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            tete=self.object.view_count,
        )


class MutipleobjectMixin(object):
    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        qs = self.model.objects.get(id=id)
        print(self.model)
        print(self.get_queryset())
        pass

class BlogUpdateView(UpdateView):
    # model = PostModel
    form_class = PostalForm
    template_name = 'create-view.html'
    # queryset = PostModel.objects.filter(title__icontains="ef")

    def get_success_url(self):
        return reverse('blog:home')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(kwargs)
        print(context)
        context['buttontitle']='Update'
        return context


    def get_object(self,queryset=None):
        return PostModel.objects.get(id=self.kwargs.get('id'))



class BlogDeleteView(DeleteView):
    form_class = PostalForm
    template_name = 'delete-view.html'

    def get_success_url(self):
        return reverse('blog:home')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buttontitle']='Delete'
        return context

    def get_object(self,queryset=None):
       return PostModel.objects.get(id=self.kwargs.get('id'))



## test Forms with Django


# def testform(request):
#     form = Postaltest(request.POST or None)
#     if form.is_valid():
#         form.save()
#     # if request.method =='POST':
#     #     form = Postaltest(request.POST)
#     #
#     # if request.method == 'GET':
#     #     form = Postaltest(age=500)
#     # if form.is_valid():
#     #     print(form.cleaned_data)
#     # print(request.GET.get("username"))
#     print(request.POST)
#     context={
#         'form':form
#     }
#     return render(request,'test_form.html',context)



def testform(request):
    form=PostalForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False)
        obj.view_count =999
        obj.save()


    if form.has_error:
        print(form.errors.as_json())

    data = form.errors.items()
    for key,value in data:
        print(key,value.as_text())

    context = {
            'form':form
        }
    return render(request,'test_form.html',context)