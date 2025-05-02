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
		name: "Rodrigo Sampaio",
		email: "rodrigo@example.com",
		role: "Admin",
		school: "Politécnico Tomar",
		course: "Engenharia Informática"
	  },
	  {
		id: 2,
		name: "Florence Shaw",
		email: "florence@untitledul.com",
		role: "Admin",
		school: "University A",
		course: "Computer Science"
	  },
	  // Add more users...
	];
  
	// State for search and pagination
	let searchTerm = '';
	let currentPage = 1;
	const usersPerPage = 5;
  
	// Filter users based on search term
	$: filteredUsers = users.filter(user => 
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
	  <div class="mb-6 flex justify-between items-center">
		<div>
		  <h1 class="text-2xl font-bold">User Management</h1>
		</div>
		<Button variant="default">Add User</Button>
	  </div>
  
	  <!-- Search and Filter Bar -->
	  <div class="mb-6 flex items-center justify-between">
		<div class="relative w-64">
		  <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
		  <Input
			bind:value={searchTerm}
			placeholder="Search users..."
			class="pl-10"
		  />
		</div>
	  </div>
  
	  <!-- Users Table -->
	  <div class="rounded-lg border shadow-sm overflow-hidden">
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
				  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
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
				<Table.Cell class="px-4 py-6 text-center text-gray-500">
				  No users found
				</Table.Cell>
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
		  </span> of <span class="font-medium">{filteredUsers.length}</span> users
		</div>
		<div class="flex space-x-2">
		  <Button
			variant="outline"
			size="sm"
			onclick={prevPage}
			disabled={currentPage === 1}
		  >
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