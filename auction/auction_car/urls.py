from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'brands', BrandListApiView, basename='brand')
router.register(r'models', ModelListAPiView, basename='model')
router.register(r'cars', CarListApiView, basename='car')
router.register(r'car-detail', CarDetailApiView, basename='car-detail')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'auctions', AuctionListApiVIew, basename='auction')
router.register(r'bids', BidListApiView, basename='bid')
router.register(r'feedback', FeedBackListCreateAPIView, basename='feedback')


urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
