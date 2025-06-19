(function () {
    function formatPhone(phone) {
        let value = phone.value.replace(/\D/g, ""); // Remove caracteres não numéricos

        if (value.length > 11) value = value.slice(0, 11); // Limita o número a 11 dígitos

        let formattedValue = "";

        if (value.length > 2) {
            formattedValue = `(${value.slice(0, 2)})`;
            if (value.length > 7) {
                formattedValue += ` ${value.slice(2, 7)}-${value.slice(7)}`; // Formato (XX) XXXXX-XXXX
            } else if (value.length > 2) {
                formattedValue += ` ${value.slice(2)}`; // Formato (XX) XXXXX
            }
        } else {
            formattedValue = value; // Caso o número seja menor que 2 dígitos
        }

        phone.value = formattedValue;
    }

    const input = document.getElementById("phone");

    document.addEventListener("DOMContentLoaded", () => {
        formatPhone(input);
    });

    input.addEventListener("input", () => {
        formatPhone(input);
    });
})();
