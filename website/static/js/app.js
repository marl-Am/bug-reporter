
// filter tasks
function filterTasks(status) {
    if (status === 'All') { }
    else if (status === 'open') { }
    else if (status === 'testing') { }
    else { }
}

function deleteProject(projectId) {
    fetch("/delete_project", {
        method: "POST",
        body: JSON.stringify({ projectId: projectId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteTask(taskId) {
    fetch("/delete_task", {
        method: "POST",
        body: JSON.stringify({ taskId: taskId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

// $(document).ready(function () {
//     setTimeout(function () {
//         $('.alert').fadeOut('fast');
//     }, 3000);
// });

window.onload = function () {


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