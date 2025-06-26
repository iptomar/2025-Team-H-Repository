<script lang="ts">
  import { onMount } from 'svelte';
  import { Calendar, type EventApi } from '@fullcalendar/core';
  import timeGridPlugin from '@fullcalendar/timegrid';
  import interactionPlugin, { Draggable } from '@fullcalendar/interaction';

  // --- Variáveis de Estado ---
  let calendarEl: HTMLElement;
  let calendar: Calendar;
  let showModal = false;
  let eventStart = '';
  let eventEnd = '';
  let eventColor = '#4f46e5';
  let selectedEvent: EventApi | null = null;
  let currentConflictMessage: string | null = null; // Para exibir a mensagem de erro no modal

  // Variáveis para o Toast (Notificações)
  let showToast = false;
  let toastMessage = '';
  let toastType: 'success' | 'error' | 'warning' = 'success'; // Tipo de mensagem para o estilo

  // Dados mock para simular o backend
  interface Professor {
    id: string;
    nome: string;
    indisponibilidades: { start: string; end: string; title: string; display?: 'background' }[];
  }

  interface Sala {
    id: string;
    nome: string;
    capacidade: number;
    campus: string; // Tomar, Abrantes
    especial?: boolean; // Se for uma sala especial (ex: laboratório)
    cursoResponsavelId?: string; // Para salas especiais
  }

  interface Cadeira {
    id: string;
    nome: string;
    tipo: 'T' | 'P' | 'TP';
    cursoId: string;
  }

  interface Grupo {
    id: string;
    nome: string;
    numAlunos: number;
    cadeiraId: string;
    cursoId: string;
    escolaId: string; // ESTT, ESGT, ESTA
  }

  interface AulaNaoAtribuida {
    id: string;
    cadeiraId: string;
    grupoId: string;
    tipo: 'T' | 'P' | 'TP';
    professorPreferencialId?: string; // Professor que idealmente daria a aula
    duracaoHoras: number; // Ex: 1.5 para 1h30
  }

  // --- DADOS MOCK ---
  const mockProfessores: Professor[] = [
    { id: 'p1', nome: 'Prof. João Silva', indisponibilidades: [
      { start: '2025-04-07T11:00:00', end: '2025-04-07T12:00:00', title: 'Indisponível', display: 'background' },
      { start: '2025-04-09T10:00:00', end: '2025-04-09T12:00:00', title: 'Indisponível', display: 'background' }
    ]},
    { id: 'p2', nome: 'Prof. Maria Costa', indisponibilidades: [
      { start: '2025-04-08T09:30:00', end: '2025-04-08T10:30:00', title: 'Indisponível', display: 'background' }
    ]},
    { id: 'p3', nome: 'Prof. Pedro Santos', indisponibilidades: [] },
    { id: 'p4', nome: 'Prof. Ana Pereira', indisponibilidades: [] }
  ];

  const mockSalas: Sala[] = [
    { id: 's1', nome: 'Sala O101', capacidade: 30, campus: 'Tomar' },
    { id: 's2', nome: 'Sala Q202', capacidade: 25, campus: 'Tomar' },
    { id: 's3', nome: 'Laboratório B303', capacidade: 20, campus: 'Tomar', especial: true, cursoResponsavelId: 'c1' }, // Eng. Informática
    { id: 's4', nome: 'Sala O404', capacidade: 40, campus: 'Abrantes' },
    { id: 's5', nome: 'Sala A10', capacidade: 50, campus: 'Tomar' },
  ];

  const mockCadeiras: Cadeira[] = [
    { id: 'cad1', nome: 'Gestão Projetos', tipo: 'T', cursoId: 'c1' }, // Eng. Informática
    { id: 'cad2', nome: 'POO', tipo: 'TP', cursoId: 'c1' },
    { id: 'cad3', nome: 'EDA', tipo: 'P', cursoId: 'c1' },
    { id: 'cad4', nome: 'Análise Matemática I', tipo: 'T', cursoId: 'c2' }, // Gestão
    { id: 'cad5', nome: 'Introdução à Economia', tipo: 'T', cursoId: 'c2' },
  ];

  const mockGrupos: Grupo[] = [
    { id: 'g1_cad1', nome: 'G1', numAlunos: 25, cadeiraId: 'cad1', cursoId: 'c1', escolaId: 'e1' },
    { id: 'g2_cad1', nome: 'G2', numAlunos: 20, cadeiraId: 'cad1', cursoId: 'c1', escolaId: 'e1' },
    { id: 'g1_cad2', nome: 'G1', numAlunos: 25, cadeiraId: 'cad2', cursoId: 'c1', escolaId: 'e1' },
    { id: 'g1_cad3', nome: 'G1', numAlunos: 20, cadeiraId: 'cad3', cursoId: 'c1', escolaId: 'e1' },
    { id: 'g1_cad4', nome: 'G1', numAlunos: 35, cadeiraId: 'cad4', cursoId: 'c2', escolaId: 'e2' },
  ];

  const mockCursos = [
    { id: 'c1', nome: 'Engenharia Informática', escolaId: 'e1' },
    { id: 'c2', nome: 'Gestão', escolaId: 'e2' },
  ];

  const mockEscolas = [
    { id: 'e1', nome: 'ESTT', campus: 'Tomar' },
    { id: 'e2', nome: 'ESGT', campus: 'Tomar' },
    { id: 'e3', nome: 'ESTA', campus: 'Abrantes' },
  ];


  let aulasNaoAtribuidas: AulaNaoAtribuida[] = [
    { id: 'aula1', cadeiraId: 'cad1', grupoId: 'g1_cad1', tipo: 'T', professorPreferencialId: 'p1', duracaoHoras: 1.5 },
    { id: 'aula2', cadeiraId: 'cad2', grupoId: 'g1_cad2', tipo: 'TP', professorPreferencialId: 'p2', duracaoHoras: 2 },
    { id: 'aula3', cadeiraId: 'cad3', grupoId: 'g1_cad3', tipo: 'P', professorPreferencialId: 'p3', duracaoHoras: 2.5 },
    { id: 'aula4', cadeiraId: 'cad4', grupoId: 'g1_cad4', tipo: 'T', professorPreferencialId: 'p4', duracaoHoras: 1 },
    { id: 'aula5', cadeiraId: 'cad1', grupoId: 'g2_cad1', tipo: 'T', professorPreferencialId: 'p1', duracaoHoras: 1.5 },
  ];

  interface CalendarEventData {
    id: string;
    title: string;
    start: string;
    end: string;
    backgroundColor: string;
    display?: string; // 'auto', 'background', 'block', 'list-item'
    extendedProps: {
      professorId: string;
      salaId: string;
      cadeiraId: string;
      groupId: string;
      aulaId?: string; // para identificar se veio de aulasNaoAtribuidas
      isIndisponibilidade?: boolean; // Para indisponibilidades de professor
      isTempDragEvent?: boolean; // Marcador para eventos temporários de drag
    };
  }

  const initialEvents: CalendarEventData[] = [
    {
      id: '1',
      title: 'Análise Matemática I (G1) - Prof. João Silva - Sala O101',
      start: '2025-04-07T09:00:00',
      end: '2025-04-07T10:00:00',
      backgroundColor: '#4f46e5',
      extendedProps: { professorId: 'p1', salaId: 's1', cadeiraId: 'cad4', groupId: 'g1_cad4' }
    },
    {
      id: '2',
      title: 'EDA (G1) - Prof. Maria Costa - Laboratório B303',
      start: '2025-04-08T14:00:00',
      end: '2025-04-08T15:30:00',
      backgroundColor: '#10b981',
      extendedProps: { professorId: 'p2', salaId: 's3', cadeiraId: 'cad3', groupId: 'g1_cad3' }
    }
  ];

  let eventIdCounter = 100; // Começa de um ID mais alto para não colidir com initialEvents

  // Dados para o modal de agendamento
  let selectedProfessorId = '';
  let selectedSalaId = '';
  let selectedCadeiraId = ''; // Irá vir do arrastar ou clique
  let selectedGrupoId = ''; // Irá vir do arrastar ou clique
  let eventDurationHours = 1; // Default
  let currentEventCampus = ''; // Determinado pelo grupo ou arrasto

  // Variáveis para auxiliar na drag-and-drop
  let draggedAula: AulaNaoAtribuida | null = null;
  let tempEventId: string | null = null; // Para o evento temporário ao arrastar


  // --- Funções Auxiliares ---
  function getCadeira(id: string) { return mockCadeiras.find(c => c.id === id); }
  function getGrupo(id: string) { return mockGrupos.find(g => g.id === id); }
  function getProfessor(id: string) { return mockProfessores.find(p => p.id === id); }
  function getSala(id: string) { return mockSalas.find(s => s.id === id); }
  function getEscola(id: string) { return mockEscolas.find(e => e.id === id); }
  function getCurso(id: string) { return mockCursos.find(c => c.id === id); }

  function formatTime(dateStr: string | Date): string {
    const date = new Date(dateStr);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  }

  function formatDate(dateStr: string | Date): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-PT');
  }

  // --- Funções de Notificação (Toast) ---
  function showNotification(message: string, type: 'success' | 'error' | 'warning' = 'success') {
    toastMessage = message;
    toastType = type;
    showToast = true;
    setTimeout(() => {
      showToast = false;
    }, 3000); // Esconde a notificação após 3 segundos
  }

  // --- Funções de gerenciamento de indisponibilidades no calendário ---
  function clearProfessorIndisponibilities() {
    if (!calendar) return;
    calendar.getEvents().filter(event => event.extendedProps.isIndisponibilidade).forEach(event => event.remove());
  }

  function loadProfessorIndisponibilities(professorId: string) {
    if (!calendar) return;
    clearProfessorIndisponibilities(); // Limpa as anteriores
    const professor = getProfessor(professorId);
    if (professor) {
      professor.indisponibilidades.forEach((indisp, index) => {
        calendar.addEvent({
          id: `indisp-${professor.id}-${index}`, // ID único para cada indisponibilidade
          start: indisp.start,
          end: indisp.end,
          title: indisp.title,
          backgroundColor: '#a3a3a3', // Cor cinza para indisponibilidade
          borderColor: '#808080',
          display: 'background',
          extendedProps: {
            professorId: professor.id,
            salaId: '',
            cadeiraId: '',
            groupId: '',
            isIndisponibilidade: true // Identificador para indisponibilidade
          }
        });
      });
    }
  }

  // --- Lógica de Conflitos ---
  function checkConflict(newEvent: { start: Date, end: Date, professorId?: string, salaId?: string, groupId?: string }, eventBeingCheckedId?: string): string | null {
    const newEventStart = newEvent.start.getTime();
    const newEventEnd = newEvent.end.getTime();

    const roundToHalfHour = (ms: number) => Math.round(ms / (30 * 60 * 1000)) * (30 * 60 * 1000);
    const newEventStartRounded = roundToHalfHour(newEventStart);
    const newEventEndRounded = roundToHalfHour(newEventEnd);

    const allEvents = calendar.getEvents();
    for (const existingEvent of allEvents) {
      // Ignorar o próprio evento ao editar/mover ou eventos temporários de drag-and-drop não salvos
      if (existingEvent.id === eventBeingCheckedId) continue;
      // if (existingEvent.extendedProps.isTempDragEvent && existingEvent.id !== tempEventId) continue; // Pode causar problemas se houver múltiplos drags

      const existingEventStart = existingEvent.start!.getTime();
      const existingEventEnd = existingEvent.end!.getTime();

      const existingEventStartRounded = roundToHalfHour(existingEventStart);
      const existingEventEndRounded = roundToHalfHour(existingEventEnd);

      // Verificar sobreposição de tempo
      if (newEventStartRounded < existingEventEndRounded && newEventEndRounded > existingEventStartRounded) {
        const existingProfId = existingEvent.extendedProps.professorId;
        const existingSalaId = existingEvent.extendedProps.salaId;
        const existingGroupId = existingEvent.extendedProps.groupId;

        // Conflito de Professor
        if (newEvent.professorId && existingProfId === newEvent.professorId) {
          // Conflito com indisponibilidade (agora identificada por isIndisponibilidade)
          if (existingEvent.extendedProps.isIndisponibilidade) {
            return `O professor ${getProfessor(newEvent.professorId)?.nome} está indisponível neste horário.`;
          }

          // Conflito com outra aula do mesmo professor
          if (!existingEvent.extendedProps.isIndisponibilidade) {
            const existingEventSala = getSala(existingSalaId);
            const newEventSala = getSala(newEvent.salaId || '');

            // Conflito de tempo de viagem entre campi
            if (existingEventSala && newEventSala && existingEventSala.campus !== newEventSala.campus) {
                const gapAfterExisting = Math.abs(newEventStartRounded - existingEventEndRounded) / (1000 * 60 * 60);
                const gapBeforeExisting = Math.abs(existingEventStartRounded - newEventEndRounded) / (1000 * 60 * 60);

                if ( (newEventStartRounded < existingEventEndRounded && gapAfterExisting < 1) ||
                     (newEventEndRounded > existingEventStartRounded && gapBeforeExisting < 1) ) {
                    return `Conflito de tempo de viagem para ${getProfessor(newEvent.professorId)?.nome} entre campi. Necessário 1h de intervalo.`;
                }
            } else {
                return `Conflito de horário para o professor ${getProfessor(newEvent.professorId)?.nome}.`;
            }
          }
        }

        // Conflito de Sala (apenas para eventos não-background)
        if (newEvent.salaId && existingSalaId === newEvent.salaId && !existingEvent.extendedProps.isIndisponibilidade) {
          return `Conflito de sala: ${getSala(newEvent.salaId)?.nome} já ocupada.`;
        }

        // Conflito de Grupo de Turma (apenas para eventos não-background)
        if (newEvent.groupId && existingGroupId === newEvent.groupId && !existingEvent.extendedProps.isIndisponibilidade) {
          return `Conflito de horário para o grupo ${getGrupo(newEvent.groupId)?.nome}.`;
        }
      }
    }

    // Alertas não-bloqueadores (ex: horas diárias excedidas) - pode ser processado separadamente
    return null;
  }

  // --- FullCalendar Setup ---
  onMount(() => {
    const initialCalendarEvents = [...initialEvents];

    calendar = new Calendar(calendarEl, {
      plugins: [timeGridPlugin, interactionPlugin],
      initialView: 'timeGridWeek',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'timeGridWeek,timeGridDay'
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
      events: initialCalendarEvents, // Apenas os eventos iniciais
      editable: true,
      droppable: true,
      eventResizableFromStart: true,
      selectOverlap: false, // Não permitir selecionar sobreposições

      // Determina se um evento pode ser sobreposto visualmente por outro
      eventOverlap: function(stillEvent, movingEvent) {
          // Indisponibilidades (background events) sempre permitem ser sobrepostas visualmente (para o ghost event aparecer)
          if (stillEvent.extendedProps.isIndisponibilidade) {
            return true;
          }
          // Indisponibilidades NÃO podem ser movidas para sobrepor eventos normais
          if (movingEvent?.extendedProps.isIndisponibilidade) {
            return false;
          }

          // Para eventos normais, impedir sobreposição visual se houver conflito de recurso
          const movingProfId = movingEvent?.extendedProps.professorId;
          const movingSalaId = movingEvent?.extendedProps.salaId;
          const movingGroupId = movingEvent?.extendedProps.groupId;

          const stillProfId = stillEvent.extendedProps.professorId;
          const stillSalaId = stillEvent.extendedProps.salaId;
          const stillGroupId = stillEvent.extendedProps.groupId;

          if (movingProfId && movingProfId === stillProfId) return false;
          if (movingSalaId && movingSalaId === stillSalaId) return false;
          if (movingGroupId && movingGroupId === stillGroupId) return false;

          return true; // Se não houver conflito de recurso, permite sobreposição visual (mas eventAllow/eventReceive farão a checagem completa)
      },

      // Chamado quando um evento externo é arrastado para o calendário
      eventReceive: (info) => {
        const professorId = info.event.extendedProps.professorId;
        loadProfessorIndisponibilities(professorId); // Carrega as indisponibilidades do professor

        const testEvent = {
            start: info.event.start!,
            end: info.event.end!,
            professorId: professorId,
            salaId: '', // A sala será definida no modal
            groupId: info.event.extendedProps.groupId
        };
        const conflict = checkConflict(testEvent, info.event.id); // Passa o ID do evento temporário para ignorar ele mesmo

        if (conflict) {
          info.revert(); // Reverte o drop do FullCalendar
          showNotification(conflict, 'error');
          // NADA DE REMOVER DA SIDEBAR AQUI. A aula permanece na sidebar.
          clearProfessorIndisponibilities(); // Limpa as indisponibilidades se o drop falhou
          draggedAula = null; // Reseta o estado de arrasto
        } else {
            // Se não houver conflito inicial, abre o modal
            const start = info.event.start!;
            const end = new Date(start.getTime() + (draggedAula?.duracaoHoras || 1) * 60 * 60 * 1000); // Usa a duração da aula arrastada
            const grupo = getGrupo(info.event.extendedProps.groupId);
            const cadeira = getCadeira(info.event.extendedProps.cadeiraId);
            const professor = getProfessor(info.event.extendedProps.professorId || '');
            const escolaDoGrupo = getEscola(grupo?.escolaId || '');
            currentEventCampus = escolaDoGrupo?.campus || '';

            selectedProfessorId = professor?.id || '';
            selectedCadeiraId = cadeira?.id || '';
            selectedGrupoId = grupo?.id || '';
            eventDurationHours = (end.getTime() - start.getTime()) / (1000 * 60 * 60);
            eventStart = start.toISOString();
            eventEnd = end.toISOString();
            selectedEvent = info.event; // O evento já foi adicionado temporariamente pelo FullCalendar
            tempEventId = info.event.id; // Guarda o ID do evento temporário para manipulação no modal
            currentConflictMessage = null;
            showModal = true;
            // A aula só é removida da sidebar se o agendamento for confirmado no modal
        }
      },

      // Chamado ANTES de um evento existente ser arrastado ou redimensionado
      eventAllow: (dropInfo, draggedEvent) => {
          if (!draggedEvent || draggedEvent.extendedProps.isIndisponibilidade) {
              showNotification('Não é possível mover ou redimensionar indisponibilidades diretamente.', 'warning');
              return false;
          }

          const professorId = draggedEvent.extendedProps.professorId;
          loadProfessorIndisponibilities(professorId); // Carrega as indisponibilidades do professor que está a ser movido

          const newStart = dropInfo.start;
          const newEnd = dropInfo.end;
          const salaId = draggedEvent.extendedProps.salaId;
          const groupId = draggedEvent.extendedProps.groupId;

          const conflict = checkConflict({
              start: newStart,
              end: newEnd,
              professorId: professorId,
              salaId: salaId,
              groupId: groupId
          }, draggedEvent.id);

          if (conflict) {
              showNotification(conflict, 'error');
              return false; // Não permite o drop/resize
          }
          return true; // Permite o drop/resize
      },

      // Chamado APÓS um drop bem-sucedido de evento existente
      eventDrop: (info) => {
        updateEvent(info.event);
        clearProfessorIndisponibilities(); // Limpa as indisponibilidades após o drop
        showNotification('Evento movido com sucesso!', 'success');
      },
      // Chamado APÓS um resize bem-sucedido de evento existente
      eventResize: (info) => {
        updateEvent(info.event);
        clearProfessorIndisponibilities(); // Limpa as indisponibilidades após o resize
        showNotification('Evento redimensionado com sucesso!', 'success');
      },

      // Clicar numa área vazia do calendário
      dateClick: (info) => {
        clearProfessorIndisponibilities(); // Limpa indisponibilidades ao clicar no calendário para novo evento
        eventStart = info.dateStr;
        const end = new Date(info.date);
        end.setHours(end.getHours() + eventDurationHours);
        eventEnd = end.toISOString();
        eventColor = '#4f46e5';
        selectedEvent = null;
        selectedProfessorId = '';
        selectedSalaId = '';
        selectedCadeiraId = '';
        selectedGrupoId = '';
        currentEventCampus = '';
        currentConflictMessage = null;
        showModal = true;
      },

      // Clicar num evento existente
      eventClick: (info) => {
        if (info.event.extendedProps.isIndisponibilidade) {
            showNotification('Não é possível editar indisponibilidades diretamente através de clique no horário.', 'warning');
            return;
        }
        selectedEvent = info.event;
        loadProfessorIndisponibilities(selectedEvent.extendedProps.professorId); // Carrega indisponibilidades do professor do evento
        eventStart = selectedEvent.start!.toISOString();
        eventEnd = selectedEvent.end?.toISOString() || '';
        eventColor = selectedEvent.backgroundColor || '#4f46e5';
        selectedProfessorId = selectedEvent.extendedProps.professorId || '';
        selectedSalaId = selectedEvent.extendedProps.salaId || '';
        selectedCadeiraId = selectedEvent.extendedProps.cadeiraId || '';
        selectedGrupoId = selectedEvent.extendedProps.groupId || '';
        eventDurationHours = (new Date(eventEnd).getTime() - new Date(eventStart).getTime()) / (1000 * 60 * 60);

        const salaDoEvento = getSala(selectedSalaId);
        currentEventCampus = salaDoEvento?.campus || '';
        currentConflictMessage = null;

        showModal = true;
      }
    });
    calendar.render();

    // Habilitar Draggable para a sidebar
    new Draggable(document.getElementById('external-events')!, {
      itemSelector: '.fc-event-draggable',
      eventData: function(eventEl) {
        const aulaId = eventEl.dataset.aulaId;
        draggedAula = aulasNaoAtribuidas.find(aula => aula.id === aulaId) || null;
        if (!draggedAula) return {};

        const cadeira = getCadeira(draggedAula.cadeiraId);
        const grupo = getGrupo(draggedAula.grupoId);
        const professor = getProfessor(draggedAula.professorPreferencialId || '');

        return {
          title: `${cadeira?.nome} (${grupo?.nome}) - ${professor?.nome}`,
          duration: { hours: draggedAula.duracaoHoras },
          create: true, // Indica que é um novo evento sendo criado
          extendedProps: {
            aulaId: draggedAula.id,
            cadeiraId: draggedAula.cadeiraId,
            groupId: draggedAula.grupoId,
            professorId: draggedAula.professorPreferencialId || '',
            salaId: '', // Sala será selecionada no modal
            tipo: draggedAula.tipo,
            isTempDragEvent: true // Marcador para eventos temporários de drag
          }
        };
      }
    });
  });

  function updateEvent(event: EventApi) {
    const professor = getProfessor(event.extendedProps.professorId);
    const sala = getSala(event.extendedProps.salaId);
    const cadeira = getCadeira(event.extendedProps.cadeiraId);
    const grupo = getGrupo(event.extendedProps.groupId);

    event.setProp('title', `${cadeira?.nome} (${grupo?.nome}) - ${professor?.nome} - ${sala?.nome}`);
    event.setExtendedProp('professorId', professor?.id);
    event.setExtendedProp('salaId', sala?.id);
    event.setExtendedProp('cadeiraId', cadeira?.id);
    event.setExtendedProp('groupId', grupo?.id);
  }

  function saveEvent() {
    const start = new Date(eventStart);
    const end = new Date(eventEnd);

    if (!selectedProfessorId || !selectedSalaId || !selectedCadeiraId || !selectedGrupoId) {
      currentConflictMessage = 'Por favor, preencha todos os campos obrigatórios (Professor, Sala, Cadeira, Grupo).';
      return;
    }

    const conflictMessage = checkConflict({
      start,
      end,
      professorId: selectedProfessorId,
      salaId: selectedSalaId,
      groupId: selectedGrupoId
    }, selectedEvent ? selectedEvent.id : tempEventId || undefined);

    if (conflictMessage) {
      currentConflictMessage = conflictMessage;
      return;
    }

    const professor = getProfessor(selectedProfessorId);
    const sala = getSala(selectedSalaId);
    const cadeira = getCadeira(selectedCadeiraId);
    const grupo = getGrupo(selectedGrupoId);

    let alertMessages: string[] = [];
    if (grupo!.numAlunos > sala!.capacidade) {
      alertMessages.push(`O número de alunos (${grupo!.numAlunos}) excede a capacidade da sala (${sala!.capacidade}).`);
    }

    if (sala!.especial && sala!.cursoResponsavelId && sala!.cursoResponsavelId !== grupo!.cursoId) {
      alertMessages.push(`A sala ${sala!.nome} é especial do curso ${getCurso(sala!.cursoResponsavelId)?.nome}. Uma aprovação pode ser necessária.`);
    }

    if (alertMessages.length > 0) {
        showNotification(alertMessages.join('\n\n'), 'warning'); // Usar toast para alertas não-bloqueantes
    }

    const title = `${cadeira!.nome} (${grupo!.nome}) - ${professor!.nome} - ${sala!.nome}`;

    let eventId = selectedEvent ? selectedEvent.id : tempEventId;

    if (selectedEvent) {
      // Editar evento existente
      selectedEvent.setProp('title', title);
      selectedEvent.setStart(start);
      selectedEvent.setEnd(end);
      selectedEvent.setProp('backgroundColor', eventColor);
      selectedEvent.setExtendedProp('professorId', selectedProfessorId);
      selectedEvent.setExtendedProp('salaId', selectedSalaId);
      selectedEvent.setExtendedProp('cadeiraId', selectedCadeiraId);
      selectedEvent.setExtendedProp('groupId', selectedGrupoId);
      selectedEvent.setExtendedProp('isTempDragEvent', false); // Não é mais temporário

      // Salva no localStorage
      saveEventsToLocalStorage();

      showNotification('Agendamento editado com sucesso!', 'success');
    } else {
      // Adicionar novo evento
      // Se veio de drag-and-drop, o evento já está no calendário (tempEventId)
      if (tempEventId) {
          const eventToUpdate = calendar.getEventById(tempEventId);
          if (eventToUpdate) {
              eventToUpdate.setProp('title', title);
              eventToUpdate.setStart(start);
              eventToUpdate.setEnd(end);
              eventToUpdate.setProp('backgroundColor', eventColor);
              eventToUpdate.setExtendedProp('professorId', selectedProfessorId);
              eventToUpdate.setExtendedProp('salaId', selectedSalaId);
              eventToUpdate.setExtendedProp('cadeiraId', selectedCadeiraId);
              eventToUpdate.setExtendedProp('groupId', selectedGrupoId);
              eventToUpdate.setExtendedProp('isTempDragEvent', false); // Não é mais temporário
              eventId = eventToUpdate.id;
          }
      } else {
          // Se não veio de drag-and-drop (e.g., clique em data)
          const newEvent = calendar.addEvent({
              id: String(eventIdCounter++),
              title,
              start,
              end,
              backgroundColor: eventColor,
              extendedProps: {
                  professorId: selectedProfessorId,
                  salaId: selectedSalaId,
                  cadeiraId: selectedCadeiraId,
                  groupId: selectedGrupoId,
                  isTempDragEvent: false
              }
          });
          eventId = newEvent?.id ?? null;
      }
      // AGORA A REMOÇÃO DA SIDEBAR ACONTECE APENAS AQUI, após o sucesso do saveEvent
      if (draggedAula && aulasNaoAtribuidas.some(aula => aula.id === draggedAula!.id)) {
        aulasNaoAtribuidas = aulasNaoAtribuidas.filter(aula => aula.id !== draggedAula!.id);
      }

      // Salva no localStorage
      saveEventsToLocalStorage();

      showNotification('Agendamento criado com sucesso!', 'success');
    }
    closeModal();
  }

  // Salva todos os eventos do calendário no localStorage
  function saveEventsToLocalStorage() {
    if (!calendar) return;
    const events = calendar.getEvents()
      .filter(e => !e.extendedProps.isIndisponibilidade)
      .map(e => ({
        id: e.id,
        title: e.title,
        start: e.start?.toISOString(),
        end: e.end?.toISOString(),
        backgroundColor: e.backgroundColor,
        extendedProps: e.extendedProps
      }));
    localStorage.setItem('timetableEvents', JSON.stringify(events));
  }

  // Carrega eventos do localStorage ao iniciar
  onMount(() => {
    const saved = localStorage.getItem('timetableEvents');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed)) {
          parsed.forEach(ev => {
            // Evita duplicar eventos já existentes (ex: initialEvents)
            if (!calendar.getEventById(ev.id)) {
              calendar.addEvent(ev);
            }
          });
        }
      } catch {}
    }
  });

  function deleteEvent() {
    if (selectedEvent) {
      const aulaOriginalId = selectedEvent.extendedProps.aulaId;
      if (aulaOriginalId) {
        const originalAula = mockAulasNaoAtribuidasStatic.find(a => a.id === aulaOriginalId);
        // Só adiciona de volta se ainda não estiver na lista
        if (originalAula && !aulasNaoAtribuidas.some(a => a.id === originalAula.id)) {
          aulasNaoAtribuidas = [...aulasNaoAtribuidas, originalAula];
        }
      }
      selectedEvent.remove();
      saveEventsToLocalStorage(); // Atualiza o localStorage após remover o evento
      showNotification('Agendamento excluído com sucesso.', 'success');
    }
    closeModal();
  }

  function closeModal() {
    // Se o modal está sendo fechado sem salvar um evento arrastado (que tem tempEventId)
    // E este evento ainda está marcado como temporário
    if (tempEventId) {
        const eventToRemove = calendar.getEventById(tempEventId);
        if (eventToRemove && eventToRemove.extendedProps.isTempDragEvent) {
            eventToRemove.remove(); // Remove o evento temporário do calendário
            // Se este evento veio de uma aula não atribuída, devolve-o à lista
            const aulaOriginalId = eventToRemove.extendedProps.aulaId;
            if (aulaOriginalId) {
                const originalAula = mockAulasNaoAtribuidasStatic.find(a => a.id === aulaOriginalId);
                if (originalAula && !aulasNaoAtribuidas.some(a => a.id === originalAula.id)) {
                    aulasNaoAtribuidas = [...aulasNaoAtribuidas, originalAula];
                }
            }
        }
    }

    showModal = false;
    eventStart = '';
    eventEnd = '';
    eventColor = '#4f46e5';
    selectedEvent = null;
    selectedProfessorId = '';
    selectedSalaId = '';
    selectedCadeiraId = '';
    selectedGrupoId = '';
    eventDurationHours = 1;
    currentEventCampus = '';
    currentConflictMessage = null;
    tempEventId = null;
    draggedAula = null; // Reseta draggedAula também

    clearProfessorIndisponibilities(); // Limpa as indisponibilidades dinâmicas ao fechar o modal
  }

  // --- MOCK DE AULAS NÃO ATRIBUÍDAS STATIC PARA REVERTER AO EXCLUIR ---
  // É bom ter uma cópia estática para poder "devolver" aulas à lista
  const mockAulasNaoAtribuidasStatic: AulaNaoAtribuida[] = [
    { id: 'aula1', cadeiraId: 'cad1', grupoId: 'g1_cad1', tipo: 'T', professorPreferencialId: 'p1', duracaoHoras: 1.5 },
    { id: 'aula2', cadeiraId: 'cad2', grupoId: 'g1_cad2', tipo: 'TP', professorPreferencialId: 'p2', duracaoHoras: 2 },
    { id: 'aula3', cadeiraId: 'cad3', grupoId: 'g1_cad3', tipo: 'P', professorPreferencialId: 'p3', duracaoHoras: 2.5 },
    { id: 'aula4', cadeiraId: 'cad4', grupoId: 'g1_cad4', tipo: 'T', professorPreferencialId: 'p4', duracaoHoras: 1 },
    { id: 'aula5', cadeiraId: 'cad1', grupoId: 'g2_cad1', tipo: 'T', professorPreferencialId: 'p1', duracaoHoras: 1.5 },
  ];


  // Filtra as salas disponíveis baseadas no campus do grupo (ou onde foi arrastado)
  $: filteredSalas = mockSalas.filter(sala => {
    // Se não há campus definido (ex: clique manual antes de selecionar grupo), mostrar todas
    if (!currentEventCampus) return true;
    return sala.campus === currentEventCampus;
  });

  // Filtra os grupos disponíveis para seleção no modal
  $: filteredGrupos = selectedCadeiraId ? mockGrupos.filter(g => g.cadeiraId === selectedCadeiraId) : mockGrupos;

</script>

<main class="min-h-screen bg-gray-50 p-8 flex space-x-6">
  <div id="external-events" class="w-72 bg-white rounded-xl shadow-sm p-4 flex-shrink-0">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Aulas por Atribuir</h3>
    {#if aulasNaoAtribuidas.length === 0}
      <p class="text-gray-500 text-sm">Todas as aulas foram atribuídas!</p>
    {:else}
      <ul class="space-y-3">
        {#each aulasNaoAtribuidas as aula (aula.id)}
          {@const cadeira = getCadeira(aula.cadeiraId)}
          {@const grupo = getGrupo(aula.grupoId)}
          {@const professor = getProfessor(aula.professorPreferencialId || '')}
          <li
            class="fc-event-draggable bg-indigo-500 text-white rounded-md p-3 text-sm cursor-grab shadow-md hover:shadow-lg transition-shadow duration-200"
            data-aula-id={aula.id}
          >
            <p class="font-medium">{cadeira?.nome} ({grupo?.nome}) - {aula.tipo}</p>
            <p class="text-xs">Professor: {professor?.nome || 'Não atribuído'}</p>
            <p class="text-xs">Duração: {aula.duracaoHoras}h</p>
          </li>
        {/each}
      </ul>
    {/if}
  </div>

  <div class="flex-grow bg-white rounded-xl shadow-sm overflow-hidden">
    <div bind:this={calendarEl}></div>
  </div>

  {#if showModal}
    <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg shadow-xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-900">
            {selectedEvent ? 'Editar Agendamento' : 'Novo Agendamento'}
          </h2>
          <button on:click={closeModal} class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="text-sm text-gray-600 mb-6">
          <span>{formatDate(eventStart)} {formatTime(eventStart)}</span>
          <span> – </span>
          <span>{formatDate(eventEnd)} {formatTime(eventEnd)}</span>
        </div>

        {#if currentConflictMessage}
          <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <strong class="font-bold">Erro de Conflito:</strong>
            <span class="block sm:inline">{currentConflictMessage}</span>
          </div>
        {/if}

        <div class="space-y-4">
          <div>
            <label for="cadeira" class="block text-sm font-medium text-gray-700 mb-1">Cadeira <span class="text-red-500">*</span></label>
            <select
              id="cadeira"
              bind:value={selectedCadeiraId}
              class="w-full p-2 border border-gray-200 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              on:change={() => { selectedGrupoId = ''; selectedProfessorId = ''; currentConflictMessage = null; }}
            >
              <option value="">Selecione uma cadeira</option>
              {#each mockCadeiras as cadeira}
                <option value={cadeira.id}>{cadeira.nome} ({cadeira.tipo})</option>
              {/each}
            </select>
          </div>

          <div>
            <label for="grupo" class="block text-sm font-medium text-gray-700 mb-1">Grupo de Turma <span class="text-red-500">*</span></label>
            <select
              id="grupo"
              bind:value={selectedGrupoId}
              class="w-full p-2 border border-gray-200 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              on:change={() => {
                const grupoSelecionado = getGrupo(selectedGrupoId);
                if (grupoSelecionado) {
                    const escolaDoGrupo = getEscola(grupoSelecionado.escolaId);
                    currentEventCampus = escolaDoGrupo?.campus || ''; // Define o campus para filtrar salas
                    const aulaNaoAtribuidaCorrespondente = aulasNaoAtribuidas.find(aula => aula.cadeiraId === selectedCadeiraId && aula.grupoId === selectedGrupoId);
                    if (aulaNaoAtribuidaCorrespondente?.professorPreferencialId) {
                        selectedProfessorId = aulaNaoAtribuidaCorrespondente.professorPreferencialId;
                    }
                }
                currentConflictMessage = null; // Limpa a mensagem de conflito
              }}
            >
              <option value="">Selecione um grupo</option>
              {#each filteredGrupos as grupo}
                <option value={grupo.id}>{grupo.nome} ({grupo.numAlunos} alunos)</option>
              {/each}
            </select>
          </div>

          <div>
            <label for="professor" class="block text-sm font-medium text-gray-700 mb-1">Professor <span class="text-red-500">*</span></label>
            <select
              id="professor"
              bind:value={selectedProfessorId}
              class="w-full p-2 border border-gray-200 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              on:change={() => {
                currentConflictMessage = null;
                clearProfessorIndisponibilities(); // Limpa as indisponibilidades anteriores
                if (selectedProfessorId) {
                    loadProfessorIndisponibilities(selectedProfessorId); // Carrega as do novo professor
                }
              }}
            >
              <option value="">Selecione um professor</option>
              {#each mockProfessores as prof}
                <option value={prof.id}>{prof.nome}</option>
              {/each}
            </select>
          </div>

          <div>
            <label for="sala" class="block text-sm font-medium text-gray-700 mb-1">Sala <span class="text-red-500">*</span></label>
            <select
              id="sala"
              bind:value={selectedSalaId}
              class="w-full p-2 border border-gray-200 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              on:change={() => { currentConflictMessage = null; }}
            >
              <option value="">Selecione uma sala</option>
              {#each filteredSalas as sala}
                {@const grupoInfo = getGrupo(selectedGrupoId)}
                <option value={sala.id}
                        class:text-orange-600={grupoInfo && grupoInfo.numAlunos > sala.capacidade}
                        class:font-semibold={sala.especial && sala.cursoResponsavelId && sala.cursoResponsavelId !== grupoInfo?.cursoId}>
                  {sala.nome} ({sala.capacidade} pax)
                  {#if grupoInfo && grupoInfo.numAlunos > sala.capacidade}
                    <span class="text-xs">(Capacidade Excedida!)</span>
                  {/if}
                  {#if sala.especial && sala.cursoResponsavelId && sala.cursoResponsavelId !== grupoInfo?.cursoId}
                    <span class="text-xs">(Sala Especial de {getCurso(sala.cursoResponsavelId)?.nome})</span>
                  {/if}
                </option>
              {/each}
            </select>
          </div>

          <div>
            <label for="eventColor" class="block text-sm font-medium text-gray-700 mb-1">Cor do Evento</label>
            <input type="color" id="eventColor" bind:value={eventColor}
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

  {#if showToast}
    <div class="fixed bottom-4 right-4 z-[100] p-4 rounded-lg shadow-lg flex items-center space-x-3"
         class:bg-green-500={toastType === 'success'}
         class:bg-red-500={toastType === 'error'}
         class:bg-orange-500={toastType === 'warning'}
         class:text-white={true}>
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        {#if toastType === 'success'}
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        {:else if toastType === 'error'}
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        {:else if toastType === 'warning'}
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.332 16c-.77 1.333.192 3 1.732 3z" />
        {/if}
      </svg>
      <span>{toastMessage}</span>
    </div>
  {/if}
</main>

<style>
  /* Base styles for FullCalendar */
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

  /* --- Melhorias UI/UX --- */

  /* Estilo para eventos de indisponibilidade (background) */
  :global(.fc-event-display-background) {
    background-color: #a3a3a3 !important; /* Cinza para indisponibilidade */
    border-color: #808080 !important;
    opacity: 0.4; /* Mais transparente */
    background-image: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,.1) 5px, rgba(0,0,0,.1) 10px);
  }

  /* Realce para slots inválidos ao arrastar/redimensionar */
  :global(.fc-timegrid-slot.fc-highlight-invalid) {
    background-color: rgba(255, 0, 0, 0.15) !important; /* Fundo vermelho translúcido */
    border: 1px dashed red !important;
  }

  /* Estilo para o evento "fantasma" (preview) quando em conflito */
  :global(.fc-event-dragging.fc-invalid-drop) {
      background-color: rgba(255, 0, 0, 0.6) !important; /* Ghost event vermelho mais forte */
      border-color: red !important;
  }
  :global(.fc-event-resizing.fc-invalid-drop) {
      background-color: rgba(255, 0, 0, 0.6) !important;
      border-color: red !important;
  }

  /* Estilo do Toast Notification */
  .toast-notification {
    animation: fadeInOut 3s forwards;
  }

  @keyframes fadeInOut {
    0% { opacity: 0; transform: translateY(20px); }
    10% { opacity: 1; transform: translateY(0); }
    90% { opacity: 1; transform: translateY(0); }
    100% { opacity: 0; transform: translateY(20px); }
  }
</style>