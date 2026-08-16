

self.addEventListener('push', function(event) {
    if (event.data) {
        const data = event.data.json();
        
        const options = {
            body: data.body,
            // Static qovluğuna birbaşa yol:
            icon: data.icon || '/static/icons/logo.png', 
            badge: '/static/icons/logo.png',
            tag: data.conversation_id,
            vibrate: [200, 100, 200],
            data: {
                url: data.url
            }
        };

        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();

    if (event.notification.data && event.notification.data.url) {
        event.waitUntil(
            clients.openWindow(event.notification.data.url)
        );
    }
});