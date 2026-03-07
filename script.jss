async function convertToPDF(){

const { jsPDF } = window.jspdf;

let files = document.getElementById("imageInput").files;

let pdf = new jsPDF();

for(let i=0;i<files.length;i++){

let imgData = await fileToDataURL(files[i]);

if(i>0){
pdf.addPage();
}

pdf.addImage(imgData,'JPEG',10,10,180,160);

}

pdf.save("converted.pdf");

}

function fileToDataURL(file){
return new Promise((resolve)=>{
let reader = new FileReader();
reader.onload = e => resolve(e.target.result);
reader.readAsDataURL(file);
});
}
