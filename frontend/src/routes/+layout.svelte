<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { isAuthenticated } from '$lib/stores/auth';
	import { page } from '$app/stores';

	let mobileMenuOpen = false;
	let showUserMenu = false;
	let username = '';

	function checkAuth() {
		isAuthenticated.set(!!localStorage.getItem('access_token'));
	}

	function logout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('username');
		isAuthenticated.set(false);
		closeUserMenu();
		goto('/home');
	}

	function handleLogoClick() {
		goto('/home');
	}

	function toggleUserMenu() { showUserMenu = !showUserMenu; }
	function closeUserMenu() { showUserMenu = false; }
	function handleUserMenuClick(event) { event.stopPropagation(); }

	onMount(() => {
		checkAuth();
		window.addEventListener('storage', checkAuth);
		username = localStorage.getItem('username') || '';
		document.addEventListener('click', closeUserMenu);
		return () => {
			window.removeEventListener('storage', checkAuth);
			document.removeEventListener('click', closeUserMenu);
		};
	});
</script>

<nav class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50 w-full">
	<div class="flex justify-between h-16 items-center px-8">
		<div class="flex items-center space-x-8">
			<button aria-label="Go to home" on:click={handleLogoClick} class="text-xl font-bold text-blue-600 hover:text-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
				Home
			</button>
			{#if $isAuthenticated}
				<a href="/timetable" class="text-gray-700 hover:text-blue-600 font-medium transition px-2 py-1 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 {($page.url.pathname === '/timetable') ? 'underline font-bold text-blue-700' : ''}">Timetable</a>
				<a href="/professor" class="text-gray-700 hover:text-blue-600 font-medium transition px-2 py-1 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 {($page.url.pathname === '/professor') ? 'underline font-bold text-blue-700' : ''}">Teachers</a>
			{/if}
		</div>
		<!-- Desktop Right Side -->
		<div class="hidden md:flex items-center space-x-4 ml-auto">
			{#if $isAuthenticated}
				<div class="relative flex items-center space-x-2" on:click|stopPropagation={handleUserMenuClick}>
					<button class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-gray-600 font-bold focus:outline-none focus:ring-2 focus:ring-blue-500" on:click={toggleUserMenu} aria-label="User menu">U</button>
					<button class="text-gray-700 text-sm cursor-pointer bg-transparent border-none p-0 m-0 focus:outline-none focus:ring-2 focus:ring-blue-500" on:click={toggleUserMenu} aria-label="Show user info">{username || 'User'}</button>
					{#if showUserMenu}
						<div class="absolute right-0 mt-10 w-48 bg-white rounded shadow-lg p-4 z-50 animate-fade-in">
							<div class="font-semibold text-gray-800 mb-2">User Info</div>
							<div class="text-gray-700 text-sm mb-2">Username: {username || 'User'}</div>
							<button on:click={logout} class="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-500 mt-2">Logout</button>
						</div>
					{/if}
				</div>
			{:else}
				<a href="/register" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition focus:outline-none focus:ring-2 focus:ring-blue-500">Create Account</a>
				<a href="/login" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-500">Login</a>
			{/if}
		</div>
		<!-- Mobile Hamburger -->
		<div class="md:hidden ml-auto flex items-center">
			<button aria-label="Open menu" on:click={() => mobileMenuOpen = !mobileMenuOpen} class="p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 transition">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
				</svg>
			</button>
		</div>
	</div>
	<!-- Mobile Menu -->
	{#if mobileMenuOpen}
		<div class="md:hidden bg-white border-t border-gray-200 px-8 py-4 space-y-2 shadow-lg animate-fade-in">
			{#if $isAuthenticated}
				<a href="/timetable" class="block text-gray-700 hover:text-blue-600 font-medium transition px-2 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 {($page.url.pathname === '/timetable') ? 'underline font-bold text-blue-700' : ''}">Timetable</a>
				<a href="/professor" class="block text-gray-700 hover:text-blue-600 font-medium transition px-2 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 {($page.url.pathname === '/professor') ? 'underline font-bold text-blue-700' : ''}">Teachers</a>
				<div class="relative flex items-center space-x-2" on:click|stopPropagation={handleUserMenuClick}>
					<button class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-gray-600 font-bold focus:outline-none focus:ring-2 focus:ring-blue-500" on:click={toggleUserMenu} aria-label="User menu">U</button>
					<button class="text-gray-700 text-sm cursor-pointer bg-transparent border-none p-0 m-0 focus:outline-none focus:ring-2 focus:ring-blue-500" on:click={toggleUserMenu} aria-label="Show user info">{username || 'User'}</button>
					{#if showUserMenu}
						<div class="absolute right-0 mt-10 w-48 bg-white rounded shadow-lg p-4 z-50 animate-fade-in">
							<div class="font-semibold text-gray-800 mb-2">User Info</div>
							<div class="text-gray-700 text-sm mb-2">Username: {username || 'User'}</div>
							<button on:click={logout} class="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-500 mt-2">Logout</button>
						</div>
					{/if}
				</div>
			{:else}
				<a href="/register" class="block px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition focus:outline-none focus:ring-2 focus:ring-blue-500">Create Account</a>
				<a href="/login" class="block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-500">Login</a>
			{/if}
		</div>
	{/if}
</nav>

<main class="pt-6 w-full px-8">
	<slot />
</main>

<style>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.2s ease;
}
</style>
