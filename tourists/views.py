from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import Tourist, TouristCard
from .serializers import TouristSerializer, TouristCardSerializer


class TouristInfo(RetrieveUpdateAPIView):
    """
    Update/Get a tourist info.
    GET: get a tourist by ID parameter (tourist_pk) in url.
    PUT: update a tourist info providing new json data body for the tourist.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = TouristSerializer
    # permission_classes = (permissions.IsAdminUser,)

    def get_object(self):
        return Tourist.objects.get(pk=self.kwargs.get('tourist_pk'))


class TouristCardInfo(RetrieveUpdateAPIView, CreateAPIView):
    """
    Update/Get/Add a tourist card.
    GET: get a tourist card info by its tourist card pk.
    PUT: update a tourist card info with itself data.
    POST: create a new tourist card providing all necessary data.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = TouristCardSerializer

    def get_object(self):
        if self.request.method == 'GET':
            tourist_card_pk = self.request.query_params.get('tourist_card_pk')
        elif self.request.method == 'PUT':
            tourist_card_pk = self.request.data.get('tourist_card_pk')
        return TouristCard.objects.get(pk=tourist_card_pk)
