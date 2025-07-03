<script lang="ts">
import { goto } from '$app/navigation';
import { isAuthenticated } from '$lib/stores/auth';
import { onMount } from 'svelte';
let username = '';

onMount(() => {
  username = localStorage.getItem('username') || '';
});
</script>

<main class="min-h-screen w-full flex items-center justify-center relative">
  <div class="absolute inset-0 bg-cover bg-center" style="background-image: url(https://portal2.ipt.pt/img/generico/estt-ext.jpg);"></div>
  <div class="absolute inset-0 bg-black opacity-60"></div>
  <div class="relative z-10 flex items-center justify-center w-full h-full">
    <div class="bg-white bg-opacity-80 rounded-xl shadow-lg p-10 flex flex-col items-center max-w-lg mx-auto">
      {#if $isAuthenticated}
        <h1 class="text-3xl font-bold text-blue-700 mb-4">Welcome back{#if username}, {username}{/if}!</h1>
        <p class="text-lg text-gray-700 mb-8 text-center">Ready to manage your academic schedule?</p>
        <button class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition" on:click={() => goto('/timetable')}>Go to Timetable</button>
      {:else}
        <h1 class="text-4xl font-bold text-blue-700 mb-4">Welcome to the Timetable System</h1>
        <p class="text-lg text-gray-700 mb-8 text-center">Easily manage your academic schedule. Login or create an account to get started.</p>
        <div class="flex gap-4">
          <button class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition" on:click={() => goto('/login')}>Login</button>
          <button class="px-6 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition" on:click={() => goto('/register')}>Create Account</button>
        </div>
      {/if}
    </div>
  </div>
</main> 