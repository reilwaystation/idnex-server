from django.urls import path
from .views import PersonList, PersonDetail, AddressList, AddressDetail, OwnershipList, OwnershipDetail

urlpatterns = [
    path('address', AddressList.as_view()),
    path('ownerhip', OwnershipList.as_view()),
    path('person', PersonList.as_view()),
    path('person/<person>', PersonDetail.as_view()),
    path('address/<address>', AddressDetail.as_view()),
    path('ownerhip/<ownerhip>', OwnershipDetail.as_view()),
]
