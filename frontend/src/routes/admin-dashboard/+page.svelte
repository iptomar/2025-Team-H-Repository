<script lang="ts">
    import AdminDashboard from "$lib/components/AdminDashboard.svelte";
</script>


<nav class="bg-black text-white shadow-md">
    <div class="flex items-center justify-between p-4">
        <h1 class="text-2xl font-bold">Admin Dashboard</h1>
        <div class="flex space-x-4">
            <a href="/admin-dashboard" class="hover:underline">Dashboard</a>
            <a href="/admin-users" class="hover:underline">Users</a>
            <a href="/admin-settings" class="hover:underline">Settings</a>
        </div>
    </div>
</nav>
<div>
    <AdminDashboard />
</div>