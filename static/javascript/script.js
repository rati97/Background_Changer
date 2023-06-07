function loadImage(event, previewId) {
    const reader = new FileReader();
    reader.onload = function(){
        let output = document.getElementById(previewId);
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}