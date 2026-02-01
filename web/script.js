function updateFileName() {
    const input = document.getElementById('images');
    const labelSpan = document.getElementById('file-name');
    if (input.files.length > 0) {
        labelSpan.innerText = `✅ تم اختيار ${input.files.length} صور`;
        labelSpan.style.color = "#a855f7";
    }
}

async function startProcess() {
    const input = document.getElementById("images");
    const files = input.files;
    
    if (!files.length) return alert("اختر الصور اولا!");

    const status = document.getElementById("status");
    const btn = document.getElementById("btn");
    
    status.innerHTML = '<span class="loader"></span> جاري المعالجة...';
    btn.disabled = true;

    const formData = new FormData();
    for (let file of files) {
        formData.append("files", file);
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/convert", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `Doc_${Date.now()}.docx`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            status.innerHTML = "✨ <span style='color: #4ade80'>تم التحميل بنجاح!</span>";
        } else {
            status.innerHTML = "❌ حدث خطأ في السيرفر";
        }
    } catch (err) {
        status.innerHTML = "❌ السيرفر مش شغال.. اتأكد إنك فاتح api.py";
    } finally {
        btn.disabled = false;
    }
}