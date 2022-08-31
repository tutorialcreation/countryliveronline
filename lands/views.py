from django.shortcuts import render
from .helpers.property24scrapper import PropertyScrapper
from django.views.generic import View
# Create your views here.


class AddLand(View):
    def get(self, request):
        return render(request, "lands/index.html")

    def post(self, request, *args, **kwargs):
        return render(request, "lands/form.html")


class PropertyScrapperView(View):
    def get(self, request):
        ps = PropertyScrapper()
        ps.get_links()
        return render(request, "lands/index.html")
