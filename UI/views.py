from asgiref.sync import async_to_sync
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages  
from .forms import FormUploadHwork
from scripts.main import main
     

class HomePageView(FormView):
    """ Formulario para subir tarea """
    template_name = 'index.html'
    form_class = FormUploadHwork

    success_url = reverse_lazy('home')  

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(files = request.FILES)
        print(form)
        try:
            if form.is_valid():
                return self.form_valid(form)
        except Exception as e:
            messages.error(request, "No se ha enviado ningún archivo en el campo correspondiente.")
            print(e)

            
        return self.form_invalid(form)
            

    def form_valid(self, form):
        # investgar sobre cleaned_data
        archivo = form.cleaned_data.get('file_homework') 
        nombre_archivo = archivo.name
        try:
            async_to_sync(main)(nombre_archivo)
            messages.success(self.request, 'Tarea subida correctamente')
        except Exception as e:
            print("es de form valid?")
            print(e)
        
        return super().form_valid(form)
