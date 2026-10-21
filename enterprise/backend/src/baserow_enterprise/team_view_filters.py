"""
Team-based view filter for created_by/last_modified_by fields.

Allows filtering rows where the creator/last_modifier belongs to a specific Team.
This is the enterprise extension of the core "user_is" filter, but instead of
filtering by a single user, it filters by all users in a Team.
"""

from django.db.models import Q

from baserow.contrib.database.fields.field_types import (
    CreatedByFieldType,
    LastModifiedByFieldType,
)
from baserow.contrib.database.views.registries import ViewFilterType


class TeamIsViewFilterType(ViewFilterType):
    """
    The team_is filter accepts the ID of a Team and filters rows where the
    created_by / last_modified_by user belongs to that Team.
    """

    type = "team_is"
    compatible_field_types = [CreatedByFieldType.type, LastModifiedByFieldType.type]

    def get_filter(self, field_name, value, model_field, field):
        if not value:
            return Q()
        value = value.strip()
        try:
            team_id = int(value)
        except ValueError:
            return Q()

        # Resolve all user IDs that belong to this Team via TeamSubject.
        from baserow_enterprise.teams.models import TeamSubject
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user_content_type = ContentType.objects.get_for_model(User)

        user_ids = list(
            TeamSubject.objects_and_trash.filter(
                team_id=team_id,
                subject_type=user_content_type,
            ).values_list("subject_id", flat=True)
        )

        if not user_ids:
            # No members in this team -> match nothing.
            return Q(**{f"{field_name}__id__in": [-1]})

        return Q(**{f"{field_name}__id__in": user_ids})


class TeamIsNotViewFilterType(ViewFilterType):
    """
    The team_is_not filter - negation of team_is.
    Filters rows where created_by / last_modified_by user does NOT belong to the
    Team.
    """

    type = "team_is_not"
    compatible_field_types = [CreatedByFieldType.type, LastModifiedByFieldType.type]

    def get_filter(self, field_name, value, model_field, field):
        if not value:
            return Q()
        value = value.strip()
        try:
            team_id = int(value)
        except ValueError:
            return Q()

        from baserow_enterprise.teams.models import TeamSubject
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user_content_type = ContentType.objects.get_for_model(User)

        user_ids = list(
            TeamSubject.objects_and_trash.filter(
                team_id=team_id,
                subject_type=user_content_type,
            ).values_list("subject_id", flat=True)
        )

        if not user_ids:
            # No members in this team -> match everything (nobody is excluded).
            return Q()

        return ~Q(**{f"{field_name}__id__in": user_ids})
