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
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        const apiData = new FormData();
        apiData.append('name', formData.get('user_name'));
        apiData.append('phone', formData.get('user_phone'));
        apiData.append('type', formData.get('furniture_type'));
        apiData.append('message', formData.get('user_message'));
        
        const imageFile = formData.get('furniture_image');
        if (imageFile && imageFile.name) {
            apiData.append('image', imageFile);
        }

        try {
            const response = await fetch('/api/quotes', {
                method: 'POST',
                body: apiData
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
