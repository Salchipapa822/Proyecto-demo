function ordenarComentarios(order) {
    const commentList = document.getElementById('comment-list');
    const comments = Array.from(commentList.getElementsByTagName('li'));

    // Ordenar los comentarios según la fecha
    comments.sort((a, b) => {
        const fechaA = parseInt(a.getAttribute('data-fecha'));
        const fechaB = parseInt(b.getAttribute('data-fecha'));
        return order === 'newest' ? fechaB - fechaA : fechaA - fechaB;
    });

    // Limpiar la lista de comentarios
    commentList.innerHTML = '';

    // Agregar los comentarios ordenados de nuevo a la lista
    comments.forEach(comment => {
        commentList.appendChild(comment);
    });
}