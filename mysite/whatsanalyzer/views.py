from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from .models import Message, WhatsAppTextFile


# Create your views here.
def index(request):
    # Serve up the success page if upload is successful
    if request.method == "POST":
        requestFiles = request.POST.get('WhatsAppFile')
        request.FILES["TESTKEY"] = "TESTVALUE"
        # uploadedFile = request.FILES['WhatsAppFile']
        # fileContents = uploadedFile.read().decode('utf-8')
        # fileContentsList = fileContents.split('\n')
        # calculateMetrics()
        # return render(request, 'whatsanalyzer/upload.html', {'requestFiles': requestFiles})
        #                                                      # 'uploadedFile': uploadedFile,
        #                                                      # 'fileContents': fileContents,
        #                                                      # 'fileContentsList': fileContentsList})

        return redirect('upload/', {'requestFiles': requestFiles})
                                                               # 'uploadedFile': uploadedFile,
                                                               # 'fileContents': fileContents,
                                                               # 'fileContentsList': fileContentsList}))

    # Else, refresh the page
    return render(request, 'whatsanalyzer/homepage.html/')


def upload(request, uploadedFile, fileContents, fileContentsList):
    return render(request, 'upload/', {'uploadedFile': uploadedFile,
                                                              'fileContents': fileContents,
                                                              'fileContentsList': fileContentsList})
