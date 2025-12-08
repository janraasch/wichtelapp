from datetime import datetime

from django.contrib import admin, messages

from .models import Drawing, Event, Profile, UserDrawing, Wishlist


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "code_name", "address", "created_at", "updated_at")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "text", "created_at", "updated_at")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "created_at")
    list_filter = ("name", "user")
    ordering = ("-created_at",)


class UserDrawingInline(admin.TabularInline):
    model = UserDrawing
    extra = 0
    fields = ("giver", "receiver")
    readonly_fields = ("giver", "receiver")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ("year", "created_at", "user_drawing_count")
    ordering = ("-year",)
    change_list_template = "admin/wichtel/drawing/change_list.html"
    inlines = [UserDrawingInline]

    def user_drawing_count(self, obj):
        return obj.user_drawings.count()

    user_drawing_count.short_description = "Assignments"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        current_year = datetime.now().year
        extra_context["current_year"] = current_year
        extra_context["current_year_exists"] = Drawing.objects.filter(year=current_year).exists()
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "create-current-year/",
                self.admin_site.admin_view(self.create_drawing_view),
                name="wichtel_drawing_create_current_year",
            ),
        ]
        return custom_urls + urls

    def create_drawing_view(self, request):
        from django.shortcuts import redirect

        year = datetime.now().year
        try:
            drawing = Drawing.create_for_year(year)
            self.message_user(
                request,
                f"Successfully created drawing for {drawing.year} with {drawing.user_drawings.count()} assignments.",
                messages.SUCCESS,
            )
        except ValueError as e:
            self.message_user(request, f"Validation error: {e}", messages.ERROR)
        except Exception as e:
            self.message_user(request, f"Error creating drawing: {e}", messages.ERROR)
        return redirect("..")


@admin.register(UserDrawing)
class UserDrawingAdmin(admin.ModelAdmin):
    list_display = ("drawing", "giver", "receiver", "created_at")
    list_filter = ("drawing",)
    ordering = ("-drawing__year", "giver")
