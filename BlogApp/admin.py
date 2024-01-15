from django.contrib import admin
from . models import Post ,Tag , Comments , Subscribe ,Profile


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(Subscribe)
admin.site.register(Profile)
