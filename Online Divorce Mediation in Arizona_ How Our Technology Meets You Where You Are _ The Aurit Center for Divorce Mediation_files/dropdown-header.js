// // Add this JavaScript for mobile dropdown functionality
// document.addEventListener('DOMContentLoaded', function() {
//     // Toggle mobile menu
//     const menuToggler = document.querySelector('.navbar-menu-toggler');
//     const menu = document.querySelector('.navbar-menu');
//
//     if (menuToggler) {
//         menuToggler.addEventListener('click', function() {
//             menu.classList.toggle('menu-open');
//             document.body.classList.toggle('menu-is-open');
//         });
//     }
//
//     // Handle dropdown toggles on mobile
//     const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
//
//     dropdownToggles.forEach(toggle => {
//         toggle.addEventListener('click', function(e) {
//             // Only for mobile view
//             if (window.innerWidth < 992) {
//                 e.preventDefault();
//                 const parent = this.parentNode;
//                 parent.classList.toggle('active');
//             }
//         });
//     });
// });
