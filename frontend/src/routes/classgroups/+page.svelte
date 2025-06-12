<script lang="ts">
	import { onMount } from 'svelte';

	let classgroups = [];
	let showForm = false;
	let editMode = false;
	let editingId: number | null = null;

	let newGroup = {
		subject_id: '',
		group_number: '',
		enrollment_count: '',
		location_id: ''
	};

	async function fetchGroups() {
		const res = await fetch('http://localhost:8000/classgroups');
		classgroups = await res.json();
	}

	async function addGroup() {
	// Validation
	if (
		!newGroup.subject_id ||
		!newGroup.group_number ||
		!newGroup.enrollment_count ||
		!newGroup.location_id
	) {
		alert('Please fill out all fields.');
		return;
	}

	console.log('Sending:', newGroup); // Dev tool logu için

	// PUT vs POST
	const url = editingId !== null
		? `http://localhost:8000/classgroups/${editingId}`
		: 'http://localhost:8000/classgroups';

	const method = editingId !== null ? 'PUT' : 'POST';

	const res = await fetch(url, {
		method,
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			subject_id: parseInt(newGroup.subject_id),
			group_number: parseInt(newGroup.group_number),
			enrollment_count: parseInt(newGroup.enrollment_count),
			location_id: parseInt(newGroup.location_id)
		})
	});

	if (res.ok) {
		await fetchGroups();
		resetForm();
	} else {
		alert(editingId ? 'Failed to update group!' : 'Failed to add group!');
	}
}


	function resetForm() {
		newGroup = {
			subject_id: '',
			group_number: '',
			enrollment_count: '',
			location_id: ''
		};
		showForm = false;
		editMode = false;
		editingId = null;
	}

	function startEdit(group) {
		newGroup = {
			subject_id: String(group.subject_id),
			group_number: String(group.group_number),
			enrollment_count: String(group.enrollment_count),
			location_id: String(group.location_id)
		};
		editingId = group.class_group_id;
		showForm = true;
		editMode = true;
	}

	async function deleteGroup(id: number) {
		const confirmDelete = confirm('Are you sure you want to delete this group?');
		if (!confirmDelete) return;

		const res = await fetch(`http://localhost:8000/classgroups/${id}`, {
			method: 'DELETE'
		});
		if (res.ok) {
			await fetchGroups();
		} else {
			alert('Failed to delete group.');
		}
	}

	onMount(fetchGroups);
</script>

<h1 class="text-2xl font-semibold mb-4 text-green-600">ClassGroups - UI Test</h1>


<button class="mb-4 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700" on:click={() => {
	showForm = true;
	editMode = false;
	editingId = null;
	newGroup = {
		subject_id: '',
		group_number: '',
		enrollment_count: '',
		location_id: ''
	};
}}>
	+ Add New Group
</button>

{#if showForm}
	<div class="bg-gray-100 p-4 rounded mb-6 shadow">
		<h2 class="text-lg font-semibold mb-2">{editMode ? 'Edit Group' : 'New Group'}</h2>
		<div class="grid grid-cols-2 gap-4">
			<input type="number" class="p-2 border rounded" placeholder="Subject ID" bind:value={newGroup.subject_id} />
			<input type="number" class="p-2 border rounded" placeholder="Group Number" bind:value={newGroup.group_number} />
			<input type="number" class="p-2 border rounded" placeholder="Enrollment Count" bind:value={newGroup.enrollment_count} />
			<input type="number" class="p-2 border rounded" placeholder="Location ID" bind:value={newGroup.location_id} />
		</div>
		<div class="mt-4 flex gap-2">
			<button class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700" on:click={addGroup}>
				{editMode ? 'Update' : 'Save'}
			</button>
			<button class="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500" on:click={resetForm}>Cancel</button>
		</div>
	</div>
{/if}

<table class="min-w-full border border-gray-300 text-sm">
	<thead class="bg-gray-100">
		<tr>
			<th class="border px-4 py-2">ID</th>
			<th class="border px-4 py-2">Subject ID</th>
			<th class="border px-4 py-2">Group Number</th>
			<th class="border px-4 py-2">Enrollment</th>
			<th class="border px-4 py-2">Location</th>
			<th class="border px-4 py-2">Actions</th>
		</tr>
	</thead>
	<tbody>
		{#each classgroups as group}
			<tr class="hover:bg-gray-50">
				<td class="border px-4 py-2">{group.class_group_id}</td>
				<td class="border px-4 py-2">{group.subject_id}</td>
				<td class="border px-4 py-2">{group.group_number}</td>
				<td class="border px-4 py-2">{group.enrollment_count}</td>
				<td class="border px-4 py-2">{group.location_id}</td>
				<td class="border px-4 py-2 space-x-2">
					<button class="text-blue-600 hover:underline" on:click={() => startEdit(group)}>Edit</button>
					<button class="text-red-600 hover:underline" on:click={() => deleteGroup(group.class_group_id)}>Delete</button>
				</td>
			</tr>
		{/each}
	</tbody>
</table>
