from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Auteur, Livre
from .serializers import AuteurSerializer, LivreSerializer


class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer

    @action(detail=True, methods=['get'])
    def livres(self, request, pk=None):
        auteur = self.get_object()
        livres = auteur.livres.all()
        serializer = LivreSerializer(livres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        return Response({
            'total_auteurs': Auteur.objects.count(),
            'total_livres': Livre.objects.count(),
        })


class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        qs = Livre.objects.filter(disponible=True)
        serializer = LivreSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def emprunter(self, request, pk=None):
        livre = self.get_object()
        if not livre.disponible:
            return Response(
                {'erreur': "Ce livre n'est pas disponible."},
                status=status.HTTP_400_BAD_REQUEST
            )
        livre.disponible = False
        livre.save()
        return Response({'message': f'"{livre.titre}" emprunté avec succès.'})

    @action(detail=True, methods=['post'])
    def rendre(self, request, pk=None):
        livre = self.get_object()
        livre.disponible = True
        livre.save()
        return Response({'message': f'"{livre.titre}" rendu avec succès.'})