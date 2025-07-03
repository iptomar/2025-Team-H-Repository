<script lang="ts">
  import { onMount } from 'svelte';
  import { Calendar, type EventApi } from '@fullcalendar/core';
  import timeGridPlugin from '@fullcalendar/timegrid';
  import interactionPlugin from '@fullcalendar/interaction';
  import * as XLSX from 'xlsx'; // Import xlsx library
  import { apiClient } from '$lib/api';

  // --- Existing interfaces and mock data remain unchanged ---
  interface Professor {
    id: string;
    nome: string;
    email: string;
    escolaId: string;
    indisponibilidades: { id: string; start: string; end: string; title: string; type: 'single' | 'recurring' | 'full-day' }[];
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
    escolaId: string;
  }

  interface Sala {
    id: string;
    nome: string;
    capacidade: number;
    campus: string;
  }

  interface Curso {
    id: string;
    nome: string;
    escolaId: string;
  }

  // Mock data (unchanged)
  const mockProfessores: Professor[] = [
    {
      id: 'p1',
      nome: 'Prof. João Silva',
      email: 'joao.silva@ipt.pt',
      escolaId: 'e1',
      indisponibilidades: [
        { id: 'indisp1_p1', start: '2025-04-07T11:00:00', end: '2025-04-07T12:00:00', title: 'Reunião', type: 'single' },
        { id: 'indisp2_p1', start: '2025-04-09T10:00:00', end: '2025-04-09T12:00:00', title: 'Formação', type: 'single' }
      ]
    },
    {
      id: 'p2',
      nome: 'Prof. Maria Costa',
      email: 'maria.costa@ipt.pt',
      escolaId: 'e2',
      indisponibilidades: [
        { id: 'indisp1_p2', start: '2025-04-08T09:30:00', end: '2025-04-08T10:30:00', title: 'Orientação de Tese', type: 'single' }
      ]
    },
    {
      id: 'p3',
      nome: 'Prof. Pedro Santos',
      email: 'pedro.santos@ipt.pt',
      escolaId: 'e1',
      indisponibilidades: []
    }
  ];

  const mockCadeiras: Cadeira[] = [
    { id: 'cad1', nome: 'Gestão Projetos', tipo: 'T', cursoId: 'c1' },
    { id: 'cad2', nome: 'POO', tipo: 'TP', cursoId: 'c1' },
    { id: 'cad3', nome: 'EDA', tipo: 'P', cursoId: 'c1' },
    { id: 'cad4', nome: 'Análise Matemática I', tipo: 'T', cursoId: 'c2' }
  ];

  const mockGrupos: Grupo[] = [
    { id: 'g1_cad1', nome: 'G1', numAlunos: 25, cadeiraId: 'cad1', cursoId: 'c1', escolaId: 'e1' },
    { id: 'g1_cad2', nome: 'G1', numAlunos: 25, cadeiraId: 'cad2', cursoId: 'c1', escolaId: 'e1' },
    { id: 'g1_cad3', nome: 'G1', numAlunos: 20, cadeiraId: 'cad3', cursoId: 'c1', escolaId: 'e1' },
    { id: 'g1_cad4', nome: 'G1', numAlunos: 35, cadeiraId: 'cad4', cursoId: 'c2', escolaId: 'e2' }
  ];

  const mockSalas: Sala[] = [
    { id: 's1', nome: 'Sala O101', capacidade: 30, campus: 'Tomar' },
    { id: 's2', nome: 'Sala Q202', capacidade: 25, campus: 'Tomar' },
    { id: 's3', nome: 'Laboratório B303', capacidade: 20, campus: 'Tomar' },
    { id: 's4', nome: 'Sala O404', capacidade: 40, campus: 'Abrantes' }
  ];

  const mockCursos: Curso[] = [
    { id: 'c1', nome: 'Engenharia Informática', escolaId: 'e1' },
    { id: 'c2', nome: 'Gestão', escolaId: 'e2' }
  ];

  const mockEscolas = [
    { id: 'e1', nome: 'ESTT', campus: 'Tomar' },
    { id: 'e2', nome: 'ESGT', campus: 'Tomar' },
    { id: 'e3', nome: 'ESTA', campus: 'Abrantes' }
  ];

  const mockAulasAgendadas = [
    {
      id: 'aula1',
      title: 'POO (G1) - Prof. João Silva - Sala O101',
      start: '2025-04-07T09:00:00',
      end: '2025-04-07T10:30:00',
      backgroundColor: '#4f46e5',
      extendedProps: { professorId: 'p1', salaId: 's1', cadeiraId: 'cad2', groupId: 'g1_cad2' }
    },
    {
      id: 'aula2',
      title: 'Gestão Projetos (G1) - Prof. João Silva - Sala Q202',
      start: '2025-04-08T10:00:00',
      end: '2025-04-08T11:30:00',
      backgroundColor: '#3b82f6',
      extendedProps: { professorId: 'p1', salaId: 's2', cadeiraId: 'cad1', groupId: 'g1_cad1' }
    },
    {
      id: 'aula3',
      title: 'Análise Matemática I (G1) - Prof. Maria Costa - Sala O101',
      start: '2025-04-07T14:00:00',
      end: '2025-04-07T15:00:00',
      backgroundColor: '#10b981',
      extendedProps: { professorId: 'p2', salaId: 's1', cadeiraId: 'cad4', groupId: 'g1_cad4' }
    }
  ];

  // --- Existing variables and functions remain largely unchanged ---
  const loggedInProfessor: Professor = mockProfessores[0];
  let calendarElSchedule: HTMLElement;
  let calendarSchedule: Calendar;
  let calendarElAvailability: HTMLElement;
  let calendarAvailability: Calendar;
  let showIndisponibilityModal = false;
  let indispStart = '';
  let indispEnd = '';
  let indispTitle = '';
  let selectedIndisponibility: Professor['indisponibilidades'][0] | null = null;
  let indispType: 'single' | 'recurring' | 'full-day' = 'single';
  let indispRecurringDays: number[] = [];
  let indispIdCounter = 1000;
  let showToast = false;
  let toastMessage = '';
  let toastType: 'success' | 'error' | 'warning' = 'success';
  let events = [];
  let teachers = [];
  let eventsByTeacher = {};

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

  function showNotification(message: string, type: 'success' | 'error' | 'warning' = 'success') {
    toastMessage = message;
    toastType = type;
    showToast = true;
    setTimeout(() => {
      showToast = false;
    }, 3000);
  }

  // --- Existing syncIndisponibilityToScheduleCalendar, checkAvailabilityConflict, saveIndisponibility, deleteIndisponibility, closeIndisponibilityModal functions remain unchanged ---
  function syncIndisponibilityToScheduleCalendar(indisp: Professor['indisponibilidades'][0], action: 'add' | 'update' | 'remove') {
    if (!calendarSchedule) return;
    const eventIdInSchedule = `indisp-schedule-${indisp.id}`;
    if (action === 'add') {
      calendarSchedule.addEvent({
        id: eventIdInSchedule,
        title: indisp.title,
        start: indisp.start,
        end: indisp.end,
        backgroundColor: '#a3a3a3',
        borderColor: '#808080',
        display: 'background',
        classNames: ['teacher-indisponibility'],
        extendedProps: {
          isIndisponibilidade: true,
          originalIndispId: indisp.id
        }
      });
    } else if (action === 'update') {
      const eventToUpdate = calendarSchedule.getEventById(eventIdInSchedule);
      if (eventToUpdate) {
        eventToUpdate.setProp('title', indisp.title);
        eventToUpdate.setStart(indisp.start);
        eventToUpdate.setEnd(indisp.end);
      }
    } else if (action === 'remove') {
      const eventToRemove = calendarSchedule.getEventById(eventIdInSchedule);
      if (eventToRemove) {
        eventToRemove.remove();
      }
    }
    try {
      localStorage.setItem(
        `indisponibilidades-${loggedInProfessor.id}`,
        JSON.stringify(loggedInProfessor.indisponibilidades)
      );
    } catch (e) {
      showNotification('Falha ao salvar no armazenamento local.', 'warning');
    }
  }

  // Load indisponibilities from localStorage (unchanged)
  (() => {
    try {
      const stored = localStorage.getItem(`indisponibilidades-${loggedInProfessor.id}`);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed)) {
          loggedInProfessor.indisponibilidades = parsed;
        }
      }
    } catch (e) {
      // Ignore parsing errors
    }
  })();

  function checkAvailabilityConflict(newIndisp: { start: Date, end: Date }, indispIdBeingChecked?: string): string | null {
    const newIndispStart = newIndisp.start.getTime();
    const newIndispEnd = newIndisp.end.getTime();
    const roundToHalfHour = (ms: number) => Math.round(ms / (30 * 60 * 1000)) * (30 * 60 * 1000);
    const newIndispStartRounded = roundToHalfHour(newIndispStart);
    const newIndispEndRounded = roundToHalfHour(newIndispEnd);
    const professorLessons = mockAulasAgendadas.filter(aula => aula.extendedProps.professorId === loggedInProfessor.id);
    for (const lesson of professorLessons) {
      const lessonStart = new Date(lesson.start).getTime();
      const lessonEnd = new Date(lesson.end).getTime();
      const lessonStartRounded = roundToHalfHour(lessonStart);
      const lessonEndRounded = roundToHalfHour(lessonEnd);
      if (newIndispStartRounded < lessonEndRounded && newIndispEndRounded > lessonStartRounded) {
        return `Conflito: Você já tem a aula "${lesson.title}" agendada neste horário.`;
      }
    }
    const currentIndisponibilities = calendarAvailability.getEvents();
    for (const existingIndisp of currentIndisponibilities) {
      if (existingIndisp.id === indispIdBeingChecked) continue;
      const existingIndispStart = existingIndisp.start!.getTime();
      const existingIndispEnd = existingIndisp.end!.getTime();
      const existingIndispStartRounded = roundToHalfHour(existingIndispStart);
      const existingIndispEndRounded = roundToHalfHour(existingIndispEnd);
      if (newIndispStartRounded < existingIndispEndRounded && newIndispEndRounded > existingIndispStartRounded) {
        return `Conflito: Você já marcou uma indisponibilidade "${existingIndisp.title}" neste horário.`;
      }
    }
    return null;
  }

  function saveIndisponibility() {
    const start = new Date(indispStart);
    const end = new Date(indispEnd);
    if (!indispTitle) {
      showNotification('Por favor, insira um título para a indisponibilidade.', 'error');
      return;
    }
    const conflictMessage = checkAvailabilityConflict({ start, end }, selectedIndisponibility?.id);
    if (conflictMessage) {
      showNotification(conflictMessage, 'error');
      return;
    }
    let updatedIndisps: Professor['indisponibilidades'];
    if (selectedIndisponibility) {
      const originalIndispId = selectedIndisponibility.id;
      const updatedIndisp = { ...selectedIndisponibility, start: start.toISOString(), end: end.toISOString(), title: indispTitle, type: indispType };
      loggedInProfessor.indisponibilidades = loggedInProfessor.indisponibilidades.map(indisp =>
        indisp.id === originalIndispId ? updatedIndisp : indisp
      );
      updatedIndisps = loggedInProfessor.indisponibilidades;
      const eventToUpdate = calendarAvailability.getEventById(originalIndispId);
      if (eventToUpdate) {
        eventToUpdate.setProp('title', indispTitle);
        eventToUpdate.setStart(start);
        eventToUpdate.setEnd(end);
        eventToUpdate.setExtendedProp('type', indispType);
      }
      syncIndisponibilityToScheduleCalendar(updatedIndisp, 'update');
      showNotification('Indisponibilidade atualizada com sucesso!', 'success');
    } else {
      const newId = `indisp-${loggedInProfessor.id}-${indispIdCounter++}`;
      const newIndisp = { id: newId, start: start.toISOString(), end: end.toISOString(), title: indispTitle, type: indispType };
      loggedInProfessor.indisponibilidades.push(newIndisp);
      updatedIndisps = loggedInProfessor.indisponibilidades;
      calendarAvailability.addEvent({
        id: newId,
        title: indispTitle,
        start: start,
        end: end,
        backgroundColor: '#a3a3a3',
        borderColor: '#808080',
        extendedProps: { type: indispType }
      });
      syncIndisponibilityToScheduleCalendar(newIndisp, 'add');
      showNotification('Indisponibilidade adicionada com sucesso!', 'success');
    }
    try {
      localStorage.setItem(
        `indisponibilidades-${loggedInProfessor.id}`,
        JSON.stringify(updatedIndisps)
      );
    } catch (e) {
      showNotification('Falha ao salvar no armazenamento local.', 'warning');
    }
    closeIndisponibilityModal();
  }

  function deleteIndisponibility() {
    if (selectedIndisponibility) {
      const indispToDelete = selectedIndisponibility;
      loggedInProfessor.indisponibilidades = loggedInProfessor.indisponibilidades.filter(indisp => indisp.id !== indispToDelete.id);
      const eventToRemove = calendarAvailability.getEventById(indispToDelete.id);
      if (eventToRemove) {
        eventToRemove.remove();
      }
      syncIndisponibilityToScheduleCalendar(indispToDelete, 'remove');
      try {
        localStorage.setItem(
          `indisponibilidades-${loggedInProfessor.id}`,
          JSON.stringify(loggedInProfessor.indisponibilidades)
        );
      } catch (e) {
        showNotification('Falha ao atualizar o armazenamento local.', 'warning');
      }
      showNotification('Indisponibilidade excluída com sucesso!', 'success');
    }
    closeIndisponibilityModal();
  }

  function closeIndisponibilityModal() {
    showIndisponibilityModal = false;
    indispStart = '';
    indispEnd = '';
    indispTitle = '';
    selectedIndisponibility = null;
    indispType = 'single';
    indispRecurringDays = [];
  }

  // --- New Function: Export Timetable to Excel ---
  function exportToExcel() {
    if (!calendarSchedule) {
      showNotification('Erro: Calendário não está inicializado.', 'error');
      return;
    }

    // Get all events from the schedule calendar
    const events = calendarSchedule.getEvents();

    // Determine the week range (Monday to Sunday)
    const weekDays = [
      { key: 1, label: 'Segunda' },
      { key: 2, label: 'Terça' },
      { key: 3, label: 'Quarta' },
      { key: 4, label: 'Quinta' },
      { key: 5, label: 'Sexta' },
      { key: 6, label: 'Sábado' },
      { key: 0, label: 'Domingo' }
    ];

    // Define time slots (08:00 to 23:00, every 30 min)
    const slots: string[] = [];
    for (let h = 8; h <= 23; h++) {
      slots.push(`${h.toString().padStart(2, '0')}:00`);
      if (h !== 23) slots.push(`${h.toString().padStart(2, '0')}:30`);
    }

    // Build a map: { slot: { weekday: eventString } }
    const timetable: Record<string, Record<number, string>> = {};
    for (const slot of slots) {
      timetable[slot] = {};
      for (const day of weekDays) {
        timetable[slot][day.key] = '';
      }
    }

    // Fill timetable with events
    for (const event of events) {
      const isIndisponibility = event.extendedProps.isIndisponibilidade || false;
      const start = new Date(event.start!);
      const end = new Date(event.end!);
      let current = new Date(start);

      // For each slot the event covers, fill the cell
      while (current < end) {
        const hour = current.getHours().toString().padStart(2, '0');
        const min = current.getMinutes().toString().padStart(2, '0');
        const slotKey = `${hour}:${min}`;
        const weekday = current.getDay(); // 0=Sunday, 1=Monday, ...
        if (timetable[slotKey] && timetable[slotKey][weekday] === '') {
          timetable[slotKey][weekday] = isIndisponibility
            ? `Indisp.: ${event.title}`
            : `${event.title}`;
        }
        // Next slot (30 min)
        current = new Date(current.getTime() + 30 * 60 * 1000);
      }
    }

    // Prepare data for Excel: first row is header
    const header = ['Hora', ...weekDays.map(d => d.label)];
    const excelData = [header];
    for (const slot of slots) {
      const row = [slot];
      for (const day of weekDays) {
        row.push(timetable[slot][day.key]);
      }
      excelData.push(row);
    }

    // Create worksheet
    const worksheet = XLSX.utils.aoa_to_sheet(excelData);

    // Set column widths
    worksheet['!cols'] = [
      { wch: 8 }, // Hora
      ...weekDays.map(() => ({ wch: 32 }))
    ];

    // Create workbook and append worksheet
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Horário');

    // Generate and download Excel file
    XLSX.writeFile(
      workbook,
      `Horario_${loggedInProfessor.nome.replace(/\s+/g, '_')}_${formatDate(new Date())}.xlsx`
    );

    showNotification('Horário exportado com sucesso!', 'success');
  }

  // --- FullCalendar Setup (unchanged except for onMount) ---
  onMount(async () => {
    const professorScheduledLessons = mockAulasAgendadas.filter(aula => aula.extendedProps.professorId === loggedInProfessor.id)
      .map(aula => ({
        ...aula,
        classNames: ['teacher-lesson']
      }));
    const professorIndisponibilitiesForSchedule = loggedInProfessor.indisponibilidades.map(indisp => ({
      id: `indisp-schedule-${indisp.id}`,
      title: indisp.title,
      start: indisp.start,
      end: indisp.end,
      backgroundColor: '#a3a3a3',
      borderColor: '#808080',
      display: 'background',
      classNames: ['teacher-indisponibility'],
      extendedProps: {
        isIndisponibilidade: true,
        originalIndispId: indisp.id
      }
    }));
    const allProfessorEvents = [...professorScheduledLessons, ...professorIndisponibilitiesForSchedule];

    calendarSchedule = new Calendar(calendarElSchedule, {
      plugins: [timeGridPlugin],
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
      events: allProfessorEvents,
      editable: false,
      selectable: false,
      eventContent: function(arg) {
        if (!arg.event.extendedProps.isIndisponibilidade) {
          return { html: `
            <div class="fc-event-main-frame">
              <div class="fc-event-time">${formatTime(arg.event.start!)} - ${formatTime(arg.event.end!)}</div>
              <div class="fc-event-title-container">
                <div class="fc-event-title fc-sticky">${arg.event.title}</div>
                ${arg.event.extendedProps.salaId ? `<div class="fc-event-location text-xs">${getSala(arg.event.extendedProps.salaId)?.nome}</div>` : ''}
              </div>
            </div>
          `};
        }
        return { html: `<div class="fc-event-title fc-sticky">${arg.event.title}</div>` };
      }
    });
    calendarSchedule.render();

    const initialIndisponibilities = loggedInProfessor.indisponibilidades.map(indisp => ({
      id: indisp.id,
      title: indisp.title,
      start: indisp.start,
      end: indisp.end,
      backgroundColor: '#a3a3a3',
      borderColor: '#808080',
      extendedProps: { type: indisp.type }
    }));

    calendarAvailability = new Calendar(calendarElAvailability, {
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
      events: initialIndisponibilities,
      editable: true,
      selectable: true,
      select: (info) => {
        indispStart = info.startStr;
        indispEnd = info.endStr;
        indispTitle = '';
        selectedIndisponibility = null;
        indispType = 'single';
        showIndisponibilityModal = true;
      },
      eventClick: (info) => {
        const clickedIndisp = loggedInProfessor.indisponibilidades.find(indisp => indisp.id === info.event.id);
        if (clickedIndisp) {
          selectedIndisponibility = clickedIndisp;
          indispStart = info.event.start!.toISOString();
          indispEnd = info.event.end?.toISOString() || '';
          indispTitle = info.event.title;
          indispType = info.event.extendedProps.type || 'single';
          showIndisponibilityModal = true;
        }
      },
      eventDrop: (info) => {
        const newStart = info.event.start!;
        const newEnd = info.event.end!;
        const conflict = checkAvailabilityConflict({ start: newStart, end: newEnd }, info.event.id);
        if (conflict) {
          info.revert();
          showNotification(conflict, 'error');
        } else {
          const updatedIndisp = {
            id: info.event.id,
            start: newStart.toISOString(),
            end: newEnd.toISOString(),
            title: info.event.title,
            type: info.event.extendedProps.type
          };
          loggedInProfessor.indisponibilidades = loggedInProfessor.indisponibilidades.map(indisp =>
            indisp.id === updatedIndisp.id ? updatedIndisp : indisp
          );
          syncIndisponibilityToScheduleCalendar(updatedIndisp, 'update');
          showNotification('Indisponibilidade movida com sucesso!', 'success');
        }
      },
      eventResize: (info) => {
        const newStart = info.event.start!;
        const newEnd = info.event.end!;
        const conflict = checkAvailabilityConflict({ start: newStart, end: newEnd }, info.event.id);
        if (conflict) {
          info.revert();
          showNotification(conflict, 'error');
        } else {
          const updatedIndisp = {
            id: info.event.id,
            start: newStart.toISOString(),
            end: newEnd.toISOString(),
            title: info.event.title,
            type: info.event.extendedProps.type
          };
          loggedInProfessor.indisponibilidades = loggedInProfessor.indisponibilidades.map(indisp =>
            indisp.id === updatedIndisp.id ? updatedIndisp : indisp
          );
          syncIndisponibilityToScheduleCalendar(updatedIndisp, 'update');
          showNotification('Indisponibilidade redimensionada com sucesso!', 'success');
        }
      }
    });
    calendarAvailability.render();

    events = await apiClient.getEvents();
    // Assume you have a way to get all teachers
    teachers = await apiClient.getTeachers ? await apiClient.getTeachers() : [];
    // Group events by teacherId
    eventsByTeacher = {};
    for (const event of events) {
      const tid = event.extendedProps?.professorId || event.professorId;
      if (!tid) continue;
      if (!eventsByTeacher[tid]) eventsByTeacher[tid] = [];
      eventsByTeacher[tid].push(event);
    }
  });

  interface AulaNaoAtribuida {
    id: string;
    title: string;
    start: string;
    end: string;
    backgroundColor: string;
    borderColor: string;
    extendedProps: {
      professorId?: string;
      salaId?: string;
      cadeiraId?: string;
      groupId?: string;
    };
  }
  const mockAulasNaoAtribuidasStatic: AulaNaoAtribuida[] = [];
</script>

<div class="flex flex-col items-center justify-center min-h-[60vh]">
  <h1 class="text-3xl font-bold mb-4 text-blue-700">Teachers</h1>
  <p class="text-lg text-gray-700">This page will show teacher information and schedules soon.</p>
</div>

<main class="min-h-screen bg-gray-50 p-8">
  <div class="max-w-7xl mx-auto space-y-8">
    <div class="bg-white rounded-xl shadow-sm p-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Bem-vindo, {loggedInProfessor.nome}!</h1>
      <p class="text-gray-600">Este é o seu dashboard. Aqui pode visualizar o seu horário e gerir as suas indisponibilidades.</p>
      <div class="mt-4 text-sm text-gray-700">
        <p><span class="font-semibold">Email:</span> {loggedInProfessor.email}</p>
        <p><span class="font-semibold">Escola:</span> {getEscola(loggedInProfessor.escolaId)?.nome}</p>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm overflow-hidden p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-semibold text-gray-900">Meu Horário Atual</h2>
        <button
          on:click={exportToExcel}
          class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
        >
          Exportar para Excel
        </button>
      </div>
      <div bind:this={calendarElSchedule} class="h-[600px]"></div>
    </div>

    <div class="bg-white rounded-xl shadow-sm overflow-hidden p-6">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">Minhas Indisponibilidades</h2>
      <p class="text-gray-600 mb-4">
        Clique e arraste no calendário para adicionar uma nova indisponibilidade, ou clique numa existente para editar/remover.
      </p>
      <div bind:this={calendarElAvailability} class="h-[600px]"></div>
    </div>
  </div>

  {#if showIndisponibilityModal}
    <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg shadow-xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-900">
            {selectedIndisponibility ? 'Editar Indisponibilidade' : 'Nova Indisponibilidade'}
          </h2>
          <button on:click={closeIndisponibilityModal} class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="text-sm text-gray-600 mb-6">
          <span>{formatDate(indispStart)} {formatTime(indispStart)}</span>
          <span> – </span>
          <span>{formatDate(indispEnd)} {formatTime(indispEnd)}</span>
        </div>

        <div class="space-y-4">
          <div>
            <label for="indispTitle" class="block text-sm font-medium text-gray-700 mb-1">Título <span class="text-red-500">*</span></label>
            <input type="text" id="indispTitle" bind:value={indispTitle}
                   class="w-full p-2 border border-gray-200 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                   placeholder="Ex: Reunião de departamento, consulta médica" />
          </div>
          <div class="hidden">
            <label for="indispType" class="block text-sm font-medium text-gray-700 mb-1">Tipo de Indisponibilidade</label>
            <select id="indispType" bind:value={indispType} class="w-full p-2 border border-gray-200 rounded-md">
              <option value="single">Evento Único</option>
              <option value="recurring">Recorrente Semanal</option>
              <option value="full-day">Dia Inteiro</option>
            </select>
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          {#if selectedIndisponibility}
            <button
              on:click={deleteIndisponibility}
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              Excluir
            </button>
          {/if}
          <button
            on:click={closeIndisponibilityModal}
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
          >
            Cancelar
          </button>
          <button
            on:click={saveIndisponibility}
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>
  {/if}

  {#if showToast}
    <div class="fixed bottom-4 right-4 z-[100] p-4 rounded-lg shadow-lg flex items-center space-x-3 toast-notification"
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

  <h1 class="text-2xl font-bold mb-6">Teachers' Schedules</h1>
  {#if teachers.length === 0}
    <p>No teachers found.</p>
  {:else}
    <div class="space-y-8">
      {#each teachers as teacher}
        <div class="bg-white rounded shadow p-4">
          <h2 class="text-xl font-semibold mb-2">{teacher.nome}</h2>
          {#if eventsByTeacher[teacher.id]?.length}
            <ul class="list-disc ml-6">
              {#each eventsByTeacher[teacher.id] as event}
                <li class="mb-1">
                  <span class="font-medium">{event.title}</span>
                  <span class="text-gray-600 text-sm"> ({new Date(event.start).toLocaleString()} - {new Date(event.end).toLocaleString()})</span>
                </li>
              {/each}
            </ul>
          {:else}
            <p class="text-gray-500">No scheduled events.</p>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</main>

<style>
  /* Existing styles remain unchanged */
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
  :global(.teacher-lesson) {
    background-color: #4f46e5 !important;
    border-color: #4f46e5 !important;
  }
  :global(.teacher-indisponibility) {
    background-color: #a3a3a3 !important;
    border-color: #808080 !important;
    opacity: 0.4;
    background-image: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,.1) 5px, rgba(0,0,0,.1) 10px);
  }
  :global(.fc-timegrid-slot.fc-highlight-invalid) {
    background-color: rgba(255, 0, 0, 0.15) !important;
    border: 1px dashed red !important;
  }
  :global(.fc-event-dragging.fc-invalid-drop) {
    background-color: rgba(255, 0, 0, 0.6) !important;
    border-color: red !important;
  }
  :global(.fc-event-resizing.fc-invalid-drop) {
    background-color: rgba(255, 0, 0, 0.6) !important;
    border-color: red !important;
  }
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