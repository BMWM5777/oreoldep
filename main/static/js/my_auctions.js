function openModal(id, title, imageUrl, status, price, description, endTime, adminComment) {
    const modalContent = `
    <div class="modal-header">
        <h5 class="modal-title" id="auctionModalLabel">${title}</h5>
    </div>
    <div class="modal-body">
        <div class="auction-modal-gallery">
            <img id="auction-modal-main-image"
                 src="${imageUrl}"
                 class="auction-modal-main-img"
                 alt="${title}">
        </div>
        <p class="auction-modal-description">
            <strong>Описание:</strong> ${description || "Описание отсутствует"}
        </p>
        ${adminComment ? `<p class="auction-modal-admin-comment"><strong>Комментарий администратора:</strong> ${adminComment}</p>` : ""}
        <p class="auction-modal-price">
            <strong>Текущая цена:</strong> ${price} тенге
        </p>
        <p class="auction-modal-endtime">
            <strong>Дата окончания:</strong> ${endTime}
        </p>
        <p class="auction-modal-status">
            <strong>Статус:</strong> ${status}
        </p>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
    </div>
    `;
    document.getElementById('auction-modal-content').innerHTML = modalContent;
    const modal = new bootstrap.Modal(document.getElementById('auctionModal'));
    modal.show();
}
