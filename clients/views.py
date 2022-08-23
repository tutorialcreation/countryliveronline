from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class YellowPagesScrapperView(View):
    def post(self, request, *args, **kwargs):
        return render(request, 'clients/yellowpages.html')


class FacebookScrapperView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'clients/facebook.html')

    def post(self, request, *args, **kwargs):
        return render(request, 'clients/facebook.html')
