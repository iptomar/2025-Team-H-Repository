<!-- src/App.svelte -->
<script lang="ts">
  type EventData = Record<string, string>;

  const horas: string[] = [
    '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30',
    '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
    '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
    '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00'
  ];
  
  const dias: string[] = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo'];

  let agenda: EventData = {};
  let showModal = false;
  let selectedTime = '';
  let selectedDay = '';
  let eventText = '';

  // Open modal with selected time and day
  function openModal(hora: string, dia: string) {
    selectedTime = hora;
    selectedDay = dia;
    eventText = agenda[`${hora}-${dia}`] || ''; // Pre-fill with existing event, if any
    showModal = true;
  }

  // Save event and close modal
  function saveEvent() {
    if (eventText.trim()) {
      agenda[`${selectedTime}-${selectedDay}`] = eventText.trim();
      agenda = agenda; // Trigger reactivity
    }
    closeModal();
  }

  // Close modal without saving
  function closeModal() {
    showModal = false;
    eventText = '';
  }
</script>

<main class="bg-gray-100 min-h-screen p-6">
  <div class="overflow-x-auto bg-white shadow-md rounded-lg">
    <table class="min-w-full table-auto text-center">
      <thead>
        <tr class="bg-blue-500 text-white">
          <th class="px-2 border-b">Hora</th>
          {#each dias as dia}
            <th class="px-2 border-b">{dia.charAt(0).toUpperCase() + dia.slice(1)}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each horas as hora}
          <tr class="border-b">
            <td class="px-2 font-bold">{hora}</td>
            {#each dias as dia}
              <td 
                class="px-2 cursor-pointer hover:bg-gray-200 transition-colors"
                on:click={() => openModal(hora, dia)}
              >
                {agenda[`${hora}-${dia}`] || ""}
              </td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  <!-- Modal -->
  {#if showModal}
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 class="text-lg font-bold mb-4">
          Evento em {selectedTime} - {selectedDay.charAt(0).toUpperCase() + selectedDay.slice(1)}
        </h2>
        <input 
          type="text" 
          bind:value={eventText} 
          placeholder="Digite o evento" 
          class="w-full p-2 border rounded mb-4"
          on:keydown={(e) => e.key === 'Enter' && saveEvent()}
        />
        <div class="flex justify-end gap-2">
          <button 
            on:click={closeModal} 
            class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
          >
            Cancelar
          </button>
          <button 
            on:click={saveEvent} 
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>
  {/if}
</main>

<style>
  table { width: 100%; border-collapse: collapse; }
  th, td { border: 1px solid #e2e8f0; padding: 10px; text-align: center; }
  th { background-color: #2b6cb0; color: white; }
  td { min-width: 120px; height: 40px; }
  .cursor-pointer { cursor: pointer; }
</style>