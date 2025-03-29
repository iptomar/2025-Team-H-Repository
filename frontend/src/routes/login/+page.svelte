<script lang="ts">
	import UserLoginForm from '$lib/components/UserLoginForm.svelte';
	import { Button } from '$lib/components/ui/button';
</script>

<main>
	<div
		class="container relative hidden h-screen flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0"
	>
		<Button href="/register" variant="ghost" class="absolute right-4 top-4 md:right-8 md:top-8">
			Criar conta
		</Button>
		<div class="relative hidden h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex">
			<div
				class="absolute inset-0 bg-cover"
				style=" background-image: url(https://portal2.ipt.pt/img/generico/estt-ext.jpg);"
			></div>
		</div>
		<div class="lg:p-8">
			<div class="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
				<div class="flex flex-col space-y-2 text-center">
					<h1 class="text-2xl font-semibold tracking-tight">Efetuar Login</h1>
					<p class="text-sm text-muted-foreground">Introduza o seu email e password</p>
				</div>
				<UserLoginForm />
			</div>
		</div>
	</div>
</main>
