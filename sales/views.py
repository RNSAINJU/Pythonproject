from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
# from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import employees
from .serializers import employeeSerializer

from django.views.decorators.csrf import csrf_exempt

class employeeList(APIView):
    def get(self,request):
        employees1=employees.objects.all()
        serializer=employeeSerializer(employees1, many=True)
        # return Response(serializer.data)
        return JsonResponse(serializer.data,safe=False)

    def post(self,request):
        data= JSONParser().parse(self.request)
        serializer=employeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

    def delete(self,request,pk):
        employee=get_object_or_404(employees.objects.all(), pk=pk)
        employee.delete()
        return HttpResponse(status=204)


# @csrf_exempt
# def employeelist(request,pk):
#     try:
#         employee=employees.objects.get(pk=pk)
#     except employee.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer=employeeSerializer(employee)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data= JSONParser().parse(request)
#         serializer=employeeSerializer(employee,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors,status=400)

    # elif request.method == 'DELETE':
    #     employee=employees.objects.get(pk=pk)
    #     employee.delete()
    #     return HttpResponse(status=204)
