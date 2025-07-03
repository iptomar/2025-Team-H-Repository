<script lang="ts">
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import { redirect } from '@sveltejs/kit';

	onMount(() => {
		goto("/login");
	})

	export const load = () => {
		throw redirect(307, '/home');
	};
</script>

