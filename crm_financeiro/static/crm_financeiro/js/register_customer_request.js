(function () {
    const responseDiv = document.querySelector(".form-container");
    const form = document.getElementById("register-customer-form");
    const submitBtn = document.getElementById("submit-form-btn");
    const url = window.location.href;

    const clearErrors = () => {
        document.querySelectorAll(".error-message").forEach(el => (el.textContent = ""));
    };

    const renderResponse = (redirect_url) => {
        const heading = "Cliente cadastrado com sucesso!";
        const content = `
            <p class="response-text-1">Agora você pode gerar propostas para esse cliente.</p>
            <a href="${redirect_url}" class="btn btn-primary">Acessar dados do cliente.</a>
        `;
        responseDiv.innerHTML = `
            <div class="response p-4 border rounded" autocomplete="off">
                <h3>${heading}</h3>
                ${content}
            </div>`;
    };

    const renderErrorResponse = () => {
        const heading = "Erro inesperado!";
        const content = `<p class="response-text-1">Parece que houve um erro em nossos sistemas.
                        Tente novamente em outro momento.</p>`;
        responseDiv.innerHTML = `
            <div class="response p-4 border rounded" autocomplete="off">
                <h3>${heading}</h3>
                ${content}
            </div>`;
    }

    const handleErrors = async errorResponse => {
        const errors = await errorResponse;
        if (errors.errors) {
            for (const [field, details] of Object.entries(errors.errors)) {
                const errorElement = document.getElementById(`${field}-error`);
                if (errorElement) {
                    errorElement.textContent = details[0].message;
                    errorElement.className = "error-message alert alert-danger mt-1 pt-1 pb-1 pr-3 pl-3 d-block";
                }
            }
            submitBtn.innerHTML = "Cadastrar";
        } else {
            renderErrorResponse();
        }
    };

    form.addEventListener("submit", async e => {
        e.preventDefault();
        clearErrors();
        submitBtn.innerHTML = "Aguarde...";

        const formData = new FormData(form);
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": form.querySelector("input[name='csrfmiddlewaretoken']").value,
                },
                body: formData,
            });

            if (!response.ok) {
                if (response.headers.get("Content-Type")?.includes("application/json")) {
                    throw await response.json();
                } else {
                    throw new Error("Response is not valid JSON.");
                }
            }

            const data = await response.json();
            if (data.success) {
                renderResponse(data.redirect_url);
            } else {
                renderErrorResponse();
            }
        } catch (errorResponse) {
            handleErrors(errorResponse);
        }
    });
})();
