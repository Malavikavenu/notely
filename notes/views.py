from django.shortcuts import render

from notes.models import User,Task

from rest_framework.response import Response

from rest_framework.views import APIView

# generic CreateAPiView

from rest_framework import generics,authentication,permissions

from notes.serializers import UserSerializer,TaskSerializer

from notes.permissions import OwnerOnly



class UserCreationView(generics.CreateAPIView):

    serializer_class=UserSerializer


class TaskListCreateView(generics.ListCreateAPIView):

    serializer_class=TaskSerializer

    queryset=Task.objects.all()

    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    

    # def list(self, request, *args, **kwargs):
    #     qs=Task.objects.filter(owner=request.user)

    #     serializer_instance=TaskSerializer(qs,many=True)

    #     return Response(data=serializer_instance.data)
    
    #or

    def get_queryset(self):
        #lh:8000/api/tasks?category=business 
        qs=Task.objects.filter(owner=self.request.user)

        if "category" in self.request.query_params:

            category_value=self.request.query_params.get("category")

            qs=qs.filter(category=category_value)

#lh:8000/api/tasks?priority=low
        if "priority" in self.request.query_params:

            priority_value=self.request.query_params.get("priority")

            qs=qs.filter(priority=priority_value)

        # print(self.request.query_params)


        return qs
    

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset=Task.objects.all()

    serializer_class=TaskSerializer

    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]


from django.db.models import Count
class TaskSummaryApiView(APIView):

    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

   

    def get(self,request,*args,**kwargs):


        qs=Task.objects.filter(owner=request.user)

        category_summary=qs.values("category").annotate(count=Count('category'))

        status_summary=qs.values("status").annotate(count=Count('status'))

        priority_summary=qs.values("priority").annotate(count=Count('priority'))

        task_count=qs.count()

        context={
            "category summary":category_summary,
            "status summary":status_summary,
            "priority summary":priority_summary,
            "total_count":task_count
        }

        return Response(data=context)
    

            
#categories
#url:lh:8000/api/tasks/categories/

class CategoryListView(APIView):

    def get(self,request,*args,**kwargs):

        qs=Task.category_choices

        # st=set()
        # for tp in qs:
        #     for cat in tp:
        #         st.add(cat)
        #or

        st={cat for tp in qs for cat in tp}

        return Response(data=st)





