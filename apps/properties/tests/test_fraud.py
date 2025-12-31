from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.accounts.models import User
from apps.properties.models import Property, PropertyImage


class FraudDetectionTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='landlord1', password='pass')
        self.user2 = User.objects.create_user(username='landlord2', password='pass')

        self.prop1 = Property.objects.create(
            owner=self.user1,
            title='Nice Room 1',
            description='Desc',
            area='Thamel',
            address='Addr 1',
            price_per_month=10000
        )
        self.prop2 = Property.objects.create(
            owner=self.user2,
            title='Nice Room 2',
            description='Desc',
            area='Thamel',
            address='Addr 2',
            price_per_month=12000
        )

    def test_duplicate_image_flags_properties(self):
        # Create two images with identical bytes
        img_bytes = b"fake-image-bytes"
        img1 = SimpleUploadedFile('img1.jpg', img_bytes, content_type='image/jpeg')
        img2 = SimpleUploadedFile('img2.jpg', img_bytes, content_type='image/jpeg')

        pimg1 = PropertyImage.objects.create(property=self.prop1, image=img1)
        pimg2 = PropertyImage.objects.create(property=self.prop2, image=img2)

        self.prop1.refresh_from_db()
        self.prop2.refresh_from_db()

        self.assertTrue(self.prop1.is_flagged)
        self.assertTrue(self.prop2.is_flagged)
        self.assertGreaterEqual(self.prop1.flag_count, 1)
        self.assertGreaterEqual(self.prop2.flag_count, 1)
        self.assertIn('Duplicate image detected', (self.prop1.fraud_reason or ''))
