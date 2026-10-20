<template>
  <Dropdown
    :value="copy"
    :disabled="disabled"
    :fixed-items="true"
    :show-empty-value="false"
    :initial-display-name="initialDisplayName"
    class="dropdown--floating filters__value-dropdown"
    @input="input"
  >
    <DropdownItem
      v-for="team in teams"
      :key="team.id"
      :name="team.name"
      :value="team.id"
    ></DropdownItem>
  </Dropdown>
</template>

<script>
import Dropdown from '@baserow/modules/core/components/Dropdown'
import DropdownItem from '@baserow/modules/core/components/DropdownItem'
import viewFilter from '@baserow/modules/database/mixins/viewFilter'
import TeamService from '@baserow_enterprise/services/team'

export default {
  name: 'ViewFilterTypeTeamDropdown',
  components: { Dropdown, DropdownItem },
  mixins: [viewFilter],
  data() {
    return {
      teams: [],
      loading: true,
      loadError: false,
    }
  },
  computed: {
    copy() {
      const value = this.filter.value
      return value === '' ? null : parseInt(value) || null
    },
    initialDisplayName() {
      const selected = this.teams.find((t) => t.id === this.copy)
      return selected?.name
    },
  },
  mounted() {
    this.fetchTeams()
  },
  methods: {
    async fetchTeams() {
      this.loading = true
      this.loadError = false
      try {
        const workspaceId = await this.resolveWorkspaceId()
        if (workspaceId === null) {
          this.loadError = true
          return
        }
        const { data } = await TeamService(this.$client).fetchAll(workspaceId)
        this.teams = data.results || data
      } catch {
        this.loadError = true
      } finally {
        this.loading = false
      }
    },
    async resolveWorkspaceId() {
      // Try to get workspace id from the view's table via the store
      const tableId = this.view?.table_id
      if (tableId === undefined) return null

      // The application store maps databases (applications) to workspaces
      const applications = this.$store.state.application.items || []
      const app = applications.find((a) => {
        const tables = a.tables || []
        return tables.some((t) => t.id === tableId)
      })
      return app?.workspace?.id ?? null
    },
    input(value) {
      value = value === null ? '' : value.toString()
      this.$emit('input', value)
    },
  },
}
</script>
