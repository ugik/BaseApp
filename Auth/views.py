from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext

from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail, EmailMultiAlternatives

from forms import CustomUserCreationForm, CustomUserChangeForm
from Auth.models import CustomUser as User
import logging
from Crypto.Cipher import AES
import base64

logr = logging.getLogger(__name__)
secret_key = "1234567890123456"

def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/login')

	context = {}
	return render_to_response('index.html', 
                             {'full_name' : request.user.email, 'verified' : request.user.verified},
                              context_instance=RequestContext(request))	

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c, context_instance=RequestContext(request))

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
	
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/user/loggedin')
    else:
        return HttpResponseRedirect('/user/invalid')

def loggedin(request):
	return render_to_response('loggedin.html',
						 	 {'full_name' : request.user.email},
							  context_instance=RequestContext(request))

def invalid_login(request):
# delete data
    from Auth.models import CustomUser as User
    try:
        record = User.objects.get(pk=1)
        record.delete()
    except:
        pass

    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

#    import pdb; pdb.set_trace()

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        # see if user with this email already exists
        try:
            user = User.objects.get(email=form.data['email'])
            return render_to_response('invalid_user.html')
        except:
            pass


        if form.is_valid():
            form.save()

            # get new user record id to use in verification link
            try:
                user_id = User.objects.get(email=form.cleaned_data['email']).pk
            except:
                user_id = 0

            # encrypt the user_id
            pad = encode(user_id)
            subject, from_email, to = 'Verify registration', 'ugikma@gmail.com', form.cleaned_data['email']

            # verification url for email
            verify_url = request.build_absolute_uri()+pad
            send_verification_email(subject, from_email, to, verify_url) 

            if len(form.cleaned_data['alias']) == 0:
                try:  # default alias to email prefix
                    email = form.cleaned_data['email']
                    record = User.objects.get(email=email)
                    prefix=email[:email.find('@')]
                    record.alias = prefix
                    record.save()
                except:
                    pass

            return HttpResponseRedirect('/user/register_success')
        else:
            print form.errors  # see the form errors in the console.

    args = {}
    args.update(csrf(request))
	
    args['form'] = CustomUserCreationForm()
    return render_to_response('register.html', args)

def user_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/loggedin')

    else:
        user = request.user
#        profile = user.profile
        form = CustomUserChangeForm(instance=user)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('profile.html', args, context_instance=RequestContext(request))


def verify_user(request, user_id=None):

    try:
        user_id = decode(user_id)   # decode the user_id passed in url
        record = User.objects.get(pk=int(user_id))
        record.verified = True
        record.save()
        return render_to_response('verified.html')
    except:
        user_id = None
        return HttpResponseRedirect('/user/invalid')

    return HttpResponseRedirect('/')

def register_success(request):
	return render_to_response('register_success.html')

def send_verification_email(subject, from_email, to, verify_url):
    plaintext = get_template('email_verify.txt')
    htmly     = get_template('email_verify.html')

    d = Context({ 'verify_url': verify_url })

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True

def encode(user_id):
    text = "%016d" % (user_id)   # pad to 16bytes
    cipher = AES.new(secret_key,AES.MODE_ECB)
    return(base64.b64encode(cipher.encrypt(text)))

def decode(text):
    cipher = AES.new(secret_key,AES.MODE_ECB)
    return(cipher.decrypt(base64.b64decode(text)))


