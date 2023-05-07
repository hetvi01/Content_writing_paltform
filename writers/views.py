from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from writers.constants import MSG_REGISTER_USER_SUCCESSFULLY, MSG_LOG_IN_SUCCESSFULLY
from writers.serializer import WriterSerializer


class WriterRegistrationView(APIView):
    serializer_class = WriterSerializer

    def post(self, request):
        """
        Registration for writer
        :param request:
        :return: serialized data
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={"message": MSG_REGISTER_USER_SUCCESSFULLY, "data": serializer.data},
                            status=HTTP_201_CREATED)


class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        """
        user login
        """
        response = super(LoginView, self).post(request, *args, **kwargs)
        return Response(data={"message": MSG_LOG_IN_SUCCESSFULLY, "data": response.data})
