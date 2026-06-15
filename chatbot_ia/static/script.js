async function enviarMensaje() {
  const input = document.getElementById('mensaje');
  const mensaje = input.value.trim();

  if (!mensaje) return;

  const chat = document.getElementById('chat');

  // Mostrar mensaje del usuario
  chat.innerHTML += `
    <div class="mensaje usuario">
      <span class="burbuja">${mensaje}</span>
    </div>
  `;

  input.value = '';
  scrollAbajo();

  // Indicador de escritura
  const idEscribiendo = 'escribiendo-' + Date.now();
  chat.innerHTML += `
    <div class="mensaje bot escribiendo" id="${idEscribiendo}">
      <span class="burbuja"></span>
    </div>
  `;
  scrollAbajo();

  try {
    const respuesta = await fetch('/mensaje', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mensaje: mensaje })
    });

    const datos = await respuesta.json();

    // Remover indicador y mostrar respuesta
    document.getElementById(idEscribiendo)?.remove();

    chat.innerHTML += `
      <div class="mensaje bot">
        <span class="burbuja">${datos.respuesta}</span>
      </div>
    `;
  } catch (error) {
    document.getElementById(idEscribiendo)?.remove();
    chat.innerHTML += `
      <div class="mensaje bot">
        <span class="burbuja">Error al conectar con el servidor.</span>
      </div>
    `;
  }

  scrollAbajo();
}

function scrollAbajo() {
  const chat = document.getElementById('chat');
  chat.scrollTop = chat.scrollHeight;
}
