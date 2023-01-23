// const openButton = document.getElementById("open-button");
// const testingButton = document.getElementById("testing-button");
// const completeButton = document.getElementById("complete-button");

// const bugs = document.getElementsByClassName("bug");

// openButton.addEventListener("click", () => {
//   showLoadingSpinner();
//   filterBugs("OPEN");
//   hideLoadingSpinner();
// });

// testingButton.addEventListener("click", () => {
//   showLoadingSpinner();
//   filterBugs("TESTING");
//   hideLoadingSpinner();
// });

// completeButton.addEventListener("click", () => {
//   showLoadingSpinner();
//   filterBugs("COMPLETE");
//   hideLoadingSpinner();
// });

// //function filterBugs(status) {
// //  Array.from(bugs).forEach(bug => {
// //    if (bug.getAttribute("data-status") === status) {
// //      bug.style.display = "block";
// //    } else {
// //      bug.style.display = "none";
// //    }
// //  });
// //}

// function showLoadingSpinner() {
//   const loadingSpinner = document.getElementById("loading-spinner");
//   loadingSpinner.classList.remove("d-none");
// }

// function hideLoadingSpinner() {
//   const loadingSpinner = document.getElementById("loading-spinner");
//   loadingSpinner.classList.add("d-none");
// }

// //function filterBugs(status) {
// //// Hide all bugs
// //$('#bugs li').hide();
// //
// //// Show only the bugs with the specified status
// //$('#bugs li[data-status="' + status + '"]').show();
// //}


// function filterBugs(status) {
//     var bugs = document.querySelectorAll('.card');
//     for (var i = 0; i < bugs.length; i++) {
//         var bug = bugs[i];
//         var bugStatus = bug.querySelector('.text-muted').textContent;
//         if (bugStatus === status) {
//             bug.style.display = "block";
//         }
//         else if (status === 'ALL'){
//             bug.style.display = "block";
//         }
//         else {
//             bug.style.display = "none";
//         }
//     }
// }

// //function filterBugs(status) {
// //    var elements = document.getElementsByClassName("status-" + status);
// //    for (var i = 0; i < elements.length; i++) {
// //        elements[i].style.display = elements[i].style.display === "none" ? "" : "none";
// //    }
// //}

// // Registration

// // Registration Ends