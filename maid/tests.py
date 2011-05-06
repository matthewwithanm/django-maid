from django.test import TestCase
import tempfile
import os.path
import maid
from django.core.files.base import File
from django.db import models


class TestModel(models.Model):
    document = models.FileField(upload_to='testmodel')

class TestModel2(models.Model):
    document = models.FileField(upload_to='testmodel')

maid.register_file_fields(TestModel, ['document'])
maid.register_file_fields(TestModel2)


def _create_file(filename):
    filename = os.path.join(tempfile.gettempdir(), filename)
    file = File(open(filename, 'w+'))
    file.write(filename)
    return file


def _create_model_instance(model, filename):
    return model.objects.create(document=_create_file(filename))


class FileFieldCleanupTest(TestCase):
    
    def test_delete_model_1(self):
        self._test_delete_model(TestModel)
    
    def test_delete_model_2(self):
        self._test_delete_model(TestModel2)
    
    def test_save_new(self):
        self._test_save_new(TestModel)
    
    def test_save_new_2(self):
        self._test_save_new(TestModel2)
    
    def _test_delete_model(self, model):
        model = _create_model_instance(model, 'file_1.txt')
        file_path = model.document.path
        model.delete()
        self.assertFileExists(file_path, False)
    
    def _test_save_new(self, model):
        model = _create_model_instance(model, 'file_2.txt')
        old_path = model.document.path
        model.document = _create_file('file_2.txt')
        model.save()
        self.assertFileExists(old_path, False)
        self.assertFileExists(model.document.path)

    def assertFileExists(self, file_path, assertion=True):
        # Verify that the file was deleted.
        try:
            open(file_path)
        except IOError:
            file_exists = False
        else:
            file_exists = True
        
        if assertion:
            self.assertTrue(file_exists, 'The file %s does not exist.' % file_path)
        else:
            self.assertFalse(file_exists, 'The file %s was not deleted.' % file_path)
