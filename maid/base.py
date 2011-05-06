from django.db.models.signals import post_delete, pre_save, post_save
import weakref


class FileFieldRegistry(object):
    
    # Maps models to a set of file field properties whose files should be
    # deleted when orphaned.
    _registered_fields = {}
    
    # Maps model instances that are about to be saved to their old versions.
    _old_instances = weakref.WeakKeyDictionary()
    
    def register(self, model, field_names):
        """
        Registers a FileField with the maid. When a new file is saved or the
        current value is deleted, she'll get rid of the old file.
        """
        
        if model not in self._registered_fields:
            # If this is the first time the model is being registered, connect
            # our signals.
            post_delete.connect(self._model_post_delete, sender=model)
            pre_save.connect(self._model_pre_save, sender=model)
            post_save.connect(self._model_post_save, sender=model)
            
        # Register the new fields.
        self._registered_fields[model] = self._registered_fields.get(model, set()) | set(field_names)

    def _model_pre_save(self, instance, sender, **kwargs):
        # We don't need to check for changed file fields if this is a new
        # instance.
        if instance.pk:
            old_instance = sender._default_manager.get(pk=instance.pk)
            self._old_instances[instance] = old_instance

    def _model_post_save(self, instance, sender, **kwargs):
        try:
            old_instance = self._old_instances.pop(instance)
        except KeyError:
            pass
        else:
            for field_name in self._registered_fields[sender]:
                old_file = getattr(old_instance, field_name)
                new_file = getattr(instance, field_name)
                if old_file != new_file:
                    self._delete(old_instance, field_name)

    def _model_post_delete(self, instance, sender, **kwargs):
        # This is just re-adding what changeset 1531
        # (http://code.djangoproject.com/changeset/15321) removed.
        for field_name in self._registered_fields[sender]:
            self._delete(instance, field_name)

    @staticmethod
    def _delete(instance, field_name):
        model_type = instance.__class__
        field = model_type._meta.get_field(field_name)
        file = getattr(instance, field_name)
    
        # If no other object of this type references the file, 
        # and it's not the default value for future objects, 
        # delete it from the backend.
        if file and file.name != field.default and \
            not model_type._default_manager.filter(**{field.name: file.name}).exclude(pk=instance.pk):
                # Don't save the instance because that would trigger the
                # pre_save signal again.
                file.delete(save=False) 
        elif file:
            # Otherwise, just close the file, so it doesn't tie up resources. 
            file.close()


# The registry instance.
file_field_registry = FileFieldRegistry()


def register_file_fields(model, *fields):
    """
    Register a FileField (or similar) to have its unused files automatically
    deleted.
    """
    file_field_registry.register(model, fields)
