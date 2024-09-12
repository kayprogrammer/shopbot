$(document).ready(function () {
    const $chatForm = $("#chat-form");
    const $messageInput = $("#message-input");
    const $chatArea = $("#chat-area");
    const $submitButton = $("#send-btn-div"); // Assuming you have a submit button with this ID

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    $chatForm.on("submit", function (event) {
        const $sendButton = $("#send-btn"); // Assuming you have a send button with this ID
        event.preventDefault();

        let userMessage = $messageInput.val().trim();
        if (userMessage === "") {
            alert("Please enter a message.");
            return;
        }

        if (userMessage.length > 500) { // Example maximum length
            alert("Message is too long. Please limit to 500 characters.");
            return;
        }

        $chatArea.append(`
            <div class="message user-message">
                <p>${escapeHtml(userMessage)}</p>
            </div>
        `);

        $messageInput.val("");
        $submitButton.prop('disabled', true);
        $sendButton.html(`
            <button class="btn btn-primary" type="button" id="send-btn" disabled>
                <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                Processing request...
            </button>
        `)
        $.ajax({
            url: "/chat",
            type: "POST",
            data: JSON.stringify({ message: userMessage }),
            contentType: 'application/json',
            dataType: "json",
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value // Include CSRF token
            },
            success: function (response) {
                console.log(response)
                $chatArea.append(`
                    <div class="message bot-message">
                        <p>${response.message.response_text}</p>
                    </div>
                `);

                if (response.products && response.products.length > 0) {
                    let productHTML = '<div class="row">';
                    response.products.forEach(product => {
                        productHTML += `
                            <div class="col-md-4 mb-4">
                                <div class="card product-card">
                                    <img src="${escapeHtml(product.image)}" class="card-img-top" alt="${product.title}">
                                    <div class="card-body">
                                        <h6 class="card-title">Platform: ${product.source}</h6>
                                        <h5 class="card-title">${product.title}</h5>
                                        <p class="card-text">$${product.price}</p>
                                        <a href="${product.link}" class="btn btn-primary" target="_blank">View Product</a>
                                        <p class="mt-2">Rating: ${product.rating} / 5</p>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                    productHTML += '</div>';
                    $chatArea.append(productHTML);
                }

                $chatArea.scrollTop($chatArea[0].scrollHeight);
                $sendButton.html(`<button class="btn btn-primary" type="submit" id="send-btn">Send</button>`)
            },
            error: function (xhr, status, error) {
                alert(`Error communicating with the server: ${error}`);
                console.error("AJAX error:", status, error);
            },
            complete: function() {
                $submitButton.prop('disabled', false);
            }
        });
    });
});