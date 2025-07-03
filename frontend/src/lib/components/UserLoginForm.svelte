<script lang="ts">
	import { Button } from '$lib/components/ui/button/';
	import { Input } from '$lib/components/ui/input/';
	import { Label } from '$lib/components/ui/label/';
	import { cn } from '$lib/utils';
	import { auth } from '$lib/api';
	import { goto } from '$app/navigation';
	import { isAuthenticated } from '$lib/stores/auth';

	let className: string | undefined | null = undefined;
	export { className as class };

	let isLoading = false;
	let email = '';
	let password = '';
	let error = '';

	async function onSubmit() {
		isLoading = true;
		error = '';

		try {
			const loginResponse = await auth.login({
				username: email, // API expects 'username' field
				password: password
			});

			// Login successful - set auth state and redirect
			isAuthenticated.set(true);
			console.log('Login successful:', loginResponse.user);
			localStorage.setItem('access_token', loginResponse.access_token);
			localStorage.setItem('username', email);
			await goto('/home');
			
		} catch (err) {
			error = err instanceof Error ? err.message : 'Login failed';
			console.error('Login error:', err);
		} finally {
			isLoading = false;
		}
	}
</script>

<div class={cn('grid gap-6', className)} {...$$restProps}>
	<form on:submit|preventDefault={onSubmit}>
		<div class="grid gap-2">
			<div class="grid gap-1">
				<Label class="sr-only" for="email">Email</Label>
				<Input
					id="email"
					bind:value={email}
					placeholder="nome@ipt.pt"
					type="email"
					autocapitalize="none"
					autocomplete="email"
					autocorrect="off"
					disabled={isLoading}
					required
				/>
				<Label class="sr-only" for="password">Password</Label>
				<Input
					id="password"
					bind:value={password}
					placeholder="password"
					type="password"
					autocomplete="current-password"
					autocorrect="off"
					disabled={isLoading}
					required
				/>
			</div>
			
			{#if error}
				<div class="text-sm text-red-600 bg-red-50 p-2 rounded">
					{error}
				</div>
			{/if}
			
			<Button type="submit" class="w-full" disabled={isLoading}>
				{#if isLoading}
					Logging in...
				{:else}
					Login
				{/if}
			</Button>
		</div>
	</form>
</div>
