// static/main.js

function encrypt() {
    var plaintext = document.getElementById('plaintext').value;
    $.ajax({
        type: 'POST',
        url: '/encrypt',
        contentType: 'application/json',
        data: JSON.stringify({ plaintext: plaintext }),
        success: function(response) {
            document.getElementById('ciphertext').value = response.ciphertext;
        }
    });
}

function decrypt() {
    var ciphertext = document.getElementById('ciphertext').value;
    $.ajax({
        type: 'POST',
        url: '/decrypt',
        contentType: 'application/json',
        data: JSON.stringify({ ciphertext: ciphertext }),
        success: function(response) {
            document.getElementById('plaintext').value = response.plaintext;
        }
    });
}
