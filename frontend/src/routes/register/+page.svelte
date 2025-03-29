<script lang="ts">
	import UserRegisterForm from '$lib/components/UserRegisterForm.svelte';
	import { Button } from '$lib/components/ui/button';
</script>

<main>
	<div
		class="container relative hidden h-screen flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0"
	>
		<Button
			href="/login"
			variant="ghost"
			class="absolute right-4 top-4 md:right-8 md:top-8"
		>
			Login
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
					<h1 class="text-2xl font-semibold tracking-tight">Criar uma conta</h1>
					<p class="text-sm text-muted-foreground">Introduza o seu email para criar conta</p>
				</div>
				<UserRegisterForm />
				<p class="px-8 text-center text-sm text-muted-foreground">
					Ao continuar, aceita os nossos
					<a href="/terms" class="underline underline-offset-4 hover:text-primary">
						Termos de Serviço
					</a>
					e
					<a href="/privacy" class="underline underline-offset-4 hover:text-primary">
						Política de Privacidade
					</a>
					.
				</p>
			</div>
		</div>
	</div>
</main>
