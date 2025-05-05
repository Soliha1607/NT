import datetime
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView, \
    CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from erp.models import Category, Course, Student, Homework, Video
from .serializers import CategoryModelSerializer, CourseModelSerializer, StudentModelSerializer, HomeworkSerializer, \
    VideoSerializer
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import permissions, status
from erp.permissions import CanEditWithinSpecialTime
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# Create your views here.

class CategoryListCreateApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        queryset = Category.objects.all().annotate(course_count=Count('courses'))
        return queryset


class CategoryDetailAPiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    lookup_field = 'pk'


class CourseListCreateApiView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]


class StudentGenericApiView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializers = self.get_serializer(products, many=True)
        return Response(serializers.data)


class CourseListByCategory(GenericAPIView):
    serializer_class = CourseModelSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Course.objects.filter(category=category_id)
        return Course.objects.none()

    def get(self, request):
        students = self.get_queryset()
        serializers = self.get_serializer(students, many=True)
        return Response(serializers.data)


class HomeworkCreateAPIView(CreateAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class VideoListCReateApiView(ListCreateAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class VideoDetailAPiView(RetrieveUpdateDestroyAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    permission_classes = [CanEditWithinSpecialTime]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            access_token_exp = access_token['exp']
            current_time = datetime.datetime.utcnow()
            exp_time = datetime.datetime.fromtimestamp(access_token_exp)
            expires_in = (exp_time - current_time).total_seconds()

            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'expires_in': int(expires_in),
                'expires_at': exp_time.isoformat() + 'Z',
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)