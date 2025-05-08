import datetime

from django.core.cache import cache
from rest_framework.generics import ListCreateAPIView, GenericAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView
from rest_framework.views import APIView
from erp.models import Category, Course, Student, Homework, Video
from .serializers import CategoryModelSerializer, CourseModelSerializer, StudentModelSerializer, HomeworkSerializer, \
    VideoSerializer
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# Create your views here.

class CategoryListCreateApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

    def get_queryset(self):
        key = 'categories'
        queryset = cache.get(key)
        if queryset:
            return queryset

        queryset = Category.objects.all().annotate(course_count=Count('courses'))
        cache.set(key, queryset, timeout=None)
        return queryset


class CategoryDetailAPiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        key = f'categories-{self.kwargs["pk"]}'
        queryset = cache.get(key)
        if queryset:
            return queryset
        queryset = Category.objects.filter(courses=self.kwargs['pk'])
        cache.set(key, queryset, timeout=None)
        return queryset


class CourseListCreateApiView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer

    def get_queryset(self):
        key = f'course'
        queryset = cache.get(key)
        if queryset:
            return queryset
        queryset = Course.objects.all().select_related('category')
        cache.set(key, queryset, timeout=None)
        return queryset


class StudentGenericApiView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, *args, **kwargs):
        key = 'students'
        serializers = cache.get(key)
        if serializers:
            return Response(serializers.data, status=status.HTTP_200_OK)
        products = self.get_queryset()
        serializers = self.get_serializer(products, many=True)
        cache.set(key, serializers, timeout=None)
        return Response(serializers.data)


class CourseListByCategory(ListAPIView):
    serializer_class = CourseModelSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        key = f'course-{category_id}'
        queryset = cache.get(key)
        if queryset:
            return queryset
        queryset = Course.objects.filter(category=category_id).select_related('category')
        cache.set(key, queryset, timeout=None)
        return queryset


class HomeworkCreateAPIView(ListCreateAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def get_queryset(self):
        key = f'homework'
        queryset = cache.get(key)
        if queryset:
            return queryset
        queryset = Homework.objects.all().select_related('module')
        cache.set(key, queryset, timeout=None)
        return queryset

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class VideoListCreateApiView(ListCreateAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        key = f'video'
        queryset = cache.get(key)
        if queryset:
            return queryset
        queryset = Video.objects.all()
        cache.set(key, queryset, timeout=None)
        return queryset


class VideoDetailAPiView(RetrieveUpdateDestroyAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_queryset(self):
        key = f'video-{self.kwargs["pk"]}'
        queryset = cache.get(key)
        if queryset:
            print('kirdi')
            return queryset
        queryset = Video.objects.all().select_related('module')
        cache.set(key, queryset, timeout=None)
        return queryset


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