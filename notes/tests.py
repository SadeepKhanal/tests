from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Note
class NoteTestCase(TestCase):
    def test_create_note_successfully(self):
        note = Note.objects.create(
            title="Sample Note - Sadeep Khanal Roll 31",
            content="This note content is valid and long enough."
        )

        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(note.title,
                         "Sample Note - Sadeep Khanal Roll 31")
        self.assertEqual(note.content,
                         "This note content is valid and long enough.")
        print("PASS: test_create_note_successfully - Sadeep Khanal-Roll: 31")
    def test_validation_error_for_short_content(self):
        """Ensure validation fails when note content is too short."""
        note = Note(
            title="Invalid Note",
            content="Small"
        )
        with self.assertRaises(ValidationError) as error:
            note.full_clean()
        self.assertIn(
            "Content must contain at least 10 characters.",
            str(error.exception)
        )
        print("PASS: test_validation_error_for_short_content - Sadeep Khanal-Roll: 31")