from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.forms import profileUpdateForm, userUpdateForm
from users.models import Profile as Pro
from users.models import  Kerkesat
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from django.core.mail import send_mail
from django.core.mail import EmailMessage

# Create your views here.

@login_required
def Profile(request):
    if request.method == 'POST':
        u_form = userUpdateForm(request.POST,instance=request.user)
        p_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile Updated')
            return redirect('users:profile')
    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context= {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'profile/profile.html',context)


def kerkesa(request):
    if request.method == 'POST':
        emri = request.POST.get('name')
        email = request.POST.get('e-mail')
        numri_tel = request.POST.get('phone')
        prof = request.user.profile
        kerkesa = Kerkesat(profili=prof, emri=emri, email=email, numri_tel=numri_tel)
        kerkesa.save()
        prof_id = prof.id
        Pro.objects.filter(id=prof_id).update(is_teacher=True)
        
        message = ''
        send_mail(
            'MesoOn, kerkesa u pranua.',
            message,
            'mesoon@no-reply.com',
            [email],
            fail_silently=False,
        )
        send_mail(
            'Team_Gurukul',
            'Dikush beri kerkese per llogari mesuesi. Me info: ' + emri + ' , ' + email + ' , ' + numri_tel + ' , ' + str(prof) + '.',
            'gsvcontact.vedas@gmail.com',
            ['chiraagkakar@gmail.com'],
            fail_silently=False,
        )
        messages.info(request, f'The request was sent successfully, you will be notified by email.')
        return redirect('courses:home')


