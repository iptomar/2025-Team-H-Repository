<!-- src/App.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { Calendar, type EventApi } from '@fullcalendar/core';
  import timeGridPlugin from '@fullcalendar/timegrid';
  import interactionPlugin from '@fullcalendar/interaction';

  let calendarEl: HTMLElement;
  let calendar: Calendar;

  let showModal = false;
  let eventStart = '';
  let eventEnd = '';
  let eventColor = '#4f46e5';
  let selectedEvent: EventApi | null = null;
  let selectedProfessor = '';
  let selectedSala = '';
  let selectedCadeira = '';
  let eventId = 3;

  const professores = ['Prof. João', 'Prof. Maria', 'Prof. Pedro', 'Prof. Ana'];
  const salas = ['Sala O101', 'Sala Q202', 'Sala B303', 'Sala O404'];
  const cadeiras = ['Gestão Projetos', 'POO', 'EDA', 'Análise Matemática I'];

  const initialEvents = [
    { 
      id: '1',
      title: 'Análise Matemática I - Prof. Luis - Sala B303', 
      start: '2025-04-07T09:00:00',
      end: '2025-04-07T10:00:00', 
      backgroundColor: '#4f46e5',
      extendedProps: { professor: 'Prof. Luis', sala: 'Sala B303', cadeira: 'Análise Matemática I' }
    },
    { 
      id: '2',
      title: 'EDA - Prof. Maria - Sala Q202', 
      start: '2025-04-08T14:00:00',
      end: '2025-04-08T15:30:00', 
      backgroundColor: '#10b981',
      extendedProps: { professor: 'Prof. Maria', sala: 'Sala Q202', cadeira: 'EDA' }
    }
  ];

  function formatTime(dateStr: string): string {
    const date = new Date(dateStr);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  }

  onMount(() => {
    calendar = new Calendar(calendarEl, {
      plugins: [timeGridPlugin, interactionPlugin],
      initialView: 'timeGridWeek',
      headerToolbar: {
        left: '',
        center: '',
        right: ''
      },
      initialDate: '2025-04-07',
      weekends: true,
      allDaySlot: false,
      slotMinTime: '08:00:00',
      slotMaxTime: '23:30:00',
      slotDuration: '00:30:00',
      slotLabelFormat: {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      },
      events: initialEvents,
      editable: true,
      eventResizableFromStart: true,
      eventDrop: (info) => updateEvent(info.event),
      eventResize: (info) => updateEvent(info.event),
      dateClick: (info) => {
        eventStart = info.dateStr;
        const end = new Date(info.date);
        end.setHours(end.getHours() + 1);
        eventEnd = end.toISOString();
        eventColor = '#4f46e5';
        selectedEvent = null;
        selectedProfessor = '';
        selectedSala = '';
        selectedCadeira = '';
        showModal = true;
      },
      eventClick: (info) => {
        selectedEvent = info.event;
        eventStart = selectedEvent.start!.toISOString();
        eventEnd = selectedEvent.end?.toISOString() || '';
        eventColor = selectedEvent.backgroundColor;
        selectedProfessor = selectedEvent.extendedProps.professor || '';
        selectedSala = selectedEvent.extendedProps.sala || '';
        selectedCadeira = selectedEvent.extendedProps.cadeira || '';
        showModal = true;
      }
    });
    calendar.render();
  });

  function updateEvent(event: EventApi) {
    event.setExtendedProp('professor', event.extendedProps.professor);
    event.setExtendedProp('sala', event.extendedProps.sala);
    event.setExtendedProp('cadeira', event.extendedProps.cadeira);
  }

  function saveEvent() {
    if (selectedProfessor && selectedSala && selectedCadeira) {
      const title = `${selectedCadeira} - ${selectedProfessor} - ${selectedSala}`;
      if (selectedEvent) {
        selectedEvent.setProp('title', title);
        selectedEvent.setStart(eventStart);
        selectedEvent.setEnd(eventEnd);
        selectedEvent.setProp('backgroundColor', eventColor);
        selectedEvent.setExtendedProp('professor', selectedProfessor);
        selectedEvent.setExtendedProp('sala', selectedSala);
        selectedEvent.setExtendedProp('cadeira', selectedCadeira);
      } else {
        calendar.addEvent({
          id: String(eventId++),
          title,
          start: eventStart,
          end: eventEnd,
          backgroundColor: eventColor,
          extendedProps: {
            professor: selectedProfessor,
            sala: selectedSala,
            cadeira: selectedCadeira
          }
        });
      }
      closeModal();
    }
  }

  function deleteEvent() {
    if (selectedEvent) {
      selectedEvent.remove();
    }
    closeModal();
  }

  function closeModal() {
    showModal = false;
    eventStart = '';
    eventEnd = '';
    eventColor = '#4f46e5';
    selectedEvent = null;
    selectedProfessor = '';
    selectedSala = '';
    selectedCadeira = '';
  }
</script>

<main class="min-h-screen bg-gray-50 p-8">
  <div class="mx-auto">
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div bind:this={calendarEl}></div>
    </div>
  </div>

  <!-- Modal -->
  {#if showModal}
    <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg shadow-xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-900">
            {selectedEvent ? 'Editar Evento' : 'Novo Evento'}
          </h2>
          <button on:click={closeModal} class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="text-sm text-gray-600 mb-6">
          <span>{new Date(eventStart).toLocaleDateString('pt-PT')} {formatTime(eventStart)}</span>
          <span> – </span>
          <span>{new Date(eventEnd).toLocaleDateString('pt-PT')} {formatTime(eventEnd)}</span>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Professor</label>
            <select bind:value={selectedProfessor} 
                    class="w-full p-2 border border-gray-200 rounded-md focus:ring-indigo-500 focus:border-indigo-500">
              <option value="">Selecione um professor</option>
              {#each professores as prof}
                <option value={prof}>{prof}</option>
              {/each}
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Sala</label>
            <select bind:value={selectedSala} 
                    class="w-full p-2 border border-gray-200 rounded-md focus:ring-indigo-500 focus:border-indigo-500">
              <option value="">Selecione uma sala</option>
              {#each salas as sala}
                <option value={sala}>{sala}</option>
              {/each}
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Cadeira</label>
            <select bind:value={selectedCadeira} 
                    class="w-full p-2 border border-gray-200 rounded-md focus:ring-indigo-500 focus:border-indigo-500">
              <option value="">Selecione uma cadeira</option>
              {#each cadeiras as cadeira}
                <option value={cadeira}>{cadeira}</option>
              {/each}
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Cor do Evento</label>
            <input type="color" bind:value={eventColor} 
                   class="w-full h-10 rounded-md border border-gray-200 cursor-pointer" />
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          {#if selectedEvent}
            <button
              on:click={deleteEvent}
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              Excluir
            </button>
          {/if}
          <button
            on:click={closeModal}
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
          >
            Cancelar
          </button>
          <button
            on:click={saveEvent}
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>
  {/if}
</main>

<style>
  :global(.fc) {
    font-family: 'Inter', sans-serif;
  }
  :global(.fc .fc-toolbar) {
    padding: 1rem;
    background-color: #fff;
    border-bottom: 1px solid #e5e7eb;
  }
  :global(.fc .fc-toolbar-title) {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
  }
  :global(.fc .fc-button) {
    background-color: #4f46e5;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    text-transform: capitalize;
  }
  :global(.fc .fc-button:hover) {
    background-color: #4338ca;
  }
  :global(.fc .fc-col-header-cell) {
    background-color: #f9fafb;
    color: #374151;
    font-weight: 500;
    padding: 0.75rem;
    border-bottom: 1px solid #e5e7eb;
  }
  :global(.fc .fc-timegrid-slot) {
    height: 2.5rem;
    border-color: #f3f4f6;
  }
  :global(.fc .fc-event) {
    border: none;
    border-radius: 0.375rem;
    padding: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
  }
  :global(.fc .fc-event:hover) {
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }
  :global(.fc .fc-timegrid-col) {
    background: #fff;
  }
</style>