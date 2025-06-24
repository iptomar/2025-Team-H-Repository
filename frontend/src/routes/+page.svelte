<script lang="ts">
	import { Button } from '$lib/components/ui/button';
</script>

<main>
	<div class="container relative hidden h-screen flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0">
		<!-- Left: Campus Image (same as login page) -->
		<div class="relative hidden h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex">
			<div
				class="absolute inset-0 bg-cover bg-center"
				style="background-image: url(https://portal2.ipt.pt/img/generico/estt-ext.jpg);"
			></div>
		</div>
		<!-- Right: Minimal Content -->
		<div class="flex flex-col items-center justify-center w-full h-full bg-black text-white lg:p-8">
			<div class="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
				<div class="flex flex-col space-y-2 text-center">
					<div class="flex items-center justify-center mb-4">
						<div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center">
							<span class="text-white font-bold text-xl">IPT</span>
						</div>
					</div>
					<h1 class="text-3xl font-semibold tracking-tight mb-2">IPT Timetable System</h1>
					<p class="text-base text-muted-foreground mb-6">Welcome! Manage your academic schedules in a simple and efficient way.</p>
				</div>
				<div class="flex flex-col gap-4">
					<Button href="/login" class="w-full" size="lg">To enter</Button>
					<Button href="/register" class="w-full" variant="outline" size="lg">Create Account</Button>
				</div>
			</div>
		</div>
	</div>
</main>
