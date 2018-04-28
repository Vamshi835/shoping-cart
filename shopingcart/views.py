from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.views import generic
from .forms import LoginForm,RegisterForm
import json
from .models import Register,Cart
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext


class HomeView(generic.TemplateView):
	template_name="shopingcart/home.html"

	def get(self,request):
		form=LoginForm()

		return render(request,self.template_name,{'form':form})


class RegisterView(generic.TemplateView):
	model=Register
	template_name="shopingcart/register.html"

	def get(self,request):
		form=RegisterForm()
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form=RegisterForm(request.POST)
		if form.is_valid():
			name=form.cleaned_data['name']
			email=form.cleaned_data['email']
			password=form.cleaned_data['password']
			repassword=form.cleaned_data['repassword']
			phone_no=form.cleaned_data['phone_no']
			q1=Register.objects.filter(email=email).get()
			if q1!=None:
				msg="User already exist....."
				args={'form':form,'error':msg}
				return render(request,self.template_name,args)
			elif password==repassword:
				Reg=Register(Fullname=name,email=email,password=password,phone=phone_no)
				Reg.save()
				home=HomeView()
				return redirect('shopingcart:login')
			else:
				msg="Please enter correct password"
				args={'form':form,'error':msg}
				return render(request,self.template_name,args)



class LoginView(generic.TemplateView):
	model=Register
	template_name="shopingcart/login.html"

	def get(self,request):
		if request.session.has_key('username'):
		  	username = request.session['username']
		  	q2=Cart.objects.filter(email=username).count()
		  	request.session['cart_items']=q2
		  	return render(request,'shopingcart/page.html',{"username" : username})
		return render(request,self.template_name)

	def post(self,request):
		if request.method=="POST":
			username=request.POST['Username']
			password=request.POST['password']
			request.session['username'] = username
			q1=Register.objects.get(email=username)
			if password==q1.password:
				q2=Cart.objects.filter(email=username).count()
				request.session['cart_items']=q2
				return render(request,'shopingcart/page.html',{"username" : username})
			else:
				msg="Please enter correct UserName and Password"
				return render(request,self.template_name,{'error':msg})


class DataView(generic.TemplateView):
	template_name="shopingcart/page.html"

	def get(self,request):
		json_data=json.loads(open('shopingcart/static/books.json').read())
		return HttpResponse(json.dumps(json_data))

	def post(self,request):
		return ""

class BookDataView(generic.TemplateView):
	template_name="shopingcart/individualpage.html"

	def get(self,request,index):
		index=int(index)
		json_data=json.loads(open('shopingcart/static/books.json').read())
		data=json_data['items'][index]
		return HttpResponse(json.dumps(data))


class CartDataView(generic.TemplateView):
	template_name="shopingcart/individualpage.html"

	def post(self,request):
		bookid=request.POST['bookid']
		name=request.POST['name']
		price=request.POST['price']
		index=request.POST['index']
		email=request.session['username']
		try:
			q1=Cart.objects.get(email=email,BookId=bookid)
		except Cart.DoesNotExist:
			q1=None
		if q1!=None:
			q1.Quantity=q1.Quantity+1
			q1.save()
			q2=Cart.objects.filter(email=email).count()
			request.session['cart_items']=q2
			return HttpResponse(q2)
		else:
			data=Cart(email=email,BookName=name,BookId=bookid,Index=index,Price=price)
			data.save()
			q2=Cart.objects.filter(email=email).count()
			request.session['cart_items']=q2
			return HttpResponse(q2)


class IndividualDataView(generic.TemplateView):
	template_name="shopingcart/individualpage.html"

	def get(self,request,index):
		args={
		'username':request.session['username']
		}
		return render(request,self.template_name,args,)


class CartView(generic.TemplateView):
	template_name="shopingcart/cartpage.html"
	model=Cart
	
	def get(self,request):
		email=request.session['username']
		cartdata=Cart.objects.filter(email=email).all()
		data=[]
		json_data=json.loads(open('shopingcart/static/books.json').read())
		for cart in cartdata:
			index=int(cart.Index)
			item=json_data['items'][index]
			item['quantity']=cart.Quantity
			item['amount']=round((int(cart.Quantity)*cart.Price),2)
			item['index']=index
			data.append(item)
		return render(request,self.template_name,{'data':data})


class CheckoutView(generic.ListView):
	template_name="shopingcart/checkoutpage.html"
	model=Cart
	context_object_name = 'checkout_list'

	def get_queryset(self):
		email=self.request.session['username']
		return Cart.objects.filter(email=email).all()

class DeleteItemView(generic.TemplateView):
	template_name="shopingcart/cartpage.html"
	model=Cart
	
	def get(self,request,index):
		email=request.session['username']
		deleteitem=Cart.objects.filter(email=email,Index=index).delete()
		q1=Cart.objects.filter(email=email).count()
		request.session['cart_items']=q1
		return redirect("shopingcart:cart")

class PlaceOrderView(generic.TemplateView):
	template_name="shopingcart/placeorder.html"

	def get(self,request):
		email=request.session['username']
		deleteitem=Cart.objects.filter(email=email).delete()
		q1=Cart.objects.filter(email=email).count()
		request.session['cart_items']=q1
		return render(request,self.template_name)

def logout(request):
	request.session.flush()
	return redirect("shopingcart:login")
