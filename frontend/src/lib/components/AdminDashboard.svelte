<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table';
	import { cn } from '$lib/utils.js';
</script>

<div class="p-4">
	<div class="mt-4 grid gap-2">
        <div class="p-4 bg-gray-100 flex:block justify-center">
            <h1 class="text-2xl font-bold pb-4">Users Table</h1>
            <Table.Root class="w-full max-w-3xl bg-white shadow-md rounded-xl overflow-hidden border-">
              <Table.Header class="bg-gray-50">
            <Table.Row>
              <Table.Head class="w-[100px] px-4 py-3 text-left text-sm font-semibold text-gray-700">User ID</Table.Head>
              <Table.Head class="px-4 py-3 text-sm font-semibold text-gray-700">Status</Table.Head>
              <Table.Head class="px-4 py-3 text-sm font-semibold text-gray-700">Method</Table.Head>
              <Table.Head class="px-4 py-3 text-right text-sm font-semibold text-gray-700">Actions</Table.Head>
            </Table.Row>
              </Table.Header>
              <Table.Body>
            <Table.Row>
              <Table.Cell class="px-4 py-2 font-medium text-gray-800">1</Table.Cell>
              <Table.Cell class="px-4 py-2 text-gray-600">Active</Table.Cell>
              <Table.Cell class="px-4 py-2 text-gray-600">Email</Table.Cell>
              <Table.Cell class="px-4 py-2 text-right text-blue-600 cursor-pointer hover:underline"><Button variant="default">Add User</Button>
                <Button variant="default">Edit User</Button>
                <Button variant="destructive">Delete User</Button></Table.Cell>
            </Table.Row>
              </Table.Body>
            </Table.Root>
        </div>
	</div>
</div>
