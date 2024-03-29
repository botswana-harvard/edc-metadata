from django.apps import apps as django_apps


class MetadataGetter:

    """A class that gets a filtered queryset of metadata --
    `metadata_objects`.
    """

    metadata_model = None

    def __init__(self, appointment=None, subject_identifier=None, visit_code=None,
                 visit_code_sequence=None, schedule_name=None):
        try:
            self.visit = appointment.visit
        except AttributeError:
            self.subject_identifier = subject_identifier
            self.visit_code = visit_code
            self.visit_code_sequence = visit_code_sequence
            self.schedule_name = schedule_name
        else:
            self.subject_identifier = self.visit.subject_identifier
            self.visit_code = self.visit.visit_code
            self.visit_code_sequence = self.visit.visit_code_sequence
            self.schedule_name = self.visit.schedule_name
        self.metadata_objects = self.metadata_model_cls.objects.filter(
            **self.options).order_by('show_order')

    @property
    def metadata_model_cls(self):
        return django_apps.get_model(self.metadata_model)

    @property
    def options(self):
        """Returns a dictionary of query options.
        """
        options = dict(
            subject_identifier=self.subject_identifier,
            visit_code=self.visit_code,
            visit_code_sequence=self.visit_code_sequence)
        if self.schedule_name:
            options.update(schedule_name=self.schedule_name)
        return options

    def next_object(self, show_order=None, entry_status=None):
        """Returns the next model instance based on the show order.
        """
        opts = {'show_order__gt': show_order}
        if entry_status:
            opts.update(entry_status=entry_status)
        return self.metadata_objects.filter(**opts).order_by('show_order').first()
