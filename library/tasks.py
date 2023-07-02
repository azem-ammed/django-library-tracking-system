from collections import defaultdict

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Loan


@shared_task
def check_overdue_loans():
    today = timezone.now().date()
    overdue = (
        Loan.objects.filter(is_returned=False, due_date__lt=today)
        .select_related('member__user', 'book')
        .order_by('member_id', 'id')
    )
    by_member = defaultdict(list)
    for loan in overdue:
        by_member[loan.member_id].append(loan)

    for loans in by_member.values():
        member = loans[0].member
        email = member.user.email
        if not email:
            continue
        lines = [
            f'Hello {member.user.username},',
            '',
            'The following books are overdue. Please return them as soon as possible:',
            '',
        ]
        for loan in loans:
            lines.append(f'- "{loan.book.title}" (due {loan.due_date})')
        lines.append('')
        send_mail(
            subject='Library reminder: overdue book(s)',
            message='\n'.join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=(
                f'Hello {loan.member.user.username},\n\n'
                f'You have successfully loaned "{book_title}".\n'
                f'Please return it by {loan.due_date}.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass
