from django.contrib import admin
from .models import PostModel




class PostalModelAdmin(admin.ModelAdmin):
    list_display = ['__str__','content']
    fields = [
        'id',
        'active',
        'title',
        'slug',
        'content',
        'publish',
        'view_count',
        'publish_date',
        'author_email',

    ]
    readonly_fields = [
        'id',
        'updated',
        'timestamp'
    ]
    # class Meta:
    #     model = PostModel

admin.site.register(PostModel,PostalModelAdmin)
# Register your models here.
