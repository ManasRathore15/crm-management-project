import os
import django

# Configure Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from leads.models import Agent, Lead, Comment

def seed_database():
    print("Seeding database for crm_project...")

    # 1. Create Admin Superuser
    admin_user, created = User.objects.get_or_create(username='admin', email='admin@leadflow.in')
    if created:
        admin_user.set_password('admin123')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.first_name = 'Admin User'
        admin_user.save()
        print("Admin superuser ('admin' / 'admin123') created.")
    else:
        print("Admin user already exists.")

    # 2. Create Agents
    u1, created = User.objects.get_or_create(username='priya', email='priya@leadflow.in')
    if created:
        u1.set_password('agent123')
        u1.first_name = 'Priya Sharma'
        u1.save()
    a1, created = Agent.objects.get_or_create(user=u1)
    a1.phone = '9876543211'
    a1.city = 'Mumbai'
    a1.save()
    print("Agent Priya Sharma ('priya' / 'agent123') seeded.")

    u2, created = User.objects.get_or_create(username='rahul', email='rahul@leadflow.in')
    if created:
        u2.set_password('agent123')
        u2.first_name = 'Rahul Verma'
        u2.save()
    a2, created = Agent.objects.get_or_create(user=u2)
    a2.phone = '9876543212'
    a2.city = 'Delhi'
    a2.save()
    print("Agent Rahul Verma ('rahul' / 'agent123') seeded.")

    # 3. Create Sample Leads
    if Lead.objects.count() == 0:
        # Lead 1
        Lead.objects.create(
            name="Amit Gupta", phone="9876543210", email="amit@gmail.com",
            city="Mumbai", state="Maharashtra", service="GST Registration",
            message="Urgent requirement", status="NEW", agent=None
        )

        # Lead 2
        l2 = Lead.objects.create(
            name="Sneha Patel", phone="9123456780", email="sneha@gmail.com",
            city="Ahmedabad", state="Gujarat", service="Company Incorporation",
            message="New startup", status="CONTACTED", agent=a1
        )
        # Add comment for l2
        Comment.objects.create(
            lead=l2, author=u1, text="Called and explained process"
        )

        # Lead 3
        Lead.objects.create(
            name="Rohan Mehta", phone="9988776655", email="rohan@gmail.com",
            city="Pune", state="Maharashtra", service="Trademark Registration",
            message="Logo trademark", status="IN_PROGRESS", agent=a2
        )

        # Lead 4
        Lead.objects.create(
            name="Kavya Nair", phone="8877665544", email="kavya@gmail.com",
            city="Bengaluru", state="Karnataka", service="FSSAI License",
            message="Food business", status="COMPLETED", agent=a1
        )

        # Lead 5
        Lead.objects.create(
            name="Deepak Singh", phone="7766554433", email="deepak@gmail.com",
            city="Lucknow", state="Uttar Pradesh", service="ISO Certification",
            message="Manufacturing unit", status="REJECTED", agent=None
        )
        print("5 sample leads seeded successfully.")
    else:
        print("Leads already exist in the database.")

    print("Seeding finished successfully!")

if __name__ == '__main__':
    seed_database()
