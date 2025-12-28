from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta

from apps.accounts.models import User
from apps.properties.models import Property, PropertyView, Favorite
from apps.inquiries.models import Inquiry, InquiryMessage
from apps.services.models import FindRoomRequest, ShiftHomeRequest


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to require admin/staff access."""
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class DashboardView(AdminRequiredMixin, TemplateView):
    """Main admin dashboard with analytics."""
    template_name = 'admin_panel/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        last_7_days = today - timedelta(days=7)
        
        # User Stats
        context['total_users'] = User.objects.count()
        context['total_landlords'] = User.objects.filter(user_type='LANDLORD').count()
        context['total_tenants'] = User.objects.filter(user_type='TENANT').count()
        context['new_users_30d'] = User.objects.filter(date_joined__date__gte=last_30_days).count()
        context['new_users_7d'] = User.objects.filter(date_joined__date__gte=last_7_days).count()
        
        # Property Stats
        context['total_properties'] = Property.objects.count()
        context['pending_properties'] = Property.objects.filter(status='PENDING').count()
        context['approved_properties'] = Property.objects.filter(status='APPROVED').count()
        context['rented_properties'] = Property.objects.filter(status='RENTED').count()
        context['featured_properties'] = Property.objects.filter(is_featured=True).count()
        
        # Inquiry Stats
        context['total_inquiries'] = Inquiry.objects.count()
        context['pending_inquiries'] = Inquiry.objects.filter(status='PENDING').count()
        context['inquiries_7d'] = Inquiry.objects.filter(created_at__date__gte=last_7_days).count()
        
        # Service Stats
        context['find_room_requests'] = FindRoomRequest.objects.count()
        context['pending_find_room'] = FindRoomRequest.objects.filter(status='PENDING').count()
        context['shift_home_requests'] = ShiftHomeRequest.objects.count()
        context['pending_shift_home'] = ShiftHomeRequest.objects.filter(status='PENDING').count()
        
        # Recent Activity
        context['recent_properties'] = Property.objects.select_related('owner').order_by('-created_at')[:5]
        context['recent_inquiries'] = Inquiry.objects.select_related('rental_property', 'sender').order_by('-created_at')[:5]
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        
        # Properties by District
        context['properties_by_district'] = Property.objects.values('district').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Monthly Property Trend (last 6 months)
        six_months_ago = today - timedelta(days=180)
        context['monthly_properties'] = Property.objects.filter(
            created_at__date__gte=six_months_ago
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(count=Count('id')).order_by('month')
        
        return context


class PropertyManagementView(AdminRequiredMixin, ListView):
    """Admin property management list."""
    model = Property
    template_name = 'admin_panel/properties.html'
    context_object_name = 'properties'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Property.objects.select_related('owner').order_by('-created_at')
        
        # Filters
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        district = self.request.GET.get('district')
        if district:
            queryset = queryset.filter(district=district)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(owner__email__icontains=search) |
                Q(area__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Property.STATUS_CHOICES
        context['district_choices'] = Property.DISTRICT_CHOICES
        context['pending_count'] = Property.objects.filter(status='PENDING').count()
        return context


class PropertyApproveView(AdminRequiredMixin, View):
    """Approve a property."""
    
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        property_obj.status = 'APPROVED'
        property_obj.rejection_reason = ''
        property_obj.save()
        messages.success(request, f'Property "{property_obj.title}" has been approved.')
        return redirect('admin_panel:properties')


class PropertyRejectView(AdminRequiredMixin, View):
    """Reject a property."""
    
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        reason = request.POST.get('reason', '')
        property_obj.status = 'REJECTED'
        property_obj.rejection_reason = reason
        property_obj.save()
        messages.success(request, f'Property "{property_obj.title}" has been rejected.')
        return redirect('admin_panel:properties')


class PropertyToggleFeaturedView(AdminRequiredMixin, View):
    """Toggle featured status of a property."""
    
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        property_obj.is_featured = not property_obj.is_featured
        property_obj.save()
        status = 'featured' if property_obj.is_featured else 'unfeatured'
        messages.success(request, f'Property "{property_obj.title}" is now {status}.')
        return redirect('admin_panel:properties')


class UserManagementView(AdminRequiredMixin, ListView):
    """Admin user management list."""
    model = User
    template_name = 'admin_panel/users.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.order_by('-date_joined')
        
        user_type = self.request.GET.get('user_type')
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone_number__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type_choices'] = User.USER_TYPE_CHOICES
        context['total_users'] = User.objects.count()
        context['total_landlords'] = User.objects.filter(user_type='LANDLORD').count()
        context['total_tenants'] = User.objects.filter(user_type='TENANT').count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        return context


class UserToggleActiveView(AdminRequiredMixin, View):
    """Toggle user active status."""
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.error(request, "You cannot deactivate yourself.")
        else:
            user.is_active = not user.is_active
            user.save()
            status = 'activated' if user.is_active else 'deactivated'
            messages.success(request, f'User "{user.email}" has been {status}.')
        return redirect('admin_panel:users')


class InquiryManagementView(AdminRequiredMixin, ListView):
    """Admin inquiry management list."""
    model = Inquiry
    template_name = 'admin_panel/inquiries.html'
    context_object_name = 'inquiries'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Inquiry.objects.select_related('rental_property', 'sender', 'rental_property__owner').order_by('-created_at')
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(rental_property__title__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_inquiries'] = Inquiry.objects.count()
        context['pending_inquiries'] = Inquiry.objects.filter(status='PENDING').count()
        context['responded_inquiries'] = Inquiry.objects.filter(status='RESPONDED').count()
        context['closed_inquiries'] = Inquiry.objects.filter(status='CLOSED').count()
        return context


class ServiceRequestsView(AdminRequiredMixin, TemplateView):
    """Admin service requests management."""
    template_name = 'admin_panel/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Find Room Requests
        context['find_room_requests'] = FindRoomRequest.objects.select_related('user').order_by('-created_at')[:50]
        context['find_room_count'] = FindRoomRequest.objects.count()
        context['pending_find_room'] = FindRoomRequest.objects.filter(status='PENDING').count()
        
        # Shift Home Requests
        context['shift_home_requests'] = ShiftHomeRequest.objects.select_related('user').order_by('-created_at')[:50]
        context['shift_home_count'] = ShiftHomeRequest.objects.count()
        context['pending_shift_home'] = ShiftHomeRequest.objects.filter(status='PENDING').count()
        
        return context


class AnalyticsView(AdminRequiredMixin, TemplateView):
    """Detailed analytics view."""
    template_name = 'admin_panel/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        import json
        
        # Property views over time
        last_30_days = today - timedelta(days=30)
        six_months_ago = today - timedelta(days=180)
        
        # Total rent value
        context['total_rent_value'] = Property.objects.filter(
            status='APPROVED'
        ).aggregate(total=Sum('price'))['total'] or 0
        
        # Average price
        context['avg_price'] = Property.objects.filter(
            status='APPROVED'
        ).aggregate(avg=Avg('price'))['avg'] or 0
        
        # Conversion rate (inquiries with viewing requests / total inquiries)
        total_inquiries = Inquiry.objects.count()
        viewing_inquiries = Inquiry.objects.exclude(preferred_visit_date__isnull=True).count()
        context['conversion_rate'] = (viewing_inquiries / total_inquiries * 100) if total_inquiries > 0 else 0
        
        # Average response time (mock for now)
        context['avg_response_time'] = 4
        
        # Monthly labels and data for charts
        months = []
        property_counts = []
        user_counts = []
        for i in range(5, -1, -1):
            month_date = today - timedelta(days=i*30)
            month_start = month_date.replace(day=1)
            if i > 0:
                next_month = (month_date + timedelta(days=32)).replace(day=1)
            else:
                next_month = today + timedelta(days=1)
            
            months.append(month_start.strftime('%b'))
            property_counts.append(Property.objects.filter(
                created_at__date__gte=month_start,
                created_at__date__lt=next_month
            ).count())
            user_counts.append(User.objects.filter(
                date_joined__date__gte=month_start,
                date_joined__date__lt=next_month
            ).count())
        
        context['monthly_labels'] = json.dumps(months)
        context['monthly_properties'] = json.dumps(property_counts)
        context['monthly_users'] = json.dumps(user_counts)
        
        # Property type distribution
        property_types = Property.objects.values('property_type').annotate(
            count=Count('id')
        ).order_by('-count')
        type_labels = [Property.PROPERTY_TYPE_CHOICES[next((i for i, c in enumerate(Property.PROPERTY_TYPE_CHOICES) if c[0] == pt['property_type']), 0)][1] for pt in property_types]
        type_data = [pt['count'] for pt in property_types]
        context['property_type_labels'] = json.dumps(type_labels)
        context['property_type_data'] = json.dumps(type_data)
        
        # Price distribution
        total_properties = Property.objects.filter(status='APPROVED').count() or 1
        price_ranges = [
            {'label': 'Under Rs. 10,000', 'min': 0, 'max': 10000},
            {'label': 'Rs. 10,000 - 20,000', 'min': 10000, 'max': 20000},
            {'label': 'Rs. 20,000 - 35,000', 'min': 20000, 'max': 35000},
            {'label': 'Rs. 35,000 - 50,000', 'min': 35000, 'max': 50000},
            {'label': 'Over Rs. 50,000', 'min': 50000, 'max': 999999999},
        ]
        price_distribution = []
        for pr in price_ranges:
            count = Property.objects.filter(
                status='APPROVED',
                price__gte=pr['min'],
                price__lt=pr['max']
            ).count()
            price_distribution.append({
                'label': pr['label'],
                'count': count,
                'percentage': round(count / total_properties * 100, 1)
            })
        context['price_distribution'] = price_distribution
        
        # Top properties by views
        context['top_properties'] = Property.objects.filter(
            status='APPROVED'
        ).annotate(
            inquiry_count=Count('inquiries')
        ).order_by('-views_count')[:10]
        
        # District stats
        districts = [
            ('KATHMANDU', 'Kathmandu'),
            ('BHAKTAPUR', 'Bhaktapur'),
            ('LALITPUR', 'Lalitpur'),
        ]
        district_stats = []
        for code, name in districts:
            props = Property.objects.filter(district=code, status='APPROVED')
            district_stats.append({
                'name': name,
                'count': props.count(),
                'avg_price': props.aggregate(avg=Avg('price'))['avg'] or 0,
                'inquiries': Inquiry.objects.filter(rental_property__district=code).count(),
            })
        context['district_stats'] = district_stats
        
        return context


class ApiStatsView(AdminRequiredMixin, View):
    """API endpoint for dashboard stats (for charts)."""
    
    def get(self, request):
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        
        # Daily property views
        daily_views = list(PropertyView.objects.filter(
            viewed_at__date__gte=last_30_days
        ).annotate(
            date=TruncDate('viewed_at')
        ).values('date').annotate(count=Count('id')).order_by('date'))
        
        # Convert dates to strings
        for item in daily_views:
            item['date'] = item['date'].strftime('%Y-%m-%d')
        
        return JsonResponse({
            'daily_views': daily_views,
        })
