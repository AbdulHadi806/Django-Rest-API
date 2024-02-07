from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from .models import Todo
from .forms import UserSignUpForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import TodoSerializer

# Todo functions
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Todo_create(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Todo Created"}, status=201)
    print("Serializer Errors:", serializer.errors)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
        todo.delete()
        return Response({"message": "Todo deleted successfully"}, status=204)
    except Todo.DoesNotExist:
        return Response({"error": "Todo not found"}, status=404)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def todo_completed(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
        todo.completed = not todo.completed
        todo.save()
        return Response({"message": "Todo marked as completed"}, status=200)
    except Todo.DoesNotExist:
        return Response({"error": "Todo not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_user_todos(request, pk):
    todos = Todo.objects.filter(user_id=pk)
    serializer = TodoSerializer(todos, many=True) 
    print(serializer.data)
    return Response(serializer.data, status=200)



# User functions
@api_view(['POST'])
def User_create(request):
      try:
        form = UserSignUpForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            User.objects.create_user(username=username, email=email, password=password)
            
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
      except:
          return Response({'message': 'Something went wrong, internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
@api_view(['POST'])
def user_login(request):
      form = UserSignUpForm(request.data)
      return authenticate_user(request, form)

def authenticate_user(request, form):
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        return process_authentication_result(request, user)
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def process_authentication_result(request, user):
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'User logged in successfully', 'token': token.key}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def user_logout(request):
    logout(request)
    return Response({'message': 'Logout successful'})

@api_view(['GET'])
def get_user_info(request):
    user = request.user
    
    if user.is_authenticated:
        user_details = {
            'username': user.username,
            'email': user.email,
            'id': user.id
        }
        return Response(user_details)
    else:
        return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)