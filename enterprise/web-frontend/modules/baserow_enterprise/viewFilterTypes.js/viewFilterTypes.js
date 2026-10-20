import { ViewFilterType } from '@baserow/modules/database/viewFilters'
import ViewFilterTypeTeamDropdown from '@baserow_enterprise/components/view/ViewFilterTypeTeamDropdown'

export class TeamIsFilterType extends ViewFilterType {
  static getType() {
    return 'team_is'
  }

  getName() {
    const { $i18n: i18n } = this.app
    return i18n.t('viewFilter.isTeam')
  }

  getExample() {
    return '1'
  }

  getInputComponent() {
    return ViewFilterTypeTeamDropdown
  }

  getCompatibleFieldTypes() {
    return ['created_by', 'last_modified_by']
  }

  isAllowedInPublicViews() {
    return false
  }

  matches(rowValue, filterValue, field, fieldType) {
    // Team membership is resolved server-side; client-side always passes
    // so rows aren't hidden before the backend query returns.
    return true
  }
}

export class TeamIsNotFilterType extends ViewFilterType {
  static getType() {
    return 'team_is_not'
  }

  getName() {
    const { $i18n: i18n } = this.app
    return i18n.t('viewFilter.isNotTeam')
  }

  getExample() {
    return '1'
  }

  getInputComponent() {
    return ViewFilterTypeTeamDropdown
  }

  getCompatibleFieldTypes() {
    return ['created_by', 'last_modified_by']
  }

  isAllowedInPublicViews() {
    return false
  }

  matches(rowValue, filterValue, field, fieldType) {
    return true
  }
}
