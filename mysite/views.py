from django.http import HttpResponse


def index(request):
    html = '''
    <html>
        <body>
            <p>Welcome to my Django Assignment. This page is currently under construction.</p>
            <p>Please visit the <a href="http://localhost:8000/admin/">admin page</a> to interact with the database.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)
