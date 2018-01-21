import ipfsapi
import os
from django import forms

from MultiStakeHolder import settings
from User import blockchain


def handle_uploaded_file(f):
    with open('media/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class DocumentUpload(forms.Form):
    document = forms.FileField()
    uploaded_user_address = forms.CharField()

    def save(self):
        file = self.cleaned_data['document']
        handle_uploaded_file(file)
        client = ipfsapi.connect("http://localhost")
        file_hash = client.add(settings.BASE_DIR + '/media/' + file.name)['Hash']
        enchash = file_hash
        blockchain.uploadHash(file_hash, file.name, enchash)


def _decrypt_rsa(decrypt_key_str, cipher_text):
    from Crypto.PublicKey import RSA
    rsakey = RSA.importKey(decrypt_key_str)
    decrypted = rsakey.decrypt(cipher_text)
    return decrypted


def _encrypt_rsa(decrypt_key_str, cipher_text):
    from Crypto.PublicKey import RSA
    rsakey = RSA.importKey(decrypt_key_str)
    encrypted = rsakey.encrypt(cipher_text)
    return encrypted
