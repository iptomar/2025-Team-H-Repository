<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table';
	import { cn } from '$lib/utils.js';
	import { Input } from '$lib/components/ui/input';
	import { ChevronLeft, ChevronRight, Search } from 'lucide-svelte';

	// Sample user data
	const users = [
		{
			id: 1,
			name: 'Rodrigo Sampaio',
			email: 'rodrigo@example.com',
			role: 'Admin',
			school: 'Politécnico Tomar',
			course: 'Engenharia Informática'
		},
		{
			id: 2,
			name: 'Florence Shaw',
			email: 'florence@untitledul.com',
			role: 'Admin',
			school: 'University A',
			course: 'Computer Science'
		}
		// Add more users...
	];

	let showModal = false;

	// State for search and pagination
	let searchTerm = '';
	let currentPage = 1;
	const usersPerPage = 5;

	// Filter users based on search term
	$: filteredUsers = users.filter((user) =>
		user.name.toLowerCase().includes(searchTerm.toLowerCase())
	);

	// Pagination calculations
	$: totalPages = Math.ceil(filteredUsers.length / usersPerPage);
	$: paginatedUsers = filteredUsers.slice(
		(currentPage - 1) * usersPerPage,
		currentPage * usersPerPage
	);

	// Navigation functions
	function nextPage() {
		if (currentPage < totalPages) currentPage++;
	}

	function prevPage() {
		if (currentPage > 1) currentPage--;
	}

	function goToPage(page: number) {
		currentPage = page;
	}
</script>

<div class="flex min-h-screen">
	<!-- Main Content -->
	<div class="flex-1 p-8">
		<div class="mb-6 flex items-center justify-between">
			<!-- Search and Filter Bar -->
			<div class="flex items-center justify-between">
				<div class="relative w-64">
					<Search
						class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 transform text-gray-400"
					/>
					<Input bind:value={searchTerm} placeholder="Search users..." class="pl-10" />
				</div>
			</div>

			<Button variant="default" onclick={() => (showModal = true)}>Add User</Button>

			{#if showModal}
				<!-- Modal Overlay -->
				<div class="fixed inset-0 z-40 flex items-center justify-center bg-black bg-opacity-40">
					<!-- Modal Content -->
					<div class="z-50 w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
						<h2 class="mb-4 text-xl font-semibold">Add New User</h2>
						<form>
							<div class="mb-3">
								<label for="" class="mb-1 block text-sm font-medium">Name</label>
								<Input />
							</div>
							<div class="mb-3">
								<label for="" class="mb-1 block text-sm font-medium">Email</label>
								<Input type="email" />
							</div>
							<div class="mb-3">
								<label for="" class="mb-1 block text-sm font-medium">Role</label>
								<Input />
							</div>
							<div class="mb-3">
								<label for="" class="mb-1 block text-sm font-medium">School</label>
								<Input />
							</div>
							<div class="mb-4">
								<label for="" class="mb-1 block text-sm font-medium">Course</label>
								<Input />
							</div>
							<div class="flex justify-end space-x-2">
								<Button type="button" variant="outline" onclick={() => (showModal = false)}
									>Cancel</Button
								>
								<Button type="submit" variant="default">Add</Button>
							</div>
						</form>
					</div>
				</div>
			{/if}
		</div>

		<!-- Users Table -->
		<div class="overflow-hidden rounded-lg border shadow-sm">
			<Table.Root class="w-full">
				<Table.Header class="bg-gray-50">
					<Table.Row>
						<Table.Head class="w-[100px] px-4 py-3 text-left text-sm font-semibold text-gray-700">
							User ID
						</Table.Head>
						<Table.Head class="px-4 py-3 text-sm font-semibold text-gray-700">Username</Table.Head>
						<Table.Head class="px-4 py-3 text-sm font-semibold text-gray-700">Role</Table.Head>
						<Table.Head class="px-4 py-3 text-sm font-semibold text-gray-700">School</Table.Head>
						<Table.Head class="px-4 py-3 text-sm font-semibold text-gray-700">Course</Table.Head>
						<Table.Head class="px-4 py-3 text-right text-sm font-semibold text-gray-700">
							Actions
						</Table.Head>
					</Table.Row>
				</Table.Header>
				<Table.Body>
					{#each paginatedUsers as user (user.id)}
						<Table.Row class="hover:bg-gray-50">
							<Table.Cell class="px-4 py-2 font-medium text-gray-800">{user.id}</Table.Cell>
							<Table.Cell class="px-4 py-2 text-gray-600">
								<div class="flex flex-col">
									<span>{user.name}</span>
									<span class="text-sm text-gray-500">{user.email}</span>
								</div>
							</Table.Cell>
							<Table.Cell class="px-4 py-2 text-gray-600">
								<span
									class="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800"
								>
									{user.role}
								</span>
							</Table.Cell>
							<Table.Cell class="px-4 py-2 text-gray-600">{user.school}</Table.Cell>
							<Table.Cell class="px-4 py-2 text-gray-600">{user.course}</Table.Cell>
							<Table.Cell class="px-4 py-2 text-right">
								<div class="flex justify-end space-x-2">
									<Button size="sm" variant="outline">Edit</Button>
									<Button size="sm" variant="destructive">Delete</Button>
								</div>
							</Table.Cell>
						</Table.Row>
					{:else}
						<Table.Row>
							<Table.Cell class="px-4 py-6 text-center text-gray-500">No users found</Table.Cell>
						</Table.Row>
					{/each}
				</Table.Body>
			</Table.Root>
		</div>

		<!-- Pagination -->
		<div class="mt-6 flex items-center justify-between">
			<div class="text-sm text-gray-500">
				Showing <span class="font-medium">{(currentPage - 1) * usersPerPage + 1}</span> to
				<span class="font-medium">
					{Math.min(currentPage * usersPerPage, filteredUsers.length)}
				</span>
				of <span class="font-medium">{filteredUsers.length}</span> users
			</div>
			<div class="flex space-x-2">
				<Button variant="outline" size="sm" onclick={prevPage} disabled={currentPage === 1}>
					<ChevronLeft class="h-4 w-4" />
				</Button>

				{#each Array.from({ length: totalPages }, (_, i) => i + 1) as page}
					<Button
						variant={page === currentPage ? 'default' : 'outline'}
						size="sm"
						onclick={() => goToPage(page)}
					>
						{page}
					</Button>
				{/each}

				<Button
					variant="outline"
					size="sm"
					onclick={nextPage}
					disabled={currentPage === totalPages || totalPages === 0}
				>
					<ChevronRight class="h-4 w-4" />
				</Button>
			</div>
		</div>
	</div>
</div>
