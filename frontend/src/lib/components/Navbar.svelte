<script>
	import { goto } from '$app/navigation';

  const pages = [
    { name: 'Dashboard', value: 'dashboard' },
    { name: 'Timetable', value: 'timetable' },
    { name: 'Profile', value: 'profile' }
  ];
</script>

<nav class="bg-white shadow-md w-full px-6 py-3 flex justify-between items-center">
  <div class="text-xl font-bold text-primary">TITLE</div>
  <ul class="flex gap-6 text-gray-700">
    {#each pages as page}
      <li>
        <button
          type="button"
          class="cursor-pointer hover:text-primary bg-transparent border-none p-0 m-0 text-inherit"
          onclick={() => goto(page.value)}
        >
          {page.name}
        </button>
      </li>
    {/each}
  </ul>
</nav>
