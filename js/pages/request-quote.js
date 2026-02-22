/**
 * Al Meeran Upholstery - Request Quote Form Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    const quoteForm = document.getElementById('upholstery-quote-form');

    if (quoteForm) {
        quoteForm.addEventListener('submit', handleQuoteFormSubmission);
    }

    async function handleQuoteFormSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        try {
            const response = await fetch('http://localhost:5000/api/quotes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: data.user_name,
                    phone: data.user_phone,
                    type: data.furniture_type,
                    message: data.user_message
                })
            });

            if (!response.ok) throw new Error('Network response was not ok');

            // Success
            alert(`Thank you, ${data.user_name}! Your quote request has been received.`);
            event.target.reset();

        } catch (error) {
            console.error('Error submitting quote:', error);
            // Fallback to local storage if backend fails (Offline Mode)
            const quotes = JSON.parse(localStorage.getItem('al_meeran_quotes')) || [];
            quotes.push({
                name: data.user_name,
                phone: data.user_phone,
                type: data.furniture_type,
                message: data.user_message,
                date: new Date().toLocaleDateString()
            });
            localStorage.setItem('al_meeran_quotes', JSON.stringify(quotes));
            alert(`(Offline Mode) Thank you! Your request has been saved locally and will be processed soon.`);
            event.target.reset();
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    }
});
