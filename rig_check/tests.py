from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ambulance, Checklist, ChecklistItem, RigCheck, RigCheckItem

class RigCheckLogicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.ambulance = Ambulance.objects.create(name='Ambulance 01', is_in_service=True)
        self.checklist = Checklist.objects.create(name='Daily Checklist')
        self.critical_item = ChecklistItem.objects.create(
            checklist=self.checklist,
            name='Defibrillator',
            is_critical=True
        )
        self.non_critical_item = ChecklistItem.objects.create(
            checklist=self.checklist,
            name='Stethoscope',
            is_critical=False
        )
        self.rig_check = RigCheck.objects.create(
            ambulance=self.ambulance,
            checklist=self.checklist,
            user=self.user
        )

    def test_failed_non_critical_item_does_not_affect_service_status(self):
        """
        Tests that failing a non-critical item does not take the ambulance out of service.
        """
        RigCheckItem.objects.create(
            rig_check=self.rig_check,
            checklist_item=self.non_critical_item,
            status='Fail'
        )
        self.ambulance.refresh_from_db()
        self.assertTrue(self.ambulance.is_in_service, "Ambulance should still be in service after a non-critical failure.")

    def test_failed_critical_item_takes_ambulance_out_of_service(self):
        """
        Tests that failing a critical item correctly takes the ambulance out of service.
        """
        self.assertTrue(self.ambulance.is_in_service)
        RigCheckItem.objects.create(
            rig_check=self.rig_check,
            checklist_item=self.critical_item,
            status='Fail'
        )
        self.ambulance.refresh_from_db()
        self.assertFalse(self.ambulance.is_in_service, "Ambulance should be taken out of service after a critical failure.")

    def test_passed_critical_item_does_not_affect_service_status(self):
        """
        Tests that passing a critical item does not change the ambulance's service status.
        """
        # First, fail a critical item to take it out of service
        RigCheckItem.objects.create(
            rig_check=self.rig_check,
            checklist_item=self.critical_item,
            status='Fail'
        )
        self.ambulance.refresh_from_db()
        self.assertFalse(self.ambulance.is_in_service)

        # Now, create a new check and pass the item
        new_rig_check = RigCheck.objects.create(
            ambulance=self.ambulance,
            checklist=self.checklist,
            user=self.user
        )
        RigCheckItem.objects.create(
            rig_check=new_rig_check,
            checklist_item=self.critical_item,
            status='Pass'
        )
        self.ambulance.refresh_from_db()
        self.assertFalse(self.ambulance.is_in_service, "Passing a critical item should not automatically put an ambulance back in service.")
