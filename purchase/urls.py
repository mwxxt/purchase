from django.urls import path
from .views import *

urlpatterns = [
    path('purchase-types/', PurchaseTypeAPIView.as_view()),
    path('purchases/', PurchaseAPIView.as_view()),
    path('purchase/<int:pk>/', PurchaseDetailAPIView.as_view()),
    path('closed-contracts/', ClosedContractsListAPIView.as_view()),
    path('legal-act/', LegalActListCreate.as_view()),
    path('legal-act/<int:pk>/', LegalActUpdateDestroy.as_view()),
    path('contact-info/', ContactInfoListCreate.as_view()),
    path('contact-info/<int:pk>/', ContactInfoUpdateDestroy.as_view()),

]