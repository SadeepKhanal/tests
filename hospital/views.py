from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PatientSerializer
from .models import Patient


class PatientListAPIView(APIView):

    def get(self, request):
        records = Patient.objects.all()
        serializer = PatientSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Patient registration completed',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            obj = Patient.objects.get(pk=pk)
            return obj
        except Patient.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response(
                {'error': 'Requested patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PatientSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response(
                {'error': 'Requested patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PatientSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Patient details updated',
                    'data': serializer.data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if obj is None:
            return Response(
                {'error': 'Requested patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        obj.delete()
        return Response(
            {'message': 'Patient record removed'},
            status=status.HTTP_204_NO_CONTENT
        )