<script lang="ts">
    import { Button } from '$lib/components/ui/button';
    import { Home, CalendarPlus, Calendar, Users, Settings } from 'lucide-svelte';

    import UsersTable from '$lib/components/UsersTable.svelte';

    let active = 'dashboard';
    let ActiveComponent: typeof UsersTable | null = null;

    const menu = [
        { key: 'create', label: 'Create Schedule', icon: CalendarPlus },
        { key: 'edit', label: 'Edit Schedule', icon: Calendar },
        { key: 'users', label: 'Manage Users', icon: Users },
        { key: 'settings', label: 'Settings', icon: Settings }
    ];

    const componentMap = {
        users: UsersTable,
        // Add other mappings here
    };

    type ComponentKey = keyof typeof componentMap;

    function select(key: string) {
        active = key;
        ActiveComponent = componentMap[key as ComponentKey] ?? null;
    }
</script>

    <!-- Sidebar -->
    <aside class="h-screen w-64 bg-white border-r flex flex-col px-4">
        <nav class="flex-1 flex flex-col gap-3 mt-5">
            {#each menu as item}
                <Button
                    variant={active === item.key ? 'secondary' : 'ghost'}
                    class="justify-start gap-3 w-full"
                    onclick={() => select(item.key)}
                >
                    <svelte:component this={item.icon} class="w-5 h-5" />
                    {item.label}
                </Button>   
            {/each}
        </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1 h-full p-6">
        {#if ActiveComponent}
            <svelte:component this={ActiveComponent} />
        {/if}
    </main>

