""" vista principal de la app """
import os
import time
from asgiref.sync import async_to_sync
from django.views.generic import FormView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.contrib import messages
from scripts.main import main
from .forms import FormUploadHwork

class HomePageView(FormView):
    """ Formulario para subir tarea """
    template_name = 'index.html'
    form_class = FormUploadHwork

    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(files=request.FILES)
        print(form)
        try:
            if form.is_valid():
                return self.form_valid(form)
        except FileExistsError as e:
            messages.error(request, "No se ha enviado ningún archivo en el campo correspondiente.")
            print(e)

        return self.form_invalid(form)

    def form_valid(self, form):
        archivo = form.cleaned_data.get('file_homework')
        nombre_archivo = archivo.name

        ruta_tareas_windows = r"C:\Users\chili\OneDrive\Desktop\sena_docs\TAREAS"
        fs = FileSystemStorage(location=ruta_tareas_windows)

        if fs.exists(nombre_archivo):
            try:
                print(f"El archivo {nombre_archivo} eliminado")
                fs.delete(nombre_archivo)
            except PermissionError:
                base, ext = os.path.splitext(nombre_archivo)
                nombre_archivo = f"{base}_{int(time.time())}{ext}"
                print(f"name_alter: {nombre_archivo}")
        nombre_guardado = fs.save(nombre_archivo, archivo)
        root_complet = fs.path(nombre_guardado)
        try:
            async_to_sync(main)(nombre_archivo, root_complet)
            messages.success(self.request, 'Tarea subida correctamente')
            try:
                if os.path.exists(root_complet):
                    os.remove(root_complet)
            except FileNotFoundError as e:
                print(e)
        except FileExistsError as e:
            print("Error de Playwright:")
            print(e)
            messages.error(self.request, 'Ocurrió un error al procesar el script.')
        return super().form_valid(form)
