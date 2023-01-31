
window.onload = function () {

    // Delete user account confirmation
    $(document).ready(function () {

        $("#delete-account-button").click(function () {
            $("#confirm-delete-modal").modal("show");
        });

        $("#confirm-delete-button").click(function () {
            $("#delete-account-form form").submit();
        });

    });


    // Get references to the password inputs and the submit button
    const passwordInput = document.getElementById("password");
    const retypePasswordInput = document.getElementById("retype-password");
    const submitButton = document.querySelector("button[type='submit']");

    // Add event listeners to the password inputs
    passwordInput.addEventListener("input", checkPasswordsMatch);
    retypePasswordInput.addEventListener("input", checkPasswordsMatch);

    // Check if the passwords match and update the message and submit button
    function checkPasswordsMatch() {
        const password = passwordInput.value;
        const retypePassword = retypePasswordInput.value;
        const matchMessages = document.querySelectorAll(".do-passwords-match");

        if (password === retypePassword) {
            matchMessages.forEach(matchMessage => {
                matchMessage.textContent = "Passwords match";
                matchMessage.classList.remove("text-danger");
                matchMessage.classList.add("text-success");
            });
            submitButton.disabled = false;
        } else {
            matchMessages.forEach(matchMessage => {
                matchMessage.textContent = "Passwords do not match";
                matchMessage.classList.remove("text-success");
                matchMessage.classList.add("text-danger");
            });
            submitButton.disabled = true;
        }
    }
}
