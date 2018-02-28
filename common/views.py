# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# # Create your views here.


# class BaseListView(APIView):
#     """
#         Fetch all instances of a resource or create new resource
#     """

#     def get(self, request):
#         results = self.model.objects.all()
#         serializer = self.model_serializer(results, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = self.model_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(created_by=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BaseDetailView(APIView):
#     """
#     Update, Delete, or View a resource
#     """

#     def get_object(self, pk):
#         return get_object_or_404(self.model, pk=pk)

#     def get(self, request, pk):
#         serializer = self.model_serializer(self.get_object(pk))
#         return Response(serializer.data)

#     def put(self, request, pk):
#         serializer = self.model_serializer(
#             self.get_object(pk), data=request.data)
#         if serializer.is_valid():
#             serializer.save(edited_by=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         item = self.get_object(pk)
#         item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
