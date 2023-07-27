from django.shortcuts import render,HttpResponseRedirect, \
HttpResponse ,get_object_or_404, redirect

# Create your views here.
from .forms import CertificateForm,UpdateCertificateForm
from django.middleware.csrf import get_token 
from .models import Certificate
import json
from weasyprint import HTML
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
import jwt

from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from .forms import TokenVerificationForm
from .models import Certificate
from django.contrib import messages
from django.conf import settings

secret_key = settings.SECRET_KEY

def home(request):
    list_mycert = Certificate.objects.filter(user=request.user.id)
    context= {
        'list_mycert':list_mycert
    }
    return render(request,'home.html', context)

@login_required
def create_certificate(request):
    form = CertificateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        #form.save()
        form.instance.user = request.user
        object = form.save()
        id = object.pk
     
        cert_no = object.certificate_no
        # return HttpResponseRedirect("/")
        # render(request, "download.html", {'id':id})
        #return HttpResponse(id)
        return redirect('view_certificate_file', id=id)
        # list_obj = {
        #     "id":id,
        #     "cert_no":cert_no,
        # }
        # response = HttpResponse(json.dumps(list_obj), content_type='application/json')
        # return response
    # csrf_token = get_token(request)
    # new_form = CertificateForm(request.POST or None, initial={'csrfmiddlewaretoken': csrf_token})
    else:
        # Refresh the CSRF token
        csrf_token = get_token(request)
        #csrf_token = get_token_from_session(request)
        form = CertificateForm(request.POST or None, initial={'csrfmiddlewaretoken': csrf_token})
        context = {
            "csrf_token": csrf_token,
            "form":form,
        }
    return render(request, 'create_cert.html', context)






@login_required
#Here we can views our certificate with their respective id and whole certificate into webpage.
def view_certificate(request,id):
    cert_item = Certificate.objects.get(id=id)
    context ={
        'cert_item':cert_item,
    }
    return render(request, 'view_mycertificate.html', context)
    
@login_required
def update_certificate(request, id):
    certificate = get_object_or_404(Certificate, id=id)
    initial = {
        'name': certificate.name,
        'certificate': certificate.header,
    }
    form = UpdateCertificateForm(request.POST or None, instance=certificate, initial=initial)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            csrf_token = get_token(request)
            messages.success(request, {'Your Certificate is Updated.'})
            return redirect('home')

        else:
            messages.info(request, {'Something Wrong!'})
            return redirect('home')
    else:
        csrf_token = get_token(request)
        return render(request, 'update_certificate.html', {'form': form, 'csrf_token': csrf_token, 'initial': initial})


@login_required
def gen_cert_pdf(request, id):
    data = Certificate.objects.get(id=id)
    # html = render_to_string('genpdf.html', {'data':data})
    # #html = render(request, 'pdf.html', {'data':data})
    # pdf = HTML(string=html).write_pdf()
    # response = HttpResponse(content_type='application/pdf')
    # #response['Content-Disposition'] = f'filename=certificate23.pdf'
    # #return response
    # return HttpResponse(pdf, content_type='application/pdf')
    object = data
    name = object.name
    certificate_no = object.certificate_no
    
    html_string = render_to_string('genpdf.html', {'data':data})
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
                      #base_url=request.build_absolute_uri() for rendering static file image
    # Set the custom PDF file name
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(f'{name}{certificate_no}.pdf')
    response.write(pdf)

    return response






@login_required
def generate_token(request, id):
    certificate = get_object_or_404(Certificate, id=id)
    if request.user == certificate.user:
        # Generate an access token for the certificate
        access_token = jwt.encode({
            'certificate_id': certificate.id,
            # 'certificate_data':str(certificate.created_at),
        }, key=secret_key, algorithm='HS256')

        # Set the expiry time to 2 minutes from now
        expiry_time = datetime.utcnow() + timedelta(minutes=60)

        # Create a response object
        response = render(request, 'generate_token.html', {'access_token': access_token, 'certificate': certificate})

        # Check if the token is expired
        # if access_token['exp'] < str(datetime.now()):
        #     # Refresh the token
        #     new_access_token = jwt.encode({
        #         'certificate_id': certificate.id,
        #         # 'certificate_data':str(certificate.created_at),
        #     }, key=secret_key, algorithm='HS256')

        #     # Set the new expiry time
        #     expiry_time = datetime.utcnow() + timedelta(minutes=60)

        #     # Update the access token in the response object
        #     response['access_token'] = new_access_token

        # Return the response object
        return response

    elif certificate is None or request.user != certificate.user:
        #return render(request, 'error.html', {'message': "This certificate does not belong to you."})
        messages.warning(request, 'This certificate does not belong to you.')
        return HttpResponseRedirect('/')
    
    else:
        return redirect('/')




def verify_token(request):
    if request.method == 'POST':
        form = TokenVerificationForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            token = jwt.decode(token, secret_key, algorithms=['HS256'])
            # username, email = token['username'], token['email']
            certificate_id = token['certificate_id']
            certificate = Certificate.objects.get(id=certificate_id)
            result = {'status': 'success', 'payload': token, 'certificate': certificate}
            # if token['exp'] < datetime.now():
            #     result = {'status': 'error', 'message': 'Token is expired.'}
        return render(request, 'token_verification_result.html', {'result': result})
    else:
        form = TokenVerificationForm()
    return render(request, 'token_verification.html', {'form': form})

