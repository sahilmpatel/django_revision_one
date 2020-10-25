from django.shortcuts import render,HttpResponse
from .forms import details, file_upload, BankForm
from .upload_files import handle_uploaded_file
from .models import PersonDetails
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .serializers import PersonSerialize
from django.views.generic import TemplateView,ListView,CreateView,DetailView,UpdateView,DeleteView
from django.urls import reverse_lazy


# Create your views here.

# ..............class based view .........
class PersonAddView(CreateView):
    model = PersonDetails
    template_name = 'add_person.html'
    fields = ('name','email','phone_no','gender','address')
    success_url = reverse_lazy('PersonView')

class PersonView(ListView):
    model = PersonDetails
    template_name = 'persondetails_list.html'
    context_object_name = 'person'


class PersonViewById(DetailView):
    model = PersonDetails
    template_name = 'person_by_id.html'
    context_object_name = 'person'

class PersonUpdateView(UpdateView):
    model = PersonDetails
    template_name = 'update_person.html'
    context_object_name = 'person'
    fields = ('name', 'email', 'phone_no', 'gender', 'address')

    def get_success_url(self):
        return reverse_lazy('PersonViewById',kwargs={'pk':self.object.id})

class PersonDeleteView(DeleteView):
    model = PersonDetails
    template_name = 'delete_person.html'
    success_url = reverse_lazy('PersonView')


class HomeView(TemplateView):
    template_name = 'home.html'
    # def get_context_data(self, **kwargs):
    #     contex=super(HomeView, self).get_context_data()
    #     contex['user_list']=




# ....... function based view .........



def home_view(request):
    temp = 'abc.html'
    form = BankForm()
    return render(request,temp,{'form':form})

def details_view(request):
    temp = 'details.html'
    form = details()
    return render(request,temp,{'form':form})

def file_upload_view(request):
    temp = 'file_upload.html'
    if request.method == 'POST':
        form = file_upload(request.POST or None, request.FILES or None)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("File uploaded successfuly")
    else:
        form = file_upload()

    return render(request,temp,{'form':form})

def session_set_exp(request):
    per = PersonDetails.objects.all()
    name,email,phone_no,address,gender = [],[],[],[],[]
    for i in per.values():

        name.append(i['name'])
        email.append(i['email'])
        phone_no.append(i['phone_no'])
        address.append(i['address'])
        gender.append(i['gender'])

    # values  = {
    #     "name" :name,
    #     "email" : email,
    #     "phone_no" : phone_no,
    #     "address" : address
    # }
    request.session['name'] = name
    request.session['email'] = email
    request.session['phone_no'] = phone_no
    request.session['address'] = address
    request.session['gender'] = gender

    return HttpResponse("session set ..")

def session_get_exp(request):

    name = request.session.get('name')
    email = request.session.get('email')
    phone_no = request.session.get('phone_no')
    address = request.session.get('address')
    gender = request.session.get('gender')
    values = {
        "name": name,
        "email": email,
        "phone_no": phone_no,
        "address": address,
        "gender":gender
    }


    return JsonResponse(values)



def get_data_by_id(request,id):
    per = PersonDetails.objects.get(id=id)

    values = {
        "name" :per.name,
        "email" :per.email,
        "phone_no" : per.phone_no,
        "address" : per.address,
        "gender" : per.gender
    }
    dt = per.name
    resp = HttpResponse('cookies ....')
    resp.set_cookie('name',dt)
    # return JsonResponse(values)
    return resp

def getcookie(request):
    name = request.COOKIES['name']
    return HttpResponse("Hi"+ " "+name )



@csrf_exempt
def person_view(request):
    if request.method == 'GET':
        per = PersonDetails.objects.all()
        serialize = PersonSerialize(per,many=True)
        return JsonResponse(serialize.data,safe=False)


@csrf_exempt
def person_view_by_id(request,id):
    if request.method == 'GET':
        per = PersonDetails.objects.get(id=id)
        serialize = PersonSerialize(per)
        return JsonResponse(serialize.data)

@csrf_exempt
def add_person_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serialize = PersonSerialize(data=data)
        if serialize.is_valid():
            serialize.save()
            return JsonResponse("Created ...",safe=False)
        return JsonResponse("something wrong ...",safe=False)


@csrf_exempt
def update_person_view(request,id):
    try:
        per = PersonDetails.objects.get(id=id)
    except Exception as e:
        return JsonResponse(e)


    if request.method == 'GET':

        serialize = PersonSerialize(per)
        return JsonResponse(serialize.data,safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serialize = PersonSerialize(per,data=data)
        if serialize.is_valid():
            serialize.save()
            return JsonResponse("Updated ..",safe=False)
        return JsonResponse("something wrong ...",safe=False)

    elif request.method == 'DELETE':
        per.delete()
        return JsonResponse("Deleted ..",safe=False)



