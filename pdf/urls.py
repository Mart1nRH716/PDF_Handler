from django.urls import path
from .views import *

urlpatterns = [
    path('', InicioPDF.as_view(), name='index'),
    path('extraer/', ExtractPDF.as_view(), name='extract-pdf'),
    path('combinar/', CombinePDF.as_view(), name='combine-pdf'),
    path('descargar/<str:filename>/', DescargarArchivosView.as_view(), name='descargar_archivos'),

]
