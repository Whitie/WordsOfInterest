document.addEventListener('DOMContentLoaded', function(e) {
    let element = document.getElementById('id_raw');
    if (element) {
        const easymde = new EasyMDE({
            element: element,
            forceSync: true,
            indentWithTabs: false,
            lineNumbers: true,
            sideBySideFullscreen: false,
            tabSize: 4
        });
    }
});
