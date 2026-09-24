from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileListAPIView, CategoryListAPIVew,
                    SubCategoryListAPIew, ProductListAPIView,
                    ReviewViewSet, ProductDetailAPIView,
                    CategoryDetailAPIVew, SubCategoryDetailAPIVew,
                    UserProfileEditAPIView, RegisterView, CustomLoginView,
                    LogoutView, CartItemViewSet, CartAPIView, FavoriteItemViewSet,
                    FavoriteAPIView)

router = routers.DefaultRouter()
router.register(r'review', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('category/', CategoryListAPIVew.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIVew.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIew.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIVew.as_view(), name='subcategory_detail'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileEditAPIView.as_view(), name='user_user'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', CustomLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('cart/', CartAPIView.as_view(), name='cart_detail'),
    path('cart_item/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart_item/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('favorite/', FavoriteAPIView.as_view(), name='favorite_detail'),
    path('favorite_item/', FavoriteItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('favorite_item/<int:pk>', FavoriteItemViewSet.as_view({'delete': 'destroy'}))



]