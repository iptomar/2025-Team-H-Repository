<script lang="ts">
  import Sidebar from "$lib/components/Sidebar.svelte";
  import Navbar from "$lib/components/Navbar.svelte";
</script>

<!-- Full screen vertical layout -->
<div class="flex flex-col h-screen">

  <!-- Navbar at the top -->
  <div class="w-full">
    <Navbar />
  </div>

  <!-- Main area: Sidebar + Content -->
  <div class="flex flex-1 overflow-hidden">
    <Sidebar />
  </div>
</div>
