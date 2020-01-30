from rest_framework import viewsets, response
from apps.person.serializers import PersonListSerializer, PersonDetailSerializer, PersonCompareSerializer
from apps.person.models import Person
from rest_framework.decorators import action
from apps.person.utils import euclidean


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return PersonListSerializer
        elif self.action == 'compare':
            return PersonCompareSerializer
        else:
            return PersonDetailSerializer

    @action(detail=False, methods=['post'], name='Compare persons')
    def compare(self, request):
        serializer = PersonCompareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        p1, p2 = serializer.validated_data['person1'], serializer.validated_data['person2']
        return response.Response({'result': euclidean(p1.vector, p2.vector)})
