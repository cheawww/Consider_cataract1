// document.getElementById('capture').addEventListener('click', function() {
//     const video = document.getElementById('video');
//     const canvas = document.getElementById('canvas');
//     const context = canvas.getContext('2d');
//     const capturedImage = document.getElementById('captured-image');

//     context.drawImage(video, 0, 0, canvas.width, canvas.height);
//     canvas.toBlob(function(blob) {
//         const file = new File([blob], "photo.jpg", { type: 'image/jpeg' });
//         const dataTransfer = new DataTransfer();
//         dataTransfer.items.add(file);
//         document.getElementById('photo').files = dataTransfer.files;

//         const imageUrl = URL.createObjectURL(blob);
//         capturedImage.src = imageUrl;
//         capturedImage.style.display = 'block';
//         video.srcObject.getTracks().forEach(track => track.stop());
//         video.style.display = 'none';
//         canvas.style.display = 'none';
//         document.getElementById('capture').style.display = 'none';


document.getElementById('capture').addEventListener('click', function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const capturedImage = document.getElementById('captured-image');

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const base64Image = canvas.toDataURL('image/jpeg');

    const imageJson = JSON.stringify({ image: base64Image });

    const blob = new Blob([imageJson], { type: 'application/json' });
    const file = new File([blob], "photo.json", { type: 'application/json' });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    document.getElementById('photo').files = dataTransfer.files;

    const imageUrl = URL.createObjectURL(blob);
    capturedImage.src = base64Image;
    capturedImage.style.display = 'block';

    video.srcObject.getTracks().forEach(track => track.stop());
    video.style.display = 'none';
    canvas.style.display = 'none';
    document.getElementById('capture').style.display = 'none';
});
