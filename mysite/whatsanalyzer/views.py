from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect


# Create your views here.
def index(request):
    # Serve up the success page if upload is successful
    if request.method == "POST":
        uploadedFile = request.FILES['WhatsAppFile']
        messages.success(request, f"Uploaded File Name : {uploadedFile.name}")
        fileContents = uploadedFile.read().decode('utf-8')
        fileContentsType = type(fileContents)
        fileContentsList = fileContents.split('\n')
        fileContentsListLength = len(fileContentsList)

        return render(request, 'whatsanalyzer/upload.html', {'uploadedFile': uploadedFile,
                                                             'fileContents': fileContents,
                                                             'fileContentsListLength': fileContentsListLength,
                                                             'fileContentsList': fileContentsList})
    # Else, refresh the page
    return render(request, 'whatsanalyzer/index.html')


def upload(request):
    return render(request, 'whatsanalyzer/upload.html')


