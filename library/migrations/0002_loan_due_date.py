from datetime import timedelta

from django.db import migrations, models


def set_due_dates_from_loan_date(apps, schema_editor):
    Loan = apps.get_model('library', 'Loan')
    for loan in Loan.objects.all().iterator():
        loan.due_date = loan.loan_date + timedelta(days=14)
        loan.save(update_fields=['due_date'])


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='due_date',
            field=models.DateField(null=True),
        ),
        migrations.RunPython(set_due_dates_from_loan_date, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='loan',
            name='due_date',
            field=models.DateField(),
        ),
    ]
