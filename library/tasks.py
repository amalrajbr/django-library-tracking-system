from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.utils import timezone

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    """Check overdue loan and send notification"""


    with transaction.atomic():
        # lock the loans that are due to avoid race condition
        # when book is returned while this notif is sent 
        # this is optional
        qs = (
            Loan
            .objects
            .select_for_update()
            .filter(
                due_date__lt=timezone.now().date(), # exclude today - past only
                is_returned=False
            )
        )
        for due_loan in qs:
            # Send an email reminder to each member with overdue books.
            member_email = due_loan.member.user.email
            member_username = due_loan.member.user.username or member_email
            book_title = due_loan.book.title
            send_mail(
                subject="Loan Due Date Passed !",
                message=(
                    f"Hello {member_username}\n\n"
                    f"You should have returned loaned {book_title}"
                    f" on {due_loan.due_date}.\nPlease return it asap."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member_email],
                fail_silently=False,
            )


