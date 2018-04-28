from django.urls import path

from . import views

app_name = 'shopingcart'
urlpatterns = [
    # path('', views.HomeView.as_view(), name='home'),
    path('', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('jsondata/', views.DataView.as_view(), name='jsondata'),
    path('jsondata/<index>', views.BookDataView.as_view(), name='dataofbook'),
    path('data/<index>',views.IndividualDataView.as_view(), name='data'),
    path('cart',views.CartDataView.as_view(), name='datacart'),
    path('checkout/',views.CheckoutView.as_view(), name='checkout'),
    path('cartdata/',views.CartView.as_view(), name='cart'),
    path('deleteitem/<index>',views.DeleteItemView.as_view(), name='deleteitem'),
    path('placeorder/',views.PlaceOrderView.as_view(), name='placeorder'),
    path('logout/',views.logout, name='logout'),

   

]