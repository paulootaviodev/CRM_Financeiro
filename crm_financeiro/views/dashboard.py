from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from calendar import monthrange
from django.db.models import Count, Q
import locale

from ..models import LoanProposal, Installment
from blog.models import ViewsPerMonth

# Set locale to Brazilian Portuguese for month name formatting
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "crm_financeiro/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now()
        current_month_start = today.replace(day=1)
        current_month_end = today.replace(day=monthrange(today.year, today.month)[1])

        loan_proposals = LoanProposal.objects.order_by('-id')

        # Filter paid proposals within the current month
        paid_proposals = loan_proposals.filter(
            status='0008',
            updated_at__range=(current_month_start, current_month_end)
        )

        monthly_aggregates = paid_proposals.aggregate(
            total_value=Sum('released_value'),
            total_installments=Sum('number_of_installments'),
            installment_value=Sum('value_of_installments')
        )

        monthly_sales = monthly_aggregates['total_value'] or 0
        total_installments = monthly_aggregates['total_installments'] or 0
        installment_value = monthly_aggregates['installment_value'] or 0
        monthly_profit = total_installments * installment_value

        # Calculate default rate (unpaid proposals with status '0008' and payment_status '0004')
        unpaid_proposals = loan_proposals.filter(status='0008', payment_status='0004')
        total_proposals_count = loan_proposals.count()
        default_rate = ((unpaid_proposals.count() / total_proposals_count) * 100) if total_proposals_count else 0

        # Count proposals still in progress
        in_progress_count = loan_proposals.filter(status__in=['0001', '0002', '0003']).count()

        # Add current statistics to context
        context.update({
            'month_sales': monthly_sales,
            'month_sales_profit': monthly_profit,
            'default': default_rate,
            'loan_proposals_in_progress': in_progress_count
        })

        # Historical data for the past 12 months
        labels = []
        sales_values = []
        profit_values = []

        for i in range(11, -1, -1):
            ref_date = today - timedelta(days=30 * i)
            year = ref_date.year
            month = ref_date.month

            month_start = timezone.make_aware(datetime(year, month, 1))
            month_end = timezone.make_aware(datetime(year, month, monthrange(year, month)[1], 23, 59, 59))

            monthly_data = loan_proposals.filter(
                updated_at__range=(month_start, month_end)
            ).aggregate(
                total_value=Sum('released_value'),
                total_installments=Sum('number_of_installments'),
                installment_value=Sum('value_of_installments')
            )

            sales = monthly_data['total_value'] or 0
            installments = monthly_data['total_installments'] or 0
            installment_val = monthly_data['installment_value'] or 0
            profit = installments * installment_val

            month_label = ref_date.strftime('%b').capitalize()
            labels.append(month_label)
            sales_values.append(float(sales))
            profit_values.append(float(profit))

        # Add historical data to context
        context.update({
            'labels': labels,
            'sales_values': sales_values,
            'profit_values': profit_values
        })

        # Add installment status information
        counts = Installment.objects.order_by('-id').aggregate(
            paid=Count('id', filter=Q(is_paid=True)),
            unpaid=Count('id', filter=Q(is_paid=False, due_date__lt=timezone.now().date())),
            upcoming=Count('id', filter=Q(is_paid=False, due_date__gte=timezone.now().date())),
        )

        # Add installment data to context
        context.update({
            'paid': counts['paid'],
            'unpaid': counts['unpaid'],
            'upcoming': counts['upcoming']
        })

        # Add blog views
        labels = []
        views = []

        blog_views = ViewsPerMonth.objects.order_by('-id')

        for i in range(11, -1, -1):
            ref_date = today - timedelta(days=30 * i)
            month = ref_date.month
            year = ref_date.year

            monthly_data = blog_views.filter(
                month__month=month,
                month__year=year
            ).aggregate(
                total_views=Sum('total')
            )

            total_views = monthly_data['total_views'] or 0

            month_label = ref_date.strftime('%b').capitalize()
            labels.append(month_label)
            views.append(int(total_views))

        # Add historical data to context
        context.update({
            'views_labels': labels,
            'views': views
        })

        return context
