function deleteSess(sessId) {
    fetch('/delete-sess', {
        method: 'POST',
        body: JSON.stringify({ sessId: sessId })
    }).then((_res) => {
        window.location.reload();
    });
}