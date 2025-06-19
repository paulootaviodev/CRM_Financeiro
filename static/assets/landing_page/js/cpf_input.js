(function () {
    function formatCPF(cpf) {
        let value = cpf.value.replace(/\D/g, ""); // Remove caracteres não numéricos

        if (value.length > 11) value = value.slice(0, 11); // Limita o número a 11 dígitos

        let formattedValue = "";

        if (value.length > 3) {
            formattedValue = `${value.slice(0, 3)}.${value.slice(3, 6)}`;
            if (value.length > 6) {
                formattedValue += `.${value.slice(6, 9)}`;
                if (value.length > 9) {
                    formattedValue += `-${value.slice(9)}`; // Formato xxx.xxx.xxx-xx
                }
            }
        } else {
            formattedValue = value; // Caso o número seja menor que 3 dígitos
        }

        cpf.value = formattedValue;
    }

    const input = document.getElementById("cpf");

    document.addEventListener("DOMContentLoaded", () => {
        formatCPF(input);
    });

    input.addEventListener("input", () => {
        formatCPF(input);
    });
})();
