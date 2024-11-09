document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    const links = document.querySelectorAll('a[href^="#"]');
    for (const link of links) {
        link.addEventListener('click', smoothScroll);
    }

    // Add animation to features on scroll
    const features = document.querySelectorAll('.feature');
    window.addEventListener('scroll', animateOnScroll);

    // Form validation
    const forms = document.querySelectorAll('form');
    for (const form of forms) {
        form.addEventListener('submit', validateForm);
    }

    // Automatic logout after inactivity
    setupInactivityLogout();
});

function smoothScroll(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href');
    const targetElement = document.querySelector(targetId);
    targetElement.scrollIntoView({ behavior: 'smooth' });
}

function animateOnScroll() {
    const features = document.querySelectorAll('.feature');
    for (const feature of features) {
        const featureTop = feature.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        if (featureTop < windowHeight) {
            feature.style.opacity = '1';
            feature.style.transform = 'translateY(0)';
        }
    }
}

function validateForm(e) {
    const form = e.target;
    const inputs = form.querySelectorAll('input, select');
    let isValid = true;

    for (const input of inputs) {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    }

    if (!isValid) {
        e.preventDefault();
        alert('Please fill in all fields');
    }
}

function setupInactivityLogout() {
    let inactivityTime = 0;
    const logoutTime = 30 * 60 * 1000; // 30 minutes

    document.addEventListener('mousemove', resetInactivityTimer);
    document.addEventListener('keypress', resetInactivityTimer);

    function resetInactivityTimer() {
        inactivityTime = 0;
    }

    setInterval(() => {
        inactivityTime += 1000;
        if (inactivityTime >= logoutTime) {
            alert('You have been logged out due to inactivity');
            window.location.href = '/logout';
        }
    }, 1000);
}