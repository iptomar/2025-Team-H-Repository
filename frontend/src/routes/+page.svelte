<script lang="ts">
	import { Button } from '$lib/components/ui/button';
</script>

<main class="relative min-h-screen flex items-center justify-center overflow-hidden">
	<!-- Full-screen background image -->
	<div class="absolute inset-0 z-0">
		<img src="https://portal2.ipt.pt/img/generico/estt-ext.jpg" alt="IPT Campus" class="object-cover w-full h-full" />
	</div>

	<!-- Centered content in a black, semi-transparent box -->
	<div class="relative z-10 flex flex-col items-center justify-center w-full max-w-md px-8 py-12 bg-black bg-opacity-80 rounded-2xl shadow-2xl backdrop-blur-sm">
		<div class="flex items-center justify-center mb-6">
			<div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center">
				<span class="text-white font-bold text-xl">IPT</span>
			</div>
		</div>
		<h1 class="text-3xl font-semibold tracking-tight mb-2 text-white text-center">IPT Timetable System</h1>
		<p class="text-base text-gray-300 mb-8 text-center">Welcome! Manage your academic schedules in a simple and efficient way.</p>
		<div class="flex flex-col gap-4 w-full">
			<Button href="/login" class="w-full" size="lg">To enter</Button>
			<Button href="/register" class="w-full" variant="outline" size="lg">Create Account</Button>
		</div>
	</div>
</main>
