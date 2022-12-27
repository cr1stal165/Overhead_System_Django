"""note URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from note_vrn import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('show_stuff/', views.show_stuff, name="show_stuff"),
    path('show_manufacturer/', views.show_manufacturer, name="show_manufacturer"),
    path('show_all_products/', views.show_all_products, name="show_all_products"),
    path('show_purchased/', views.show_purchased, name="show_purchased"),
    path('add_note/', views.add_note, name="add_note"),
    path('confirm_add_note/', views.confirm_add_note, name="confirm_add_note"),
    path('note_show/<int:note_id>', views.note_show, name="note_show"),
    path('csv/', views.download_csv, name="download_csv"),
    path('delete_show/<int:note_id>', views.delete_note, name="delete_note"),

]
