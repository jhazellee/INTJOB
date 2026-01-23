document.addEventListener('DOMContentLoaded', function() {
  const authModal = document.getElementById('authModal');
  const loginForm = document.getElementById('loginForm');
  const signUpForm = document.getElementById('signUpForm');
  const switchToSignup = document.getElementById('switchToSignup');
  const switchToLogin = document.getElementById('switchToLogin');
  const openLogin = document.getElementById('openLogin');
  const openSignup = document.getElementById('openSignup');

  // Open modal
  function openModal(showSignup = false) {
    authModal.classList.remove('hidden');
    authModal.setAttribute('aria-hidden', 'false');

    if (showSignup) {
      loginForm.classList.add('hidden');
      signUpForm.classList.remove('hidden');
      document.getElementById('authTitle').textContent = 'Create Account';
    } else {
      loginForm.classList.remove('hidden');
      signUpForm.classList.add('hidden');
      document.getElementById('authTitle').textContent = 'Login';
    }
  }

  // Close modal on click outside
  authModal.addEventListener('click', e => {
    if (e.target === authModal) {
      authModal.classList.add('hidden');
      authModal.setAttribute('aria-hidden', 'true');
    }
  });

  // Switch forms
  switchToSignup.addEventListener('click', e => {
    e.preventDefault();
    openModal(true);
  });

  switchToLogin.addEventListener('click', e => {
    e.preventDefault();
    openModal(false);
  });

  // Openers from nav buttons
  openLogin?.addEventListener('click', e => { e.preventDefault(); openModal(false); });
  openSignup?.addEventListener('click', e => { e.preventDefault(); openModal(true); });

  // Login submission
  loginForm.addEventListener('submit', e => {
    e.preventDefault();
    const role = loginForm.querySelector("select[name='role']").value;
    if (role === "applicant") window.location.href = "owner.html";
    else if (role === "employer") window.location.href = "skillsandsports.html";
    else if (role === "admin") window.location.href = "admin.html";
  });

  // Signup submission
  signUpForm.addEventListener('submit', e => {
    e.preventDefault();
    alert('Sign up submitted!'); // Replace with your backend submission logic
  });
});
