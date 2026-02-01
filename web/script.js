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
    
    if (!files.length) return alert("يا حسن، اختار الصور الأول!");

    // جلب القيمة المختارة (Gemini أو GPT)
    const provider = document.querySelector('input[name="provider"]:checked').value;

    const status = document.getElementById("status");
    const btn = document.getElementById("btn");
    
    status.innerHTML = `<span class="loader"></span> جاري المعالجة بواسطة ${provider.toUpperCase()}...`;
    btn.disabled = true;

    const formData = new FormData();
    for (let file of files) {
        formData.append("files", file);
    }
    
    // إضافة الموديل المختار للطلب المرسل للسيرفر
    formData.append("provider", provider);

    try {
        const response = await fetch("/convert", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `Doc_${provider}_${Date.now()}.docx`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            status.innerHTML = "✨ <span style='color: #4ade80'>تم التحويل والتحميل!</span>";
        } else {
            status.innerHTML = "❌ حدث خطأ في السيرفر";
        }
    } catch (err) {
        status.innerHTML = "❌ السيرفر لا يستجيب";
    } finally {
        btn.disabled = false;
    }
}