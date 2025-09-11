(function () {
    const responseDiv = document.querySelector(".form-container");
    const form = document.getElementById("credit-simulation-form");
    const submitBtn = document.getElementById("submit-form-btn");
    const url = window.location.href;

    const clearErrors = () => {
        document.querySelectorAll(".error-message").forEach(el => (el.textContent = ""));
    };

    const renderResponse = (released_value) => {
        const heading = released_value != "R$ 0,00" ? "Sucesso!" : "Parece que não foi dessa vez...";
        const content = released_value != "R$ 0,00"
            ? `<p class="response-text-1">Você possui um crédito aprovado de:</p>
               <p class="response-text-2">${released_value}</p>`
            : `<p class="response-text-1">Mas não desanime, você pode tentar novamente em outro momento!</p>`;
        responseDiv.innerHTML = `
            <div class="response p-4 border rounded" autocomplete="off" style="background: rgba(255, 255, 255, 0.2); border-radius: 16px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.3);">
                <h3>${heading}</h3>
                ${content}
            </div>`;
    };

    const renderErrorResponse = () => {
        const heading = "Erro inesperado!";
        const content = `<p class="response-text-1">Parece que houve um erro em nossos sistemas.
                        Tente novamente em outro momento.</p>`;
        responseDiv.innerHTML = `
            <div class="response p-4 border rounded" class="p-4 border rounded" autocomplete="off" style="background: rgba(255, 255, 255, 0.2); border-radius: 16px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.3);>
                <h3>${heading}</h3>
                ${content}
            </div>`;
    }

    const handleErrors = async errorResponse => {
        const errors = await errorResponse;
        if (errors.errors) {
            for (const [field, details] of Object.entries(errors.errors)) {
                const errorElement = document.getElementById(`${field}-error`);
                if (errorElement) errorElement.textContent = details[0].message;
            }
            submitBtn.innerHTML = "Simular Crédito";
            turnstile.reset();
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
                renderResponse(data.data);
            } else {
                renderErrorResponse();
            }
        } catch (errorResponse) {
            handleErrors(errorResponse);
        }
    });
})();
