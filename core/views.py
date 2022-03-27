from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MusicalWork
from .serializers import MusicalWorkMetaDataFileSerializer, MusicalWorkSerializer


class WorksAPIView(APIView):
    queryset = MusicalWork.objects.none()
    serializer_class = MusicalWorkMetaDataFileSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        works_file = serializer.save()
        return Response(data={"file": works_file.file.name})

    def get(self, request: Request, *args, **kwargs):
        data = dict()

        iswc = request.query_params.get("iswc")

        if iswc is not None:
            work = MusicalWork.objects.filter(iswc=iswc).first()

            if work is not None:
                serializer = MusicalWorkSerializer(work)
                data = serializer.data

        return Response(data={"data": data})
