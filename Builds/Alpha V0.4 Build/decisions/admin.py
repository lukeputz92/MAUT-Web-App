from django.contrib import admin
from .models import UserProfile, Decide, Item, Criteria

# Register your models here.
class CriteriaInline(admin.TabularInline):
	model = Criteria

class ItemInline(admin.TabularInline):
	model = Item

class DecideAdmin(admin.ModelAdmin):
	inlines = [
		CriteriaInline,
		ItemInline,
	]

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'firstName', 'lastName')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Decide,DecideAdmin)