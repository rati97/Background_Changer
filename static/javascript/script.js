function loadImage(event, previewId) {
    const reader = new FileReader();
    reader.onload = function(){
        let output = document.getElementById(previewId);
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}


document.getElementById('change-background-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    const selfieInput = document.getElementById('selfie');
    if (selfieInput.files.length === 0) {
        alert("Please upload a selfie before submitting");
        return;
    }
    const backgroundInput = document.getElementById('background');
    const bgColorInput = document.getElementById('bg-color');
    const resizeOptionInput = document.getElementById('resize-option');

    

    const selfieFile = selfieInput.files[0];
    const backgroundFile = backgroundInput.files[0];

    // Create a promise to handle reading the file
    function readFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onloadend = function() {
                resolve(reader.result);
            };

            reader.onerror = reject;
            if (file instanceof Blob) {
                reader.readAsDataURL(file);
            }else{
                resolve(null)
            }
        });
    }

    // When both files are fully read
    Promise.all([readFile(selfieFile), readFile(backgroundFile)]).then(function(results) {
        // Extract the file data from the data URLs
        const selfieData = results[0];
        const backgroundData = results[1];
        

        // Prepare the data to send to the server
        const data = {
            'selfie': selfieData,
            'background': backgroundData,
            'bg_color': bgColorInput.value,
            'resize_option': resizeOptionInput.value,
        };

        // Send the data to the server
        let url = document.getElementsByClassName("submit-url");
        url = url[0].id
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(function(response) {
            // Handle the server's response
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('An error occurred: ' + response.statusText);
            }
        }).then(function(data) {
            if (data && data.result) {
                console.log('Background changed successfully');
                
                const result_image = document.getElementById('result-image');
                result_image.style.display = "block"
                result_image.src = data.result;
            } else {
                throw new Error('An error occurred: The server\'s response did not include a result');
            }
        }).catch(function(error) {
            console.error(error);
        });
    });
});
