from django.shortcuts import render, redirect
from django.http import request 
from app.forms import forms_Database
from app.models import Database
from app.serializers import Serializer_Database
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView 
from rest_framework import serializers ,status


# render data from database 
def database(request):
    database=Database.objects.all()
    if database.exists():
        return render(request,"app/templates/database.html", {"data": database})
    else:
        return render(request,"app/templates/database.html", {"data": "No data yet"})


def insert(request):
    if request.method=="POST":
        form=forms_Database(request.POST)
        if form.is_valid():
            form.save()
    else:
        form=forms_Database()
    return render(request,"app/templates/insert.html", {"form": form})


def delete(request):
    if request.method=="POST":
        selected_id=request.POST.getlist("Select_id")
        if selected_id:
            Database.objects.filter(id__in=selected_id).delete()
        return redirect("delete")

    database=Database.objects.all()
    return render(request,"app/templates/delete.html", {"data": database})

# def update(request):
#     database=Database.objects.all()
#     if database.exists():
#         return render(request,"app/templates/update.html", {"data": database})
#     else:
#         database=Database()
#         return render(request,"app/templates/update.html", {"data": database})

def update(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("Select_id")
        for data_id in selected_ids:
            data = Database.objects.get(id=data_id)
            data.Name = request.POST.get("Name")
            data.Gender = request.POST.get("Gender")
            data.Mobile = request.POST.get("Mobile")
            data.Address = request.POST.get("Address")
            data.save()
        return redirect("update")
    
    data = Database.objects.all()
    return render(request, "app/templates/update.html", {"data": data})



#___________________________________________________________REST FRAMEWORK______________________________________________________________________________________________

@api_view(["POST"])
def rest_insert(request):
    if request.method=="POST":
        serializer=Serializer_Database(data=request.data, many=True) # for bulk
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"message": "Data Saved Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Post methos is initializing"})


@api_view(["GET"])
def rest_database(request):
    data=Database.objects.all()
    serializer=Serializer_Database(data, many=True)
    return Response(serializer.data)

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, ListCreateAPIView

# class rest_update(UpdateAPIView):
#     queryset = Database.objects.all()
#     serializer_class = Serializer_Database

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# update rest_framework using url with put id no's http://127.0.0.1:8000/rest_update/13
class rest_update(UpdateAPIView):
    queryset = Database.objects.all()
    serializer_class = Serializer_Database  # Use this for DRF compatibility

    def patch(self, request, *args, **kwargs):
        serializer1 = Serializer_Database(data=request.data, many=True)  # Assume you're sending a list
        if serializer1.is_valid():
            for item in serializer1.validated_data:
                selected_id = item.get('id')
                try:
                    instance = Database.objects.get(id=selected_id)
                except Database.DoesNotExist:
                    continue  # Skip if record not found

                serializer_instance = Serializer_Database(instance, data=item, partial=True)
                if serializer_instance.is_valid():
                    serializer_instance.save()
            return Response({"message": "Records updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)




class rest_delete(DestroyAPIView):
    queryset = Database.objects.all()
    serializer_class = Serializer_Database

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




