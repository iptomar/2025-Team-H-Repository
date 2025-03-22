<script>
  const horas = [
    '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30',
    '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
    '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
    '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00'
  ];
  const dias = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'];
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
            <td class="px-2">{hora}</td>
            {#each dias as _}
              <td class="px-2"></td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</main>

<style>
  table { width: 100%; border-collapse: collapse; }
  th, td { border: 1px solid #e2e8f0; }
  th { background-color: #2b6cb0; }
</style>
