<script lang="ts">
    import { rooms, fetchRooms, createRoom, updateRoom, deleteRoom } from '../stores/roomStore';
    import type { Room } from '../types/room';
    import { onMount } from 'svelte';

    // Estado para o formulário de criação
    let newRoom: Omit<Room, 'room_id'> = {
        name: '',
        capacity: 0,
        location_id: 0,
        owner_course_id: null,
    };

    // Estado para o modal de edição
    let showEditModal = false;
    let editRoom: Room | null = null;

    // Carrega as salas ao montar o componente
    onMount(() => {
        fetchRooms();
    });

    // Função para abrir o modal de edição
    function openEditModal(room: Room) {
        editRoom = { ...room };
        showEditModal = true;
    }

    // Função para salvar alterações no modal
    async function saveEdit() {
        if (editRoom) {
            await updateRoom(editRoom.room_id, {
                name: editRoom.name,
                capacity: editRoom.capacity,
                location_id: editRoom.location_id,
                owner_course_id: editRoom.owner_course_id,
            });
        }
        closeEditModal();
    }

    // Função para fechar o modal de edição
    function closeEditModal() {
        showEditModal = false;
        editRoom = null;
    }

    // Função para criar uma nova sala
    async function handleCreateRoom() {
        if (newRoom.name && newRoom.capacity > 0 && newRoom.location_id > 0) {
            await createRoom(newRoom);
            // Reseta o formulário
            newRoom = {
                name: '',
                capacity: 0,
                location_id: 0,
                owner_course_id: null,
            };
        }
    }
</script>

<main class="bg-gray-100 min-h-screen p-6">
    <div class="max-w-4xl mx-auto">
        <!-- Formulário para criar sala -->
        <div class="bg-white p-6 rounded-lg shadow-md mb-6">
            <h2 class="text-2xl font-bold mb-4">Criar Nova Sala</h2>
            <form on:submit|preventDefault={handleCreateRoom} class="space-y-4">
                <div>
                    <label for="name" class="block text-sm font-medium text-gray-700">Nome</label>
                    <input
                        id="name"
                        type="text"
                        bind:value={newRoom.name}
                        placeholder="Ex.: Sala 101"
                        class="w-full p-2 border rounded"
                        required
                    />
                </div>
                <div>
                    <label for="capacity" class="block text-sm font-medium text-gray-700">Capacidade</label>
                    <input
                        id="capacity"
                        type="number"
                        bind:value={newRoom.capacity}
                        placeholder="Ex.: 30"
                        min="1"
                        class="w-full p-2 border rounded"
                        required
                    />
                </div>
                <div>
                    <label for="location_id" class="block text-sm font-medium text-gray-700">ID da Localização</label>
                    <input
                        id="location_id"
                        type="number"
                        bind:value={newRoom.location_id}
                        placeholder="Ex.: 1"
                        min="1"
                        class="w-full p-2 border rounded"
                        required
                    />
                </div>
                <div>
                    <label for="owner_course_id" class="block text-sm font-medium text-gray-700">ID do Curso (Opcional)</label>
                    <input
                        id="owner_course_id"
                        type="number"
                        bind:value={newRoom.owner_course_id}
                        placeholder="Ex.: 1 (deixe vazio se não aplicável)"
                        class="w-full p-2 border rounded"
                    />
                </div>
                <button
                    type="submit"
                    class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                    Criar Sala
                </button>
            </form>
        </div>

        <!-- Tabela de salas -->
        <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-2xl font-bold mb-4">Lista de Salas</h2>
            {#if $rooms.length === 0}
                <p class="text-gray-500">Nenhuma sala encontrada.</p>
            {:else}
                <div class="overflow-x-auto">
                    <table class="min-w-full table-auto text-center">
                        <thead>
                            <tr class="bg-blue-500 text-white">
                                <th class="px-4 py-2">ID</th>
                                <th class="px-4 py-2">Nome</th>
                                <th class="px-4 py-2">Capacidade</th>
                                <th class="px-4 py-2">Localização</th>
                                <th class="px-4 py-2">Curso</th>
                                <th class="px-4 py-2">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each $rooms as room}
                                <tr class="border-b">
                                    <td class="px-4 py-2">{room.room_id}</td>
                                    <td class="px-4 py-2">{room.name}</td>
                                    <td class="px-4 py-2">{room.capacity}</td>
                                    <td class="px-4 py-2">{room.location_id}</td>
                                    <td class="px-4 py-2">{room.owner_course_id || 'Nenhum'}</td>
                                    <td class="px-4 py-2">
                                        <button
                                            on:click={() => openEditModal(room)}
                                            class="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 mr-2"
                                        >
                                            Editar
                                        </button>
                                        <button
                                            on:click={() => deleteRoom(room.room_id)}
                                            class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                                        >
                                            Excluir
                                        </button>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>
    </div>

    <!-- Modal de edição -->
    {#if showEditModal && editRoom}
        <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded-lg shadow-lg w-96">
                <h2 class="text-lg font-bold mb-4">Editar Sala {editRoom.name}</h2>
                <div class="space-y-4">
                    <div>
                        <label for="edit_name" class="block text-sm font-medium text-gray-700">Nome</label>
                        <input
                            id="edit_name"
                            type="text"
                            bind:value={editRoom.name}
                            class="w-full p-2 border rounded"
                            required
                        />
                    </div>
                    <div>
                        <label for="edit_capacity" class="block text-sm font-medium text-gray-700">Capacidade</label>
                        <input
                            id="edit_capacity"
                            type="number"
                            bind:value={editRoom.capacity}
                            min="1"
                            class="w-full p-2 border rounded"
                            required
                        />
                    </div>
                    <div>
                        <label for="edit_location_id" class="block text-sm font-medium text-gray-700">ID da Localização</label>
                        <input
                            id="edit_location_id"
                            type="number"
                            bind:value={editRoom.location_id}
                            min="1"
                            class="w-full p-2 border rounded"
                            required
                        />
                    </div>
                    <div>
                        <label for="edit_owner_course_id" class="block text-sm font-medium text-gray-700">ID do Curso (Opcional)</label>
                        <input
                            id="edit_owner_course_id"
                            type="number"
                            bind:value={editRoom.owner_course_id}
                            class="w-full p-2 border rounded"
                        />
                    </div>
                </div>
                <div class="flex justify-end gap-2 mt-4">
                    <button
                        on:click={closeEditModal}
                        class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                    >
                        Cancelar
                    </button>
                    <button
                        on:click={saveEdit}
                        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                        Salvar
                    </button>
                </div>
            </div>
        </div>
    {/if}
</main>