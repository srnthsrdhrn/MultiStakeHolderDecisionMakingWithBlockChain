import json

from Crypto.Random import random
from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from User.forms import DocumentUpload
from . import blockchain


def login(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    response = blockchain.login(username, password)
    if response == '0x0000000000000000000000000000000000000000':
        return HttpResponse(json.dumps({'response': False}))
    return HttpResponse(json.dumps({'response': response}),)


@csrf_exempt
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    name = request.POST.get('name')
    portfolio = request.POST.get('portfolio')
    aadhar = request.POST.get('aadhar_number')
    if username and password and name and portfolio and aadhar:
        priv, pub = generate_RSA()
        response = blockchain.register(username, password, aadhar, name, portfolio, pub, priv)
        return HttpResponse(json.dumps({'response': response}))
    return HttpResponse(json.dumps({'error': 'Missing or Arguments'}))


def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    from Crypto.PublicKey import RSA
    new_key = RSA.generate(bits, e=randomgen())
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    return private_key, public_key


def randomgen():
    a = random.randint(3, 9999999)
    if a % 2 == 0:
        a = a + 1
    return a


@csrf_exempt
def updateHash(request):
    hash = request.POST.get('hash')
    enchash = request.POST.get('enchash')
    address = request.POST.get('address')
    portfolio = request.POST.get('portfolio')
    response = blockchain.updateHash(hash, enchash, address, portfolio)
    return HttpResponse(json.dumps({'response': response}))


@csrf_exempt
def uploadFile(request):
    form = DocumentUpload()
    if request.method == 'POST':
        form = DocumentUpload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'status': 'Success'}))
    return HttpResponse(json.dumps({'Error': form.errors}))


def _decrypt_rsa(decrypt_key_file, cipher_text):
    from Crypto.PublicKey import RSA
    key = open(decrypt_key_file, "r").read()
    rsakey = RSA.importKey(key)
    decrypted = rsakey.decrypt(cipher_text)
    return decrypted


def get_user_profile(request):
    address = request.GET.get('address')
    response = blockchain.checkUser(address)
    return HttpResponse(json.dumps({'response': response}))


def get_application(request):
    address = request.GET.get("address")
    cursor = request.GET.get("cursor")
    response = blockchain.getGovApplication(address, cursor)
    return HttpResponse(json.dumps({'response': response}))
