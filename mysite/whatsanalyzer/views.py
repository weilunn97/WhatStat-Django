from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect


# Create your views here.
def index(request):
    # Serve up the success page if upload is successful
    if request.method == "POST":
        uploadedFile = request.FILES['WhatsAppFile']
        fileContents = uploadedFile.read().decode('utf-8')
        fileContentsList = fileContents.split('\n')
        # calculateMetrics()
        # return render(request, 'whatsanalyzer/upload.html', {'uploadedFile': uploadedFile,
        #                                                      'fileContents': fileContents,
        #                                                      'fileContentsList': fileContentsList})

        return upload(request, uploadedFile, fileContents, fileContentsList)

    # Else, refresh the page
    return render(request, 'whatsanalyzer/index.html')


def upload(request, uploadedFile, fileContents, fileContentsList):
    return render(request, 'whatsanalyzer/my_template.html', {'uploadedFile': uploadedFile,
                                                         'fileContents': fileContents,
                                                         'fileContentsList': fileContentsList})


