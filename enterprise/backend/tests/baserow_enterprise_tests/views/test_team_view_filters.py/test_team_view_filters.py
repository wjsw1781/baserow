import pytest

from baserow.contrib.database.views.handler import ViewHandler


@pytest.mark.field_last_modified_by
@pytest.mark.django_db
def test_team_is_filter_type(data_fixture, enterprise_data_fixture):
    user = data_fixture.create_user()
    user2 = data_fixture.create_user()
    user3 = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    grid_view = data_fixture.create_grid_view(table=table)
    last_modified_by_field = data_fixture.create_last_modified_by_field(table=table)

    workspace = table.database.workspace
    team = enterprise_data_fixture.create_team(workspace=workspace)
    # user and user2 are in the team, user3 is not
    enterprise_data_fixture.create_subject(team=team, subject=user)
    enterprise_data_fixture.create_subject(team=team, subject=user2)

    handler = ViewHandler()
    model = table.get_model()

    row_user = model.objects.create(**{f"last_modified_by": user})
    row_user2 = model.objects.create(**{f"last_modified_by": user2})
    row_user3 = model.objects.create(**{f"last_modified_by": user3})
    row_none = model.objects.create(**{f"last_modified_by": None})

    data_fixture.create_view_filter(
        view=grid_view,
        field=last_modified_by_field,
        type="team_is",
        value=str(team.id),
    )
    ids = [r.id for r in handler.apply_filters(grid_view, model.objects.all()).all()]
    assert len(ids) == 2
    assert row_user.id in ids
    assert row_user2.id in ids
    assert row_user3.id not in ids
    assert row_none.id not in ids


@pytest.mark.field_last_modified_by
@pytest.mark.django_db
def test_team_is_not_filter_type(data_fixture, enterprise_data_fixture):
    user = data_fixture.create_user()
    user2 = data_fixture.create_user()
    user3 = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    grid_view = data_fixture.create_grid_view(table=table)
    last_modified_by_field = data_fixture.create_last_modified_by_field(table=table)

    workspace = table.database.workspace
    team = enterprise_data_fixture.create_team(workspace=workspace)
    enterprise_data_fixture.create_subject(team=team, subject=user)
    enterprise_data_fixture.create_subject(team=team, subject=user2)

    handler = ViewHandler()
    model = table.get_model()

    row_user = model.objects.create(**{f"last_modified_by": user})
    row_user2 = model.objects.create(**{f"last_modified_by": user2})
    row_user3 = model.objects.create(**{f"last_modified_by": user3})
    row_none = model.objects.create(**{f"last_modified_by": None})

    data_fixture.create_view_filter(
        view=grid_view,
        field=last_modified_by_field,
        type="team_is_not",
        value=str(team.id),
    )
    ids = [r.id for r in handler.apply_filters(grid_view, model.objects.all()).all()]
    assert len(ids) == 2
    assert row_user3.id in ids
    assert row_none.id in ids
    assert row_user.id not in ids
    assert row_user2.id not in ids


@pytest.mark.field_last_modified_by
@pytest.mark.django_db
def test_team_is_filter_empty_team(data_fixture, enterprise_data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    grid_view = data_fixture.create_grid_view(table=table)
    last_modified_by_field = data_fixture.create_last_modified_by_field(table=table)

    workspace = table.database.workspace
    # team with no members
    team = enterprise_data_fixture.create_team(workspace=workspace)

    handler = ViewHandler()
    model = table.get_model()

    row = model.objects.create(**{f"last_modified_by": user})

    data_fixture.create_view_filter(
        view=grid_view,
        field=last_modified_by_field,
        type="team_is",
        value=str(team.id),
    )
    ids = [r.id for r in handler.apply_filters(grid_view, model.objects.all()).all()]
    assert len(ids) == 0


@pytest.mark.field_last_modified_by
@pytest.mark.django_db
def test_team_is_filter_invalid_value(data_fixture, enterprise_data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    grid_view = data_fixture.create_grid_view(table=table)
    last_modified_by_field = data_fixture.create_last_modified_by_field(table=table)

    handler = ViewHandler()
    model = table.get_model()

    row = model.objects.create(**{f"last_modified_by": user})

    data_fixture.create_view_filter(
        view=grid_view,
        field=last_modified_by_field,
        type="team_is",
        value="not_a_number",
    )
    ids = [r.id for r in handler.apply_filters(grid_view, model.objects.all()).all()]
    assert len(ids) == 1  # invalid value -> Q() returns all rows
    assert row.id in ids


@pytest.mark.field_last_modified_by
@pytest.mark.django_db
def test_team_is_filter_created_by_field(data_fixture, enterprise_data_fixture):
    user = data_fixture.create_user()
    user2 = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    grid_view = data_fixture.create_grid_view(table=table)
    created_by_field = data_fixture.create_created_by_field(table=table)

    workspace = table.database.workspace
    team = enterprise_data_fixture.create_team(workspace=workspace)
    enterprise_data_fixture.create_subject(team=team, subject=user)

    handler = ViewHandler()
    model = table.get_model()

    row_user = model.objects.create(**{f"created_by": user})
    row_user2 = model.objects.create(**{f"created_by": user2})

    data_fixture.create_view_filter(
        view=grid_view,
        field=created_by_field,
        type="team_is",
        value=str(team.id),
    )
    ids = [r.id for r in handler.apply_filters(grid_view, model.objects.all()).all()]
    assert len(ids) == 1
    assert row_user.id in ids
